#!/usr/bin/env python

import time
import threading
import pigpio

MAIN_SPI=0
AUX_SPI=1

RBUTTON_MAP = {0:9,1:8,2:10,3:12,4:15,5:13,6:14,7:5,8:6,9:7,10:4,11:0,12:1,13:3,14:2}

#pin 9 maps to button 0
#BUTTON_MAP = {9:0,8:1,10:2,12:3,15:4,13:5,14:6,5:7,6:8,7:9,4:10,0:11,1:12,3:13,2:14}

BUTTON_MAP = {0:11,1:12,2:14,3:13,4:10,5:7,6:8,7:9,8:1,9:0,10:2,12:3,13:5,14:6,15:4} #11:15

# button 7 maps to led pin 0
#LED_MAP = {7:0,6:1,5:2,14:3,13:4,12:5,11:6,10:7,0:13,4:8,3:9,2:10,1:11,0:13,8:15,9:14,15:12}#working
LED_MAP = {7:0,6:1,5:2,14:3,13:4,12:5,11:6,10:7,4:8,3:9,2:10,1:11,8:12,0:13,9:14,15:15}
#0,1,2,3,4,5,6,7,8,9,10,11,x12x,13,14,15
LED_STATE = [0x00,0x00]

BUTTON_STATE = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def set_bit(v, index, x):
   """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
   mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
   v &= ~mask          # Clear the bit indicated by the mask (if x is False)
   if x:
      v |= mask         # If x was True, set the bit indicated by the mask.
   return v            # Return the result, we're done.

class PISO(threading.Thread):
   """
   A class to read multiple inputs from one or more
   SN74HC165 PISO (Parallel In Serial Out) shift
   registers.

   Either the main SPI or auxiliary SPI peripheral
   is used to clock the data off the chip.  SPI is
   used for performance reasons.

   Connect a GPIO (referred to as SH_LD) to pin 1 of
   the first chip.

   Connect SPI SCLK to pin 2 of the first chip.  SCLK
   will be GPIO 11 if the main SPI is being used and
   GPIO 21 if the auxiliary SPI is being used.

   Connect SPI MISO to pin 9 of the last chip.  MISO
   will be GPIO 9 if the main SPI is being used and
   GPIO 19 if the auxiliary SPI is being used.

                      First chip

   Pi GPIO ------> SH/LD 1 o 16 Vcc ------ 3V3
   Pi SPI clock -> CLK   2   15 CLK INH -- Ground
                   E     3   14 D
                   F     4   13 C
                   G     5   12 B
                   H     6   11 A
   Don't connect   /Qh   7   10 SER ------ Ground
   Ground -------- GND   8    9 Qh ------> next SER


                     Middle chips

   prior SH/LD --> SH/LD 1 o 16 Vcc ------ 3V3
   prior CLK ----> CLK   2   15 CLK INH -- Ground
                   E     3   14 D
                   F     4   13 C
                   G     5   12 B
                   H     6   11 A
   Don't connect   /Qh   7   10 SER <----- prior Qh
   Ground -------- GND   8    9 Qh ------> next SER


                       Last chip

   prior SH/LD --> SH/LD 1 o 16 Vcc ------ 3V3
   prior CLK ----> CLK   2   15 CLK INH -- Ground
                   E     3   14 D
                   F     4   13 C
                   G     5   12 B
                   H     6   11 A
   Don't connect   /Qh   7   10 SER <----- prior Qh
   Ground -------- GND   8    9 Qh ------> Pi SPI MISO
   """
   SPI_FLAGS_AUX=256   # use auxiliary SPI device
   SPI_FLAGS_NO_CE0=32 # don't use CE0

   def __init__(self, pi, SH_LD, OUTPUT_LATCH, SPI_device=AUX_SPI,
      chips=1, reads_per_second=100, callback=None):
      """
      Instantiate with the connection to the Pi.

      SL_LD is the GPIO connected to the shift/load pin
      of the shift register.

      SPI_device is either MAIN_SPI (default) or AUX_SPI.

      chips is the number of SN74HC165 being used (defaults
      to 1).

      reads_per_second is the number of readings to
      be made per second (defaults to 100).
      
      If a callback is specified it will be called once
      for each pin level change.  The callback receives
      the pin, the new level, and the time of reading.
      """

      threading.Thread.__init__(self)

      self._lock = threading.Lock()

      self.set_reads_per_second(reads_per_second)

      self._pi = pi
      
      assert 0 <= SH_LD <= 53
      self._SH_LD = SH_LD

      assert 0 <= SPI_device <= 1
      flags = self.SPI_FLAGS_NO_CE0
      if SPI_device == AUX_SPI:
         flags |= self.SPI_FLAGS_AUX
      self._h = pi.spi_open(0, 5000000, flags)#was 5000000

      #self._h.max_speed_hz = 500000

      self._OUTPUT_LATCH = OUTPUT_LATCH

      self._pi.set_mode(self._OUTPUT_LATCH, pigpio.OUTPUT)
      self._pi.write(self._OUTPUT_LATCH, 1)

      assert 1 <= chips
      self._chips = chips

      self._callback = callback

      self._last_data = [0]*chips

      self._data_out = [0]*chips
      
      self._exiting = False

      self.daemon = True

      self.start()

      #self._outputs = [0xFF,0xFF]

   def read(self):
      """
      Reads the shift registers and returns the
      readings as a byte array (one byte per
      chip).

      In addition if a callback is registered it
      will be called for each pin level change.
      """
      data = None
      with self._lock:
         if self._exiting:
            return data
         
         
         self._pi.gpio_trigger(self._SH_LD, 1, 0)
         
         self._pi.write(self._OUTPUT_LATCH, 0)
         #self._pi.write(self._SH_LD, 0)
         
         #time.sleep(0.001)
         read_time = time.time()
         
         count, data = self._pi.spi_xfer(self._h, self._data_out)#_outputs)##[0xFF])##self._chips)
         
         #print(str(count))
         #print(str(data))
         if data != self._last_data:
            if self._callback is not None:
               # Emit callbacks for changed levels.
               for i in range(self._chips):
                  if data[i] != self._last_data[i]:
                     for j in range(8):
                        key = (i*8)+j
                        if ((data[i] & (1<<j)) != (self._last_data[i] & (1<<j))):
                           #print("bit " + str(i*8+j) + " changed")
                           #if (i*8)+j in BUTTON_MAP:
                           ret_val = None
                           if key in BUTTON_MAP:
                              btn = BUTTON_MAP[key]
                              ret_val = self._callback(btn, (data[i]>>j)&1, read_time)
                           if ret_val is not None:
                              self._data_out = ret_val
            
            self._last_data = data
            #self._outputs[0] = data[0]#[0xFF,0xFF]#data
         self._pi.write(self._OUTPUT_LATCH, 1)
         #self._pi.write(self._SH_LD, 1)
      return data
    
   def set_data(self, d):
       self._data_out = d.copy()
       
   def set_led(self, led, val):
      led_pin = LED_MAP[led]
      #print("LED PIN = " + str(led_pin) + " set to " + str(val))
      
      if led_pin > 7:
         self._data_out[1] = set_bit(self._data_out[1], led_pin - 8, val)
      else:
         self._data_out[0] = set_bit(self._data_out[0], led_pin, val)       

   def set_callback(self, callback):
      """
      Sets the callback function.  The callback will
      be called for each pin level change.

      The callback receives three parameters:
         the pin
         the new level
         the time of the reading

      There are 8 pins per chip.  The last chip has
      pins numbered 0 to 7, the next to last chip has
      pins numbered 8 to 15 etc.

      The callback is cleared by setting it to None.
      """
      with self._lock:
         self._callback = callback

   def set_reads_per_second(self, reads_per_second):
      """
      Sets the number of chip reads per second.
      It must be between 1 and 5000 reads per
      second.
      """
      with self._lock:
         assert 1 <= reads_per_second <= 5000
         self._interval = 1.0 / reads_per_second

   def cancel(self):
      """
      Cancels chip readings and releases resources.
      """
      with self._lock:
         self._exiting = True
         self._pi.spi_close(self._h)

   def run(self):
      self._next_time = time.time()
      while not self._exiting:
         self.read()
         self._next_time += self._interval
         delay = self._next_time - time.time()
         if delay > 0.0:
            time.sleep(delay)

if __name__ == "__main__":

   import time
   import SN74HC165
   import pigpio
   
   def toggleBit(n, k):
       return (n^(1<<(k-1)))

   def cbf(pin, level, tick):
      print(pin, level, tick)
      btn = pin #BUTTON_MAP[pin]
      print("Button " + str(btn))
      if BUTTON_STATE[btn] == 0:
         BUTTON_STATE[btn] = 1
      else:
         BUTTON_STATE[btn] = 0
         
      val = BUTTON_STATE[btn]
      led_pin = LED_MAP[btn]
      print("LED PIN = " + str(led_pin))
      
      if led_pin > 7:
         LED_STATE[1] = toggleBit(LED_STATE[1], led_pin - 7)
      else:
         LED_STATE[0] = toggleBit(LED_STATE[0], led_pin + 1)
         
      #LED_STATE[0] = 1
      #LED_STATE[1] = 0
         
      return LED_STATE

   pi = pigpio.pi()
   if not pi.connected:
      exit()

   run_for = 300

   sr = SN74HC165.PISO(
           pi, SH_LD=16, OUTPUT_LATCH=26,
           SPI_device=SN74HC165.AUX_SPI, chips=2,
           reads_per_second=30, callback=cbf)
   
   time.sleep(1)
   sr.set_led(8, 0)

   while True:
      run_for = 0.1
      #time.sleep(run_for)
      for i in range(0,15):
          sr.set_led(i,1)
          time.sleep(run_for)
          sr.set_led(i,0)
          time.sleep(run_for)
      #for i in range(0,15):
      #    sr.set_led(i,0)
      #time.sleep(run_for)
       
   # read all registers
   r = sr.read()
   # and print each value
   for i in range(len(r)):
      print(r[i])

   sr.cancel()
   pi.stop()
