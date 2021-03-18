import tkinter as tk

from tkinter import *
import time
import threading
import random
import queue
import pigpio
import math

class HWBoard(threading.Thread):
    def __init__ (self, clock=21, mosi=20, miso=19, ce0=16, ce1=5, latch=26, reads_per_second=90):
        threading.Thread.__init__(self)
        
        self.daemon = True
        self._pi = pigpio.pi()
        self._clock = clock
        self._mosi = mosi
        self._miso = miso
        self._ce0 = ce0
        self._ce1 = ce1
        self._latch = latch
        self._interval = 1.0 / reads_per_second
        
        self._chips = 2
        self._last_data = [0]*self._chips
        self._data_out = [0]*self._chips
        self._data_in = [0]*self._chips
        
        self._adc_channels = 8
        self._adc_value = [0]*self._adc_channels
        
        self._blink_last = time.time()
        self._blink_period = 1
        self._blink_fraction = [0.5]*8*self._chips
        
        self._adc_commands = []
        
        self._adc_active_channels = {16,17}
        
        for i in range(8):
            cmd = [1, 1, i & 1, (i & 2) >> 1, (i & 4) >> 2]
            self._adc_commands.append(cmd)
            
        self.queue = queue.Queue()
        
    def processOutgoing(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                
                msg = self.queue.get(0)
                
                if isinstance(msg, tuple):
                    # Check contents of message and do whatever is needed.
                    pin = msg[0]
                    val = msg[1]
                    print("process outgoing")
                    print("pin " + str(pin) + " value = " + str(val))
                    if pin > 7:
                        self._data_out[1] = self.set_bit(self._data_out[1], pin - 8, val)
                    else:
                        self._data_out[0] = self.set_bit(self._data_out[0], pin, val)
                    
                elif isinstance(msg, set):
                    #the last entry is the ADC subscribed pins
                    self._adc_active_channels = msg.copy()                    
            
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass        
                
    def set_bit(self, v, index, x):
        """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
        mask = 1 << index    # Compute mask, an integer with just bit 'index' set.
        v &= ~mask             # Clear the bit indicated by the mask (if x is False)
        if x:
            v |= mask            # If x was True, set the bit indicated by the mask.
        return v                # Return the result, we're done.

    def clock(self):       
        self._pi.gpio_trigger(self._clock, 1, 1)
                
    def readDigital(self, msgQueue):
        self._pi.write(self._latch, 0)
        self._pi.write(self._clock, 0)
        self._pi.write(self._ce0, 1)
        
        self._pi.gpio_trigger(self._clock, 1, 1)
        
        self._pi.write(self._ce0, 0)
        
        self._pi.gpio_trigger(self._clock, 1, 1)
        self._pi.write(self._ce0, 1)
        
        self._data_in[0] = 0
        self._data_in[1] = 0
        
        read_time = time.time()
        
        blink_current = read_time - self._blink_last
        
        while blink_current > self._blink_period:
            self._blink_last = self._blink_last + self._blink_period
            blink_current = read_time - self._blink_last
        
        #tmp = self._data_out
        
    # 3. Transfer        
        for i in range(16):
            outval = 0
            if self._data_out[math.floor(i/8)] & (1 << i%8) != 0:
                # state is one, find which part of the blink state we are in
                if blink_current < self._blink_fraction[math.floor(i/8)] * self._blink_period:
                    outval = 1
            inval = self._pi.read(self._miso)
            self._pi.write(self._mosi, outval)
            self._data_in[math.floor(i/8)] |= (inval << i%8)
            #print("bit " + str(i) + " = " + str(inval))
            self._pi.gpio_trigger(self._clock, 1, 1)
            
        
    # 4. Output latch
        self._pi.write(self._ce0, 1)
        self._pi.write(self._latch, 1)
        
        self._pi.gpio_trigger(self._clock, 1, 1)
        
        if self._data_in != self._last_data:
            # Emit callbacks for changed levels.
            for i in range(self._chips):
                if self._data_in[i] != self._last_data[i]:
                    for j in range(8):
                        key = (i*8)+j
                        if ((self._data_in[i] & (1<<j)) != (self._last_data[i] & (1<<j))):
                            #self._callback(self, key, (self._data_in[i]>>j)&1, read_time)
                            event = (self, key, (self._data_in[i]>>j)&1, read_time)
                            msgQueue.put(event)
            
            self._last_data[0] = self._data_in[0]
            self._last_data[1] = self._data_in[1]
            
    def readAnalog(self, msgQueue):
        #with self._lock:    
        sensitivity = 2
        #only read ADC for current subscribers since the read is costly
        read_time = time.time()
        #for i in self._sub
        for i in self._adc_active_channels:
            new_adc = self.getADC(i-16)
            #print("adc " + str(i) + " = " + str(new_adc[i]))
            if abs(new_adc - self._adc_value[i-16]) > sensitivity:
                event = (self, i, new_adc, read_time)
                msgQueue.put(event)
                self._adc_value[i-16] = new_adc
                
    # read SPI data from ADC8038
    def getADC(self, channel):
    # 1. CS LOW.
        #self._pi.write(self._PIN_CLK, 1)
        self._pi.write(self._ce1, 1)
        self._pi.write(self._ce1, 0)
        #self._pi.gpio_trigger(self._clock, 1, 1)
    # 2. Start clock
        self._pi.write(self._clock, 0)
        
    # 3. Input MUX address
        cmd = self._adc_commands[channel]
        #print("Address word:" + str(cmd))
        for i in cmd: # start bit + mux assignment
            if (i == 1):
                self._pi.write(self._mosi,1)
            else:
                self._pi.write(self._mosi,0)
            self._pi.gpio_trigger(self._clock, 1, 1)
            
    # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            self._pi.gpio_trigger(self._clock, 1, 1)
            ad <<= 1 # shift bit
            if self._pi.read(self._miso):
                ad |= 0x1 # set first bit

    # 5. reset
        self._pi.write(self._ce1, 1)
        self._pi.write(self._mosi,0)
        self._pi.gpio_trigger(self._clock, 1, 1)
        self._pi.gpio_trigger(self._clock, 1, 1)

        return ad       
        
class GuiPart:
    def __init__ (self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        console = tk.Button(master, text='Done', command=endCommand)
        console.pack(  )
        # Add more GUI stuff here depending on your specific needs
        self.subscribers = {}
    
    def subscribe(self, pinRange, callback):
        for pin in pinRange:
            print("subscribing pin " + str(pin))
            if pin not in self.subscribers:
                self.subscribers[pin] = []
            self.subscribers[pin].append(callback)
            
    def unsubscribe(self, pinRange, callback):
        for pin in pinRange:
            print("unsubscribing pin " + str(pin))
            if pin in self.subscribers:
                self.subscribers[pin].remove(callback)
                if len(self.subscribers[pin]) == 0:
                    self.subscribers.pop(pin, None)
                
    def clear_subscribers(self, pinRange):
        for pin in pinRange:
            if pin in self.subscribers:
                print("unsubscribing pin " + str(pin))
                self.subscribers[pin].clear()
                self.subscribers.pop(pin, None)
    
    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                hw_board = msg[0]
                # Check contents of message and do whatever is needed.
                print("pin " + str(msg[1]) + " value = " + str(msg[2]))
                pin = msg[1]
                if pin in self.subscribers:
                    for s in self.subscribers[pin]:
                        s(msg)
                #val = msg[2]
                if pin < 16:
                    out = (msg[1], msg[2], msg[3])
                    hw_board.queue.put(out)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        
        self._next_time = time.time()
        
        reads_per_second = 60
        
        self._interval = 1.0 / reads_per_second
        
        self.hw_board = HWBoard()
        
        self.hw_thread = threading.Thread(target=self.hw_update)
        self.hw_thread.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )
        self.gui.subscribe(range(16,21), self.event)
        self.gui.clear_subscribers(range(0,24))
        
    def event(self, msg):
        print("Subscribed event triggered")
        print(msg)

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def hw_update(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        self._next_time = time.time()
        avgAnalogReadTime = 0
        avgDigitalReadTime = 0
        avgReadTime = 0
        nReads = 0.0
        while self.running:
            self.hw_board.processOutgoing()
            start_time = time.time()
            self.hw_board.readDigital(self.queue)
            digital_time = time.time()
            self.hw_board.readAnalog(self.queue)
            finish_time = time.time()

            nReads = nReads + 1.0
            avgDigitalReadTime = avgDigitalReadTime + digital_time - start_time
            avgAnalogReadTime = avgAnalogReadTime + finish_time - digital_time
            avgReadTime = avgReadTime + finish_time - start_time
            self._next_time += self._interval
            delay = self._next_time - time.time()
            if delay > 0.0:
                time.sleep(delay)
                
        print("Digital read:" + str(avgDigitalReadTime/nReads))
        print("Analog read:" + str(avgAnalogReadTime/nReads))
        print("Total time to read:" + str(avgReadTime/nReads))

    def endApplication(self):
        self.running = 0
        
    def close_window(self):
        print( "Window closed")
        self.endApplication()

rand = random.Random(  )
root = tk.Tk(  )

client = ThreadedClient(root)
root.mainloop(  )