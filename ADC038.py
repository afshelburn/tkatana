#!/usr/bin/env python

import time
import threading
import pigpio

def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.
        
class SimpleADC:
    def __init__(self, pi, pin_cs=5, pin_clk=21, pin_di=20, pin_do=19):
        print("Simple ADC")
        self._pi = pi
        self._PIN_CS = pin_cs
        self._PIN_CLK = pin_clk
        self._PIN_DI = pin_di
        self._PIN_DO = pin_do
        
        #self._pi.set_mode(self._PIN_CS, pigpio.OUTPUT)
        #self._pi.set_mode(self._PIN_DO, pigpio.INPUT)
        #self._pi.set_mode(self._PIN_DI, pigpio.OUTPUT)
        #self._pi.set_mode(self._PIN_CLK, pigpio.OUTPUT)
        
    def clock(self):       
        self._pi.gpio_trigger(self._PIN_CLK, 2, 1)

    # read SPI data from ADC8038
    def getADC(self, channel):
    # 1. CS LOW.
        #self._pi.write(self._PIN_CLK, 1)
        self._pi.write(self._PIN_CS, 1)
        self._pi.write(self._PIN_CS, 0)
        #self.clock()
    # 2. Start clock
        self._pi.write(self._PIN_CLK, 0)
        
    # 3. Input MUX address
        cmd = [1, 1, channel & 1, (channel & 2) >> 1, (channel & 4) >> 2]
        #print("Address word:" + str(cmd))
        for i in cmd: # start bit + mux assignment
            if (i == 1):
                self._pi.write(self._PIN_DI,1)
            else:
                self._pi.write(self._PIN_DI,0)
            self.clock()
            
    # 4. read 8 ADC bits
        ad = 0
        for i in range(8):
            self.clock()
            ad <<= 1 # shift bit
            if self._pi.read(self._PIN_DO):
                ad |= 0x1 # set first bit

    # 5. reset
        self._pi.write(self._PIN_CS, 1)
        self._pi.write(self._PIN_DI,0)
        self.clock()
        self.clock()
        self.clock()

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
        pi.write(26, 1)
        pi.write(adc._PIN_CS, 1)
        print("Getting value")
        #for i in range(8):
        val = adc.getADC(0)
        #if i == 0:
        print("Ch " + str(0) + ":" + str(val))
        time.sleep(0.01)
            
    time.sleep(13)

#    adc.cancel()
    pi.stop()
