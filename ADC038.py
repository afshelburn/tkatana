#!/usr/bin/env python

import time
import threading
import pigpio

MAIN_SPI=0
AUX_SPI=1

def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.

class ADC(threading.Thread):
    SPI_FLAGS_AUX=256   # use auxiliary SPI device
    SPI_FLAGS_NO_CE0=32 # don't use CE0
    SPI_FLAGS_MSB_FIRST=16384
    
    def __init__(self, pi, chip_select=16, SPI_device=AUX_SPI,
      channels=8, reads_per_second=10, callback=None):
    
        threading.Thread.__init__(self)

        self._lock = threading.Lock()

        self.set_reads_per_second(reads_per_second)

        self._pi = pi

        assert 0 <= SPI_device <= 1
        flags = self.SPI_FLAGS_NO_CE0
        flags |= self.SPI_FLAGS_MSB_FIRST
        if SPI_device == AUX_SPI:
            flags |= self.SPI_FLAGS_AUX
        self._h = pi.spi_open(0, 32000, flags)#was 5000000

        #self._h.max_speed_hz = 500000

        self._chip_select = chip_select
        self._pi.set_mode(self._chip_select, pigpio.OUTPUT)
        self._pi.write(self._chip_select, 1)

        self._channels = 8

        self._callback = callback

        self._last_data = [0]*self._channels

        self._data_out = [0]*self._channels

        self._exiting = False

        self.daemon = True

        self.start()

      #self._outputs = [0xFF,0xFF]
        
    def make_control_word(self, channel):                                      
        word = 0x18 #; /* 1 1000 */       #                           
        lsb = channel & 0x01            #                          
        word = word | (lsb <<2)#  /* 1 1 lsb 0 0 */               
        word = word | (channel >>1)# /* 1 1 lsb msb middle */      
        return word                                             

    # read SPI data from ADC8032
    def getADC(self, channel):
        PIN_CS = 16
        PIN_CLK = 21
        PIN_DI = 19
        PIN_DO = 20
    # 1. CS LOW.
#        GPIO.output(PIN_CS, True)      # clear last transmission
#        GPIO.output(PIN_CS, False)     # bring CS low
        
        self._pi.write(PIN_CS, 1)
        self._pi.write(PIN_CS, 0)

    # 2. Start clock
#        GPIO.output(PIN_CLK, False)  # start clock low
        self._pi.write(PIN_CLK, 0)


    # 3. Input MUX address
        for i in [1,1,channel]: # start bit + mux assignment
            if (i == 1):
#                GPIO.output(PIN_DI, True)
                self._pi.write(PIN_DI,1)
            else:
#                GPIO.output(PIN_DI, False)
                self._pi.write(PIN_DI,0)

#            GPIO.output(PIN_CLK, True)
#            GPIO.output(PIN_CLK, False)
            self._pi.gpio_trigger(PIN_CLK, 50, 1)

        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            self._pi.gpio_trigger(PIN_CLK, 50, 1)
#            GPIO.output(PIN_CLK, True)
#            GPIO.output(PIN_CLK, False)
            ad <<= 1 # shift bit
#            if (GPIO.input(PIN_DO)):
            if self._pi.read(PIN_DO):
                ad |= 0x1 # set first bit

        # 5. reset
        GPIO.output(PIN_CS, True)

        return ad

    def read(self):

        data = None
        with self._lock:
            if self._exiting:
                return data

            for i in range(0,self._channels):
                #print("Reading channel " + str(i))
                self._pi.write(self._chip_select, 1)
                self._pi.write(self._chip_select, 0)
                read_time = time.time()

                self._data_out = [0x00,0x00,0x00]
                self._data_out[0] = 0xFF & self.make_control_word(i)
                
                #print("Control word: " + str(self._data_out[0]))
                
                count, data = self._pi.spi_xfer(self._h, self._data_out)#_outputs)##[0xFF])##self._chips)

                self._pi.write(self._chip_select, 1)
                
                #print("Count = " + str(count))
                print("Channel = " + str(i) + " = " + str(data[2]))
                time.sleep(0.01)
         #print(str(count))
         #print(str(data))
#          if data != self._last_data:
#             if self._callback is not None:
#                # Emit callbacks for changed levels.
#                for i in range(self._chips):
#                   if data[i] != self._last_data[i]:
#                      for j in range(8):
#                         if ((data[i] & (1<<j)) != (self._last_data[i] & (1<<j))):
#                            #print("bit " + str(i*8+j) + " changed")
#                            btn = BUTTON_MAP[(i*8)+j]
#                            ret_val = self._callback(btn, (data[i]>>j)&1, read_time)
#                            if ret_val is not None:
#                               self._data_out = ret_val
#             
#             self._last_data = data
            #self._outputs[0] = data[0]#[0xFF,0xFF]#data
            
        return data
    
    def set_data(self, d):
        self._data_out = d.copy()     

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

PIN_CS = 5
PIN_CLK = 21
PIN_DI = 20
PIN_DO = 19
        
class SimpleADC:
    def __init__(self, pi):
        print("Simple ADC")
        self._pi = pi
        self._pi.set_mode(PIN_CS, pigpio.OUTPUT)
        self._pi.set_mode(PIN_DO, pigpio.INPUT)
        self._pi.set_mode(PIN_DI, pigpio.OUTPUT)
        self._pi.set_mode(PIN_CLK, pigpio.OUTPUT)
        
    def clock(self):       
        self._pi.gpio_trigger(PIN_CLK, 25)
        #self._pi.write(PIN_CLK, 1)
        #time.sleep(0.01)
        #self._pi.write(PIN_CLK, 0)
        #time.sleep(0.01)
        
    # read SPI data from ADC8032
    def getADC(self, channel):

    # 1. CS LOW.
#        GPIO.output(PIN_CS, True)      # clear last transmission
#        GPIO.output(PIN_CS, False)     # bring CS low
        #self._pi.write(16,1)
        self._pi.write(PIN_CS, 1)
        self._pi.write(PIN_CS, 0)

    # 2. Start clock
#        GPIO.output(PIN_CLK, False)  # start clock low
        self._pi.write(PIN_CLK, 0)


    # 3. Input MUX address
        cmd = [1, 1, channel & 1, (channel & 2) >> 1, (channel & 4) >> 2]
        #print("Address word:" + str(cmd))
        for i in cmd: # start bit + mux assignment
            if (i == 1):
#                GPIO.output(PIN_DI, True)
                self._pi.write(PIN_DI,1)
            else:
#                GPIO.output(PIN_DI, False)
                self._pi.write(PIN_DI,0)

#            GPIO.output(PIN_CLK, True)
#            GPIO.output(PIN_CLK, False)
            #self._pi.gpio_trigger(PIN_CLK, 70, 1)
            self.clock()
        # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            #self._pi.gpio_trigger(PIN_CLK, 70, 1)
            self.clock()
#            GPIO.output(PIN_CLK, True)
#            GPIO.output(PIN_CLK, False)
            ad <<= 1 # shift bit
#            if (GPIO.input(PIN_DO)):
            if self._pi.read(PIN_DO):
                ad |= 0x1 # set first bit

        # 5. reset
#        GPIO.output(PIN_CS, True)
        self._pi.write(PIN_CS, 1)

        return ad    

if __name__ == "__main__":

    import time
    import ADC038
    import pigpio

    def toggleBit(n, k):
        return (n^(1<<(k-1)))

    def cbf(pin, level, tick):
        print(pin, level, tick)

    pi = pigpio.pi()
    if not pi.connected:
        exit()

    run_for = 5

    adc = SimpleADC(pi)

    while True:
        pi.write(16, 1)
        pi.write(PIN_CS, 1)
        
        for i in range(8):
            val = adc.getADC(i)
            if i == 0:
                print("Ch " + str(i) + ":" + str(val))
            
#         time.sleep(0.5)
#         pi.write(PIN_CS, 0)
#         time.sleep(0.5)
#    adc = ADC038.ADC(
#           pi, chip_select=16, SPI_device=ADC038.AUX_SPI, channels=8,
#           reads_per_second=1, callback=cbf)

    time.sleep(13)

#    adc.cancel()
    pi.stop()
