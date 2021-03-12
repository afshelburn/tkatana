import tkinter as tk

from tkinter import *
import time
import threading
import random
import queue
import pigpio

class HWBoard(threading.Thread):
    def __init__ (self, clock=21, mosi=20, miso=19, ce0=16, ce1=5, latch=26, reads_per_second=60):
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
        
        self._adc_channels = 5
        self._adc_value = [0]*self._adc_channels
        
        self.queue = queue.Queue()
        
    def processOutgoing(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed.
                pin = msg[1]
                val = msg[2]
                print("pin " + str(msg[1]) + " value = " + str(msg[2]))
                if pin > 7:
                    self._data_out[1] = self.set_bit(self._data_out[1], pin - 8, val)
                else:
                    self._data_out[0] = self.set_bit(self._data_out[0], pin, val)
            
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
        self._pi.gpio_trigger(self._clock, 2, 1)
                
    def readDigital(self, msgQueue):
        self._pi.write(self._latch, 0)
        self._pi.write(self._clock, 0)
        self._pi.write(self._ce0, 1)
        
        self.clock()
        
        self._pi.write(self._ce0, 0)
        
        self.clock()
        self._pi.write(self._ce0, 1)
        
        self._data_in[0] = 0
        self._data_in[1] = 0
        
        read_time = time.time()
        
    # 3. Transfer
        for i in range(8):
            outval = 0
            if self._data_out[0] & (1 << i) != 0:
                outval = 1
            inval = self._pi.read(self._miso)
            self._pi.write(self._mosi, outval)
            self._data_in[0] |= (inval << i)
            #print("bit " + str(i) + " = " + str(inval))
            self.clock()
            
        for i in range(8):
            outval = 0
            if self._data_out[1] & (1 << i) != 0:
                outval = 1
            inval = self._pi.read(self._miso)
            self._data_in[1] |= (inval << i)
            self._pi.write(self._mosi, outval)
            #print("bit " + str(i+8) + " = " + str(inval))
            self.clock()
        
    # 4. Output latch
        self._pi.write(self._ce0, 1)
        self._pi.write(self._latch, 1)
        
        self.clock()
        
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
        read_time = time.time()
        for i in range(self._adc_channels):
            new_adc = self.getADC(i)
            #print("adc " + str(i) + " = " + str(new_adc[i]))
            if abs(new_adc - self._adc_value[i]) > sensitivity:
                event = (self, i+16, new_adc, read_time)
                msgQueue.put(event)
                self._adc_value[i] = new_adc
                
    # read SPI data from ADC8038
    def getADC(self, channel):
    # 1. CS LOW.
        #self._pi.write(self._PIN_CLK, 1)
        self._pi.write(self._ce1, 1)
        self._pi.write(self._ce1, 0)
        #self.clock()
    # 2. Start clock
        self._pi.write(self._clock, 0)
        
    # 3. Input MUX address
        cmd = [1, 1, channel & 1, (channel & 2) >> 1, (channel & 4) >> 2]
        #print("Address word:" + str(cmd))
        for i in cmd: # start bit + mux assignment
            if (i == 1):
                self._pi.write(self._mosi,1)
            else:
                self._pi.write(self._mosi,0)
            self.clock()
            
    # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            self.clock()
            ad <<= 1 # shift bit
            if self._pi.read(self._miso):
                ad |= 0x1 # set first bit

    # 5. reset
        self._pi.write(self._ce1, 1)
        self._pi.write(self._mosi,0)
        self.clock()
        self.clock()

        return ad                    
        
class GuiPart:
    def __init__ (self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        console = tk.Button(master, text='Done', command=endCommand)
        console.pack(  )
        # Add more GUI stuff here depending on your specific needs
        
    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                hw_board = msg[0]
                # Check contents of message and do whatever is needed.
                print("pin " + str(msg[1]) + " value = " + str(msg[2]))
                pin = msg[1]
                #val = msg[2]
                if pin < 16:
                    hw_board.queue.put(msg)
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
        while self.running:
            self.hw_board.processOutgoing()
            self.hw_board.readDigital(self.queue)
            self.hw_board.readAnalog(self.queue)
            self._next_time += self._interval
            delay = self._next_time - time.time()
            if delay > 0.0:
                time.sleep(delay)

    def endApplication(self):
        self.running = 0
        
    def close_window(self):
        print( "Window closed")
        self.endApplication()

rand = random.Random(  )
root = tk.Tk(  )

client = ThreadedClient(root)
root.mainloop(  )