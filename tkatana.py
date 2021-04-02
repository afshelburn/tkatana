import tkinter as tk

from tkinter import *
import tkinter.font as tkFont

import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox

from itertools import cycle
import time
import katana
import pigpio
import PatchData
import center_tk_window as centerTK
import json
from PatchData import *
import threading
import random
import queue
import math
import json
import librarian

root = tk.Tk()

root.attributes('-zoomed',True)

logging = True

def log(msg, level=0):
    if logging:
        if level > 0:
            print(msg)

bh = 42
bw = 56

mainFont = tkFont.nametofont("TkDefaultFont")
bigFont = tkFont.Font(family="Helvetica", weight="bold", size=60)

on_image = tk.PhotoImage(width=bw, height=bh)
off_image = tk.PhotoImage(width=bw, height=bh)
on_image.put(("magenta",), to=(0, 0, bw-1, bh-1))
off_image.put(("gray",), to=(0, 0, bw-1, bh-1))

editors = {}

customFont = tkFont.Font(family="Helvetica", size=7)

adc_knob_count = 6
adc_exp_pedal = 22

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
        self._adc_value = [-1]*self._adc_channels
        
        self._blink_last = time.time()
        self._blink_period = 1
        self._blink_fraction = [1]*8*self._chips
        
        self._adc_map = [16,17,20,19,18,21,22,23]
        
        self._adc_commands = []
        
        self._adc_active_channels = {}
        
        self.filter_constant = [0.6]*self._adc_channels
        self.filter_constant[6] = 0.75 #let expression pedal have higher sensitivity
        self.filter_constant[7] = 0.0 #disable this pin
        
        for i in range(8):
            cmd = [1, 1, i & 1, (i & 2) >> 1, (i & 4) >> 2]
            self._adc_commands.append(cmd)        
        
        self.queue = queue.Queue()
        
    def stop(self):
        self._pi.stop()
        
    def processOutgoing(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                
                if isinstance(msg, tuple):
                    # Check contents of message and do whatever is needed.
                    pin = msg[0]
                    val = msg[1]
                    log("process outgoing")
                    log("pin " + str(pin) + " value = " + str(val))
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
            #log("bit " + str(i) + " = " + str(inval))
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
        for adc in self._adc_active_channels:
            i = self._adc_map[adc-16]
            new_adc = self.getADC(i-16)
            
            if self._adc_value[i-16] < 0:
                self._adc_value[i-16] = new_adc
            else:
                new_adc = int(0.5+self.filter_constant[i-16]*new_adc + (1.0-self.filter_constant[i-16])*self._adc_value[i-16])
            
            #log("adc " + str(i) + " = " + str(new_adc[i]))
            if abs(new_adc - self._adc_value[i-16]) > sensitivity:
                event = (self, adc, new_adc, read_time)
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
        #log("Address word:" + str(cmd))
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
        
def destroyObj(obj):
    #log("Destroy object")
    obj.destroy()
        
def bigMessage(text, seconds):
    frm = tk.Frame(root)#, width=400, height=200)
    frm.grid(row=0,column=0,rowspan=3,columnspan=5)
    #bigFont.configure(size=100)
    label = tk.Label(frm, text=text, font=bigFont)
    label.grid(row=0,column=0,sticky="nsew")
    frm.after(int(seconds*1000), lambda: destroyObj(frm))

def channelAddress(base, ch):
    return (chAddr[ch][0], chAddr[ch][1], base[2], base[3])

def tempAddress(base):
    return (0x60, 0x00, base[2], base[3])

class EffectPanel:
    def __init__(self, katana, app, title, toggle_addr, color_addr, color_assign, effect_addr, level_addr, effects, hw_button, effectsSettings, parent):
        
        self.katana = katana
        self.app = app
        
        self.colors = ["Green", "Red", "Orange"]
        self.color = tk.IntVar(name=title + ".color",  value=0)
        #self.level = tk.IntVar(name=title + ".level",  value=0)
        self.toggle = tk.IntVar(name=title + ".toggle",  value=0)
        self.label = tk.StringVar(name=title + ".label", value=title)
        self.base_title = title
        
        self.labelWidget = Label(None, textvariable=self.label)
        self.title_frame = tk.LabelFrame(parent, labelwidget=self.labelWidget, padx=10, pady=5)
        
        self.green_button = tk.Radiobutton(self.title_frame, text="G", variable=self.color, indicatoron=False, value=0, width=4, fg="green")
        self.red_button = tk.Radiobutton(self.title_frame, text="R", variable=self.color, indicatoron=False, value=1, width=4, fg="red")
        self.orange_button = tk.Radiobutton(self.title_frame, text="O", variable=self.color, indicatoron=False, value=2, width=4, fg="orange")
        self.edit_button = tk.Button(self.title_frame, text="E", command=self.edit)
        
        self.edit_button.grid(row=4, columnspan=1, column=0)
        
        self.write_button = tk.Button(self.title_frame, text="W", command=self.write)
        
        self.write_button.grid(row=4, columnspan=1, column=2)

        #self.level_slider = Scale(self.title_frame, variable=self.level, from_=level_addr[1], to=level_addr[2], orient="horizontal", length=50)
        #self.level_addr = level_addr
        
        self.toggle_button = Checkbutton(self.title_frame, image=off_image, selectimage=on_image, indicatoron=False, onvalue=1, offvalue=0, variable=self.toggle)
        
        self.green_button.grid(row=0, column=0)
        self.red_button.grid(row=0, column=1)
        self.orange_button.grid(row=0, column=2)
        
        #self.level_slider.grid(row=2, column=0, columnspan=3, sticky=W+E)

        self.toggle_button.grid(row=3, column=0, sticky=N+W+S+E, columnspan=3)
        
        self.effectCycle = [cycle(effects.items()), cycle(effects.items()), cycle(effects.items())]
        self.effectMap = effects
        
        self.toggle_addr = toggle_addr
        self.color_addr = color_addr
        self.color_assign_addr = color_assign
        self.effect_addr = effect_addr
        
        self.color_trace = self.color.trace('w', self.changeColor)
        self.toggle_trace = self.toggle.trace('w', self.toggleState)
        #self.level_trace = self.level.trace('w', self.levelChanged)
        
        self.hw_button = hw_button
        self.effectsSettings = effectsSettings
        self.effectName = None
        self.effectIndex = None

            
    def edit(self, *args):
        log("Editing " + self.base_title)
        log(self.effectName)
        if self.effectName in self.effectsSettings:
            #log(str(self.effectsSettings[self.effectName]))
            key = self.base_title + "." + self.effectName
            for e in editors:
                editors[e][0].hide()
                    
            if key in editors:
                editors[key][0].read()
                self.app.subscribe(range(16,16+adc_knob_count), editors[key][0].knob_moved)
                editors[key][0].show()
            else:
                frm = tk.Toplevel(root, width=480, height=320)
                editors[key] = (EffectEditor(frm, self.katana, self.app, self.effectName, self.effectsSettings[self.effectName]), frm)
                editors[key][0].read()
                self.app.subscribe(range(16,16+adc_knob_count), editors[key][0].knob_moved)
                centerTK.center(root, frm)
                
    def write(self, *args):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        log("Write to channel " + str(ch))
        log("Writing " + self.base_title)
        log(self.effectName)
        if self.effectName in self.effectsSettings:
            for setting in self.effectsSettings[self.effectName]:
                addr = setting[5]
                sz = setting[6]
                #log(setting[0] + "->" + str(addr))
                addrNew = channelAddress(addr, ch)
                tmpVal = self.katana.query_sysex_int(addr, sz)
                curVal = self.katana.query_sysex_int(addrNew, sz)
                #log("Writing " + str(tmpVal) + " over " + str(curVal))
                if not tmpVal == curVal:
                    #log(str(setting))
                    #log("Writing " + str(tmpVal) + " over " + str(curVal))
                    self.katana.send_sysex_int(addrNew, tmpVal, sz)
                    
        tgl = self.toggle.get()
        ch_tgl_addr = channelAddress(self.toggle_addr, ch)
        self.katana.send_sysex_data(ch_tgl_addr, (tgl,))
        
        ch_assign_clr_addr = channelAddress(self.color_assign_addr, ch)
        
        clr = self.katana.query_sysex_byte(self.color_addr)
        
        ch_clr_addr = channelAddress(self.color_addr, ch)
        
        self.katana.send_sysex_data(ch_clr_addr, (self.color.get(),))
        
        log("Assigning effect " + str(self.effectIndex) + " to color " + str(clr))

        self.katana.assign_effect(ch_assign_clr_addr, clr, self.effectIndex)

        self.katana.send_sysex_data(channelAddress(self.effect_addr, ch), (self.effectIndex,))
        
        amp = self.katana.query_sysex_byte(QUERY_AMP)
        log("Writing amp " + str(amp) + " to patch")
        self.katana.send_sysex_data(channelAddress(QUERY_AMP,ch),(amp,))
        
    def nextEffect(self):
        log(str(self.color.get()))
        log("Selecting next effect for " + self.colors[self.color.get()] + ": " + self.label.get())
        val = next(self.effectCycle[self.color.get()])
        if self.katana is None:
            return
        self.katana.assign_effect(self.color_assign_addr, self.color.get(), val[0])
        self.label.set(self.base_title + ": " + val[1])
        self.effectName = val[1]
        self.effectIndex = val[0]
        bigMessage(self.effectName, 1)
        
    def changeColor(self, *args):
        self.katana.send_sysex_data(self.color_addr, (self.color.get(),))
        self.readEffect()
        bigMessage(self.colors[self.color.get()] + ": " + self.effectName, 1.5)
        
    def levelChanged(self, *args):
        log("Level changed")
        #lvl = self.level_slider.get()
        #log(self.label.get() + " level changed to " + str(lvl))
        #self.katana.send_sysex_data(self.level_addr[0], (lvl,))
        
    def toggleState(self, *args):
        self.katana.send_sysex_data(self.toggle_addr, (self.toggle.get(),))
        self.app.sendOutput(self.hw_button, self.toggle.get())
        state = ": off"
        if self.toggle.get():
            state = ": on"
        bigMessage(self.effectName + state, 1.5)
    
    def readEffect(self):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        log("Read from channel " + str(ch))
        log("Color selected is " + str(self.color.get()) + " should be " + str(self.katana.query_sysex_byte(self.color_addr)))
        res = self.katana.query_sysex_byte(self.color_assign_addr, self.color.get())
        log("Setting " + self.label.get() + " effect state to " + str(self.effectMap[res]))
        val = next(self.effectCycle[self.color.get()])
        while val[0] != res:
            val = next(self.effectCycle[self.color.get()])
        self.label.set(self.base_title + ": " + val[1])
        self.effectName = val[1]
        self.effectIndex = val[0]
        self.label.set(self.base_title + ": " + val[1])

        
    def readToggle(self):
        res = self.katana.query_sysex_byte(self.toggle_addr)
        #log("Setting " + self.label.get() + " toggle state to " + str(res))
        self.toggle.trace_vdelete('w', self.toggle_trace)
        self.toggle.set(res)
        self.toggle_trace = self.toggle.trace('w', self.toggleState)
        self.app.sendOutput(self.hw_button, self.toggle.get())
        
    def readColor(self):
        res = self.katana.query_sysex_byte(self.color_addr)
        #log("Setting " + self.label.get() + " color state to " + str(self.colors[res]))
        self.color.trace_vdelete('w', self.color_trace)
        self.color.set(res)
        self.color_trace = self.color.trace('w', self.changeColor)
        
    def read(self):
        if self.katana is None:
            return
        log("Reading state for " + self.label.get())
        self.readColor()
        self.readEffect()
        self.readToggle()
        
        
class ChannelButton:
    channel = tk.IntVar(name="Channel", value=0)

    def __init__(self, katana, title, value, parent):
        #self.var = ChannelButton.var
        self.katana = katana
        self.value = value
        self.text = StringVar(name=title + ".text", value=title)
        self.labelWidget = Label(None, textvariable=self.text)
        self.title_frame = tk.LabelFrame(parent, labelwidget=self.labelWidget, padx=10, pady=5)
        self.radio_button = tk.Radiobutton(self.title_frame, image=off_image, selectimage=on_image, indicatoron=False, value=value, variable=ChannelButton.channel)
        self.radio_button.grid(row=0, column=0, sticky=N+W+S+E)
        #ChannelButton.var.trace('w', ChannelButton.stateChanged)

class ToggleButton:
    def __init__(self, katana, app, title, hw_button, parent):
        self.katana = katana
        self.toggle = IntVar(name=title + ".toggle", value=0)
        self.text = StringVar(name=title + ".text", value=title)
        self.labelWidget = Label(None, textvariable=self.text)
        self.title_frame = tk.LabelFrame(parent, labelwidget=self.labelWidget, padx=10, pady=5)
        self.toggle_button = tk.Checkbutton(self.title_frame, image=off_image, selectimage=on_image, indicatoron=False, variable=self.toggle)
        self.toggle_button.grid(row=1, column=0, sticky=N+W+S+E, columnspan=3)
        self.toggle_trace = self.toggle.trace('w', self.stateChanged)
        self.app = app
        self.hw_button = hw_button
        
    def stateChanged(self, *args):
        log(self.text.get() + " changed to " + str(self.toggle.get()))
        self.app.sendOutput(self.hw_button, self.toggle.get())
        #state = ": off"
        #if self.toggle.get():
        #    state = ": on"
        #bigMessage(self.text.get() + state, 1.5)
        
class MomentaryButton:
    def __init__(self, katana, title, command, parent):
        self.katana = katana
        self.base_title = title
        self.text = StringVar(name=title + ".text", value=title)
        self.labelWidget = Label(None, textvariable=self.text)
        self.title_frame = tk.LabelFrame(parent, labelwidget=self.labelWidget, padx=10, pady=5)
        self.toggle_button = tk.Button(self.title_frame, image=off_image, command=command)
        self.toggle_button.grid(row=0, column=0, sticky=N+W+S+E) 
       
class RingSelector(MomentaryButton):
    def __init__(self, katana, title, addr, selectionPool, parent):
        super().__init__(katana, title, self.nextItem, parent)
        self.katana = katana
        self.selectionPool = selectionPool
        self.currentSelection = next(selectionPool)
        self.addr = addr
        
    def nextItem(self):
        newVal = next(self.selectionPool)
        self.currentSelection = newVal
        self.text.set(self.base_title + ": " + str(newVal[1]))
        self.katana.send_sysex_data(self.addr, (newVal[0],))
        log(str(newVal))
        bigMessage(str(newVal[1]), 1.5)
        
    def get(self):
        return self.currentSelection
        
    def setSelection(self, selection):
        val = next(self.selectionPool)
        #log("Selection: " + str(selection))
        while val != selection:
            val = next(self.selectionPool)
            #log(str(val))
        log("Selected " + str(val))
        self.text.set(self.base_title + ": " + selection[1])
        
class EffectSelector(MomentaryButton):
    def __init__(self, katana, title, effectPanels, parent):
        super().__init__(katana, title, self.nextItem, parent)
        self.katana = katana
        self.effectPanels = effectPanels
        
    def nextItem(self):
        log(self.text.get())
        activePanel = None
        for panel in self.effectPanels:
            if panel.toggle.get() == 1:
                activePanel = panel
                break
                
        if activePanel is not None:
            activePanel.nextEffect()

class EQToggle(ToggleButton):
    def __init__(self, katana, app, title, hw_button, parent):
        super().__init__(katana, app, title, hw_button, parent)
        self.eq_type = tk.IntVar(name="eq.type", value=0)
        self.peq_button = tk.Radiobutton(self.title_frame, text="P-Eq", variable=self.eq_type, indicatoron=False, value=0, width=4)
        self.geq_button = tk.Radiobutton(self.title_frame, text="G-Eq", variable=self.eq_type, indicatoron=False, value=1, width=4)
        self.edit_button = tk.Button(self.title_frame, text="E", command=self.editEQ, width=4)
        self.write_button = tk.Button(self.title_frame, text="W", command=self.writeEQ, width=4)
        self.peq_button.grid(row=0,column=0)
        self.geq_button.grid(row=0,column=2)
        self.edit_button.grid(row=2,column=0)
        self.write_button.grid(row=2,column=2)
        #self.toggle_button.grid(row=2,column=0,columnspan=3)
        
        self.peq_frame = tk.Toplevel(root, width=480, height=320)
        self.peq = EQEditor(self.katana, app, "P-EQ", ParametricEQ, ChParametricEQ, self.peq_frame)

        self.geq_frame = tk.Toplevel(root, width=480, height=320)
        self.geq = EQEditor(self.katana, app, "G-EQ", GraphicEQ, ChGraphicEQ, self.geq_frame)
        
        self.geq_frame.withdraw()
        self.peq_frame.withdraw()
        
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
    def selectEQ(self, *args):
        log("EQ state changed: " + str(args))
        self.eq_type.trace_vdelete('w', self.eq_type_trace)
        val = self.eq_type.get()
        self.katana.send_sysex_data(CHANNEL_EQ_TYPE, (val,))
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
    def editEQ(self):
        log("Edit EQ")
        if self.eq_type.get() == 0:
            self.peq_frame.deiconify()
            self.peq_frame.attributes("-topmost", True)
            self.peq.setActiveColors()
            centerTK.center(root, self.peq_frame)
            self.app.subscribe(range(16,16+adc_knob_count), self.peq.knob_moved)
        else:
            self.geq_frame.deiconify()
            self.geq_frame.attributes("-topmost", True)
            self.geq.setActiveColors()
            centerTK.center(root, self.geq_frame)
            self.app.subscribe(range(16,16+adc_knob_count), self.geq.knob_moved)            

    def stopEditing(self):
        if self.peq_frame.state() == 'normal':
            self.peq_frame.withdraw()
            self.app.unsubscribe(range(16,16+adc_knob_count), self.peq.knob_moved)
        if self.geq_frame.state() == 'normal':
            self.geq_frame.withdraw()
            self.app.unsubscribe(range(16,16+adc_knob_count), self.geq.knob_moved)
            
    def isEditing(self):
        if self.peq_frame.state() == 'normal':
            return True
        if self.geq_frame.state() == 'normal':
            return True
        return False
        
    def writeEQ(self):
        log("Write EQ")
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        log("Writing EQ data to channel " + str(ch))
        self.katana.send_sysex_data(channelAddress(CHANNEL_EQ_TYPE, ch), (self.eq_type.get(),))
        self.katana.send_sysex_data(channelAddress(CHANNEL_EQ_SW, ch), (self.toggle.get(),))
        if self.eq_type.get() == 0:
            self.peq.write()
        else:
            self.geq.write()
        
    def read(self):
        self.peq.read()
        self.geq.read()
        eq_type = self.katana.query_sysex_byte(CHANNEL_EQ_TYPE)
        log("EQ Type is " + str(eq_type))
        self.eq_type.trace_vdelete('w', self.eq_type_trace)
        self.eq_type.set(eq_type)
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
class EQEditor:
    def __init__(self, katana, app, title, levelInfo, chLevelInfo, parent):
        
        self.katana = katana
        
        self.app = app

        self.title_frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        
        self.parent = parent

        self.levels = []
        self.params = []
 
        #there are more parameters to edit than knobs, so let the last knob select
        #  between which bank the other knobs edit
        self.knob_offset = 0
        
        col = 0
        maxCol = 6
        i = 0
        #levelInfo = {"30Hz":(0,-24,24),"60Hz":(0,-24,24)...}
        for level in levelInfo:
            l = tk.IntVar(name=title + "." + level + ".level",  value=levelInfo[level][1])
            o = "vertical"
            row = 0 #int(i / maxCol)
            i = i + 1
            columnspan = 1
            self.params.append(level)
            slider = Scale(self.title_frame, variable=l, from_=levelInfo[level][3], to=levelInfo[level][2], orient=o, length=100)
            slider.grid(row=row,column=col,columnspan=columnspan)
            label = Label(self.title_frame, text=level, anchor="center", padx=2, font=customFont)
            label.grid(row=(row+1),column=col,columnspan=columnspan)
            col = col + 1
            trace_level = l.trace('w', self.stateChanged)
            self.levels.append([l,slider,trace_level,chLevelInfo[level][4],levelInfo[level][0], levelInfo[level][1], chLevelInfo[level][4], levelInfo[level][2], levelInfo[level][3]])
            
        self.title_frame.grid(row=0,column=0)
            
        self.reset = tk.Button(self.title_frame, text="Reset", command=self.reset)
        self.reset.grid(row = 2, column = 0)
        
        self.close = tk.Button(self.title_frame, text="Close", command=self.hide)
        self.close.grid(row = 2, column = len(levelInfo)-1)
        
        self.activeEditor = None
        
    def reset(self):
        log("Reset")
        for level in self.levels:
            level[1].set(level[5])
            #self.katana.send_sysex_data(addr, (level[5],))
            
    def write(self):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        log("Writing EQ data to channel " + str(ch))
        for level in self.levels:
            #log("Writing value = " + str(level[0].get()+level[4]))
            self.katana.send_sysex_data(channelAddress(level[6], ch), (level[0].get()+level[4],))
            #val = self.katana.query_sysex_byte(channelAddress(level[6], ch))
            #log("Read channel value = " + str(val))
            #val = self.katana.query_sysex_byte(level[6])
            #log("Read immediate value = " + str(val))
            #level[1].set(level[5])
            
    def hide(self):
        log("Close")
        self.parent.withdraw()
        self.app.unsubscribe(range(16,16+adc_knob_count), self.knob_moved)
        
    def show(self):
        log("Showing")
        self.parent.deiconify()
        self.app.subscribe(range(16,16+adc_knob_count), self.knob_moved)
        
    def edit(self):
        log("Edit")
        self.read()
        self.parent.deiconify()
        self.parent.attributes("-topmost", True)
        self.setActiveColors()
        centerTK.center(root, self.parent)
        self.app.subscribe(range(16,16+adc_knob_count), self.knob_moved)        
        
    def stopEditing(self):
        if self.parent.state() == 'normal':
            self.parent.withdraw()
            self.app.unsubscribe(range(16,16+adc_knob_count), self.knob_moved)
            
    def isEditing(self):
        if self.parent.state() == 'normal':
            return True
        return False        
            
    def stateChanged(self, *args):
        log("Eq state changed")
        for level in self.levels:
            if level[0]._name == args[0]:
                addr = level[3]
                #log(str(addr))
                val = level[0].get()
                #log("Updating " + level[0]._name + " to value " + str(val))
                self.katana.send_sysex_data(addr, (val+level[4],))
        
    def read(self):
        log("Reading Eq state", 1)
        for level in self.levels:
            addr = level[3]
            #log(str(addr))
            val = self.katana.query_sysex_byte(addr)
            log("Updating " + level[0]._name + " to value " + str(val), 0)
            level[0].trace_vdelete('w', level[2])
            level[0].set(val - level[4])
            level[2] = level[0].trace('w', self.stateChanged)
            
    def setActiveColors(self):
        start = self.knob_offset
        end = start + adc_knob_count - 1
        for i in range(len(self.levels)):
            if i >= start and i < end:
                self.levels[i][1].configure(fg='red')
            else:
                self.levels[i][1].configure(fg='black')
                
    def knob_moved(self, msg):
        pin = msg[0]
        level = msg[1]
        tick = msg[2]
        
        #if the last knob moves set the knob offset
        if pin == 16 + adc_knob_count - 1:
            #if level > 127:
            #    self.knob_offset = 5
            #else:
            #    self.knob_offset = 0
            self.knob_offset = int(level / 30)    
            self.setActiveColors()
            return
                
        index = pin - 16 + self.knob_offset
        log("index = " + str(index))
        if index >= len(self.levels):
            return
        #map the value to the setting's range
        frac = float(level)/255.0
        setting = self.levels[index]
        var = setting[0]
        low = float(setting[7])
        hi = float(setting[8])
        newVal = low + frac*(hi-low)
        log("knob " + str(index) + " adjusted, value = " + str(newVal))
        var.set(int(newVal))
        setting[1].configure(fg='red')
        
class DragDropListbox(tk.Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """
    def __init__(self, master, callback, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None
        self.callback = callback

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)
        self.callback()

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i+1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i-1, x)
            self.curIndex = i
        self.callback()
        
class ChainEditor:
    def __init__(self, parent, katana, app, title):
        self.katana = katana
        self.app = app
        self.parent = parent
        self.frame = tk.Toplevel(parent, width=200, height=450)
        self.title_frame = tk.LabelFrame(self.frame, text=title, padx=10, pady=5)
        self.title_frame.grid(row=0,column=0)
        self.list = DragDropListbox(self.title_frame, self.write, height=11)
        items = ["one", "two", "three"]
        self.list.insert(0, *items)
        
        self.read()
        self.list.grid(row=0,column=0)
        #self.list.pack()
        self.hide()
        self.lastChain = []
        
        close = tk.Button(self.frame, text="Close", command=self.hide)
        close.grid(row=1, column=0)
        
    def hide(self):
        log("Closing")
        self.frame.withdraw()
        
    def show(self):
        log("Showing")
        self.frame.deiconify()
        centerTK.center(self.parent, self.frame)
        
    def read(self):
        log("reading chain")
        addr = QUERY_EFFECT_CHAIN
        items = []#"one", "two", "three", "four", "five"]
        chain = self.katana.query_sysex_data(addr, len=20)
        log("done reading " + str(chain))
        for data in chain[1]:
            log(str(data), 0)
            for k in data:
                if k in EFFECT_CHAIN_LABEL:
                    print(EFFECT_CHAIN_LABEL[k])
                    items.append(EFFECT_CHAIN_LABEL[k])
            
        #print(self.katana.query_sysex_byte(addr))
            
        if self.list.size() > 0:
            self.list.delete(0, tk.END)
    
        self.list.insert(0, *items)
        
        self.lastChain = items.copy()
        
        
    def write(self):
        
        newChain = []
        for i in range(len(EFFECT_CHAIN)):
            newChain.append(self.list.get(i))
        
        if newChain == self.lastChain:
            log("no change", 0)
            return
        
        log("last chain: " + str(self.lastChain), 0)
        log("new chain: " + str(newChain), 1)
        self.lastChain = newChain.copy()
        log("writing chain", 0)
        data = []
        for i in range(len(EFFECT_CHAIN_PRE)):
            data.append(EFFECT_CHAIN_PRE[i])
            
        for i in range(len(newChain)):
            data.append(EFFECT_CHAIN[newChain[i]])
            
        for i in range(len(EFFECT_CHAIN_POST)):
            data.append(EFFECT_CHAIN_POST[i])
            
        log("new chain data: " + str(data), 0)
        self.katana.send_sysex_data(QUERY_EFFECT_CHAIN, tuple(data))
        log("new chain set", 1)

class EffectEditor:
    def __init__(self, parent, katana, app, title, settings):
        self.katana = katana
        
        self.app = app
        
        self.title_frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        
        self.parent = parent
        
        #('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x02))
        
        self.settings = settings.copy()
        col = 0
        
        #there are more parameters to edit than knobs, so let the last knob select
        #  between which bank the other knobs edit
        self.knob_offset = 0
        self.sliders = []
        self.trace = {}
        #('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x02))
        for setting in self.settings:
            #log(str(setting))
            l = tk.IntVar(name=title + "." + setting[0] + ".level",  value=setting[2])
            o = "vertical"
            row = 0
            columnspan = 1
            slider = Scale(self.title_frame, variable=l, from_=setting[4], to=setting[3], orient=o, length=100)
            slider.grid(row=row,column=col,columnspan=columnspan)
            label = Label(self.title_frame, text=setting[0], anchor="center", padx=4)
            label.grid(row=(row+1),column=col,columnspan=columnspan)
            self.trace[col] = (l.trace('w', self.stateChanged), l)
            col = col + 1
            self.sliders.append(slider)
            
        self.reset = tk.Button(self.title_frame, text="Reset", command=self.reset)
        self.reset.grid(row = row + 2, column = 0)
        
        self.close = tk.Button(self.title_frame, text="Close", command=self.hide)
        self.close.grid(row = row + 2, column = len(settings)-1)
            
        self.title_frame.grid(row=0,column=0)
        
        self.setActiveColors()
        
    def setActiveColors(self):
        start = self.knob_offset
        if len(self.sliders) <= adc_knob_count:
            for slider in self.sliders:
                slider.configure(fg='black')
            return
        end = start + adc_knob_count - 1
        for i in range(len(self.sliders)):
            if i >= start and i < end:
                self.sliders[i].configure(fg='red')
            else:
                self.sliders[i].configure(fg='black')        
        
    def knob_moved(self, msg):
        pin = msg[0]
        level = msg[1]
        tick = msg[2]
        log("knob " + str(pin) + " moved")
        if len(self.sliders) > adc_knob_count:
            #if the last knob moves set the knob offset
            if pin == 16 + adc_knob_count - 1:
                #if level > 127:
                #    self.knob_offset = 5
                #else:
                #    self.knob_offset = 0
                self.knob_offset = int(level / 30)    
                self.setActiveColors()
                return        
        
        index = pin - 16 + self.knob_offset
        log("index = " + str(index))
        if index >= len(self.settings):
            return
        #map the value to the setting's range
        frac = float(level)/255.0
        setting = self.settings[index]
        var = self.trace[index][1]
        low = float(setting[3])
        hi = float(setting[4])

        newVal = low + frac*(hi-low)
        if hi - low == 1:
            newVal = math.floor(newVal+0.5)
        log("knob " + str(index) + " adjusted, value = " + str(newVal))
        var.set(int(newVal))
    
    def reset(self):
        log("Reset")
        for i in range(0, len(self.settings)):
            var = self.trace[i][1]
            setting = self.settings[i]
            var.set(setting[2])
            
    def hide(self):
        log("Closing")
        self.app.unsubscribe(range(16,16+adc_knob_count), self.knob_moved)
        self.parent.withdraw()
        #self.parent.destroy()
        
    def show(self):
        log("Showing")
        self.parent.deiconify()
        
    def isShowing(self):
        return self.parent.state() == 'normal'
        
    def stateChanged(self, *args):
        #log(str(args))
        #log(args[0] + " state changed")
        for i in range(0,len(self.settings)):
            var = self.trace[i][1]
            if var._name == args[0]:
                setting = self.settings[i]
                addr = setting[5]
                sz = setting[6]
                val = var.get() + setting[1]
                #log(str(setting))
                #log("val = " + str(val))
                #log("sz = " + str(sz))
                self.katana.send_sysex_int(addr, val, sz)
                break

    def read(self):
        i = 0
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        log("Reading effect from channel " + str(ch))
        for setting in self.settings:
            addr = setting[5]
            sz = setting[6]
            #log("Setting:" + str(setting))
            #addrNew = (chOffset[0], chOffset[1], addr[2], addr[3])
            #log(str(addr))
            val = self.katana.query_sysex_int(addr, sz) - setting[1]
            var = self.trace[i][1]
            trace_id = self.trace[i][0]
            var.trace_vdelete('w', trace_id)
            var.set(val)
            trace_id = var.trace('w', self.stateChanged)
            self.trace[i] = (trace_id, var)
            i = i + 1
    
class PedalEditor:
    def __init__(self, katana, title, pedal_options, initial_value, parent):
        
        self.katana = katana

        self.title_frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        
        self.parent = parent

        self.pedal_option = tk.StringVar(name=title + ".option", value=initial_value)
        
        self.pedal_options = pedal_options

        buttons = []
        for item in pedal_options:
            button = tk.Radiobutton(self.title_frame, text=item, variable=self.pedal_option, indicatoron=False, value=item)
            button.grid(row=0,column=len(buttons))
            buttons.append(button)
            
        self.close = tk.Button(self.title_frame, text="Close", command=self.hide)
        self.close.grid(row = 1, column = len(buttons)-1)
        
        self.title_frame.grid(row=0,column=0)
        
        self.pedal_option.trace('w', self.set_pedal_map)
        
    def hide(self):
        log("Closing")
        self.parent.withdraw()
        
    def show(self):
        log("Showing")
        self.parent.deiconify()
        
    def set_pedal_map(self,*args):
        log("Setting pedal map to " + self.pedal_option.get())

        
        
class KatanaApp:
    def __init__ (self, master, queue, hw_board, endCommand):
        self.queue = queue
        
        self.hw_board = hw_board
        # Set up the GUI
        # Add more GUI stuff here depending on your specific needs
        self.subscribers = {}
        
        self.katana = katana.Katana('KATANA MIDI 1',  0,  False)
        
        self.effects = []
        self.channels = []
        self.controls = []

        layout = ["Boost", "Mod", "FX", "Delay", "Reverb"]

        effect_map = {"Boost":BOOST_OPTIONS, "Mod":EFFECT_OPTIONS, "FX":EFFECT_OPTIONS, "Delay":DELAY_OPTIONS, "Reverb":REVERB_OPTIONS}
        self.effect_settings = {"Boost":PatchData.BOOST_SETTINGS, "Mod":PatchData.FX1_SETTINGS, "FX":PatchData.FX2_SETTINGS, "Delay":PatchData.DELAY_SETTINGS, "Reverb":PatchData.REVERB_SETTINGS}
        col = 0

        for item in layout:
            panel = EffectPanel(self.katana, self, item, TOGGLES[col], COLORS[col], COLOR_ASSIGN[col], EFFECTS[col], LEVELS[item], effect_map[item], HW_BUTTONS[col], self.effect_settings[item], root)
            panel.title_frame.grid(row=2, column=col*2, columnspan=2)
            if col == 0:
                channel = ChannelButton(self.katana, "Panel", col, root)
            else:
                channel = ChannelButton(self.katana, "Ch." + str(col), col, root)
            channel.title_frame.grid(row=1, column=col*2, columnspan=2)
            col = col + 1
            self.effects.append(panel)
            self.channels.append(channel)

        
        self.channel_trace = ChannelButton.channel.trace('w', self.channelStateChanged)
    
        self.mute = ToggleButton(self.katana, self, "Mute", MUTE_HW_BUTTON, root)
        self.mute.title_frame.grid(row=0, column=4*2, columnspan=2)
        self.mute_trace = self.mute.toggle.trace('w', self.muteStateChanged)

        self.ab = ToggleButton(self.katana, self, "A/B", AB_HW_BUTTON, root)
        self.ab.title_frame.grid(row=0, column=2*2, columnspan=2)
        self.ab_trace = self.ab.toggle.trace('w', self.abStateChanged)
        
        self.amp_frame = tk.Toplevel(root, width=480, height=320)
        self.amp_panel = EQEditor(self.katana, self, "Amp Panel", AmpPanel, ChAmpPanel, self.amp_frame)
        self.amp_frame.withdraw()
        
        ampShortList = []
        for i in AMP_LOOP_SHORT:
            #log(AMP_MAP[i])
            ampShortList.append((i, AMP_MAP[i]))
            #ampNameList.append(AMP_MAP[i])
            
        self.ampCycle = cycle(ampShortList)
        self.nextAmp = RingSelector(self.katana, "Amp", QUERY_AMP, self.ampCycle, root)
        self.nextAmp.title_frame.grid(row=0, column=0, columnspan=2)
        
        self.nextEffect = EffectSelector(self.katana, "Next Effect", self.effects, root)
        self.nextEffect.title_frame.grid(row=0, column=1*2, columnspan=2)
        
        self.eq_type = tk.IntVar(name="eq.type", value=0)
                
        self.eq = EQToggle(self.katana, self, "Eq", EQ_HW_BUTTON, root)
        self.eq.title_frame.grid(row=0,column=3*2, columnspan=2)
        self.eq_trace = self.eq.toggle.trace('w', self.eqStateChanged)
        
        self.controls.append(self.nextAmp)
        self.controls.append(self.nextEffect)
        self.controls.append(self.ab)
        self.controls.append(self.eq)
        self.controls.append(self.mute)
        
        self.closeButton = tk.Button(root, text="Close", command=endCommand)
        self.closeButton.grid(row=3,column=6)

        self.restoreButton = tk.Button(root, text="Restore", command=self.restoreFile)
        self.restoreButton.grid(row=3,column=1)

        self.saveButton = tk.Button(root, text="Backup", command=self.saveAll)
        self.saveButton.grid(row=3,column=2)
        
        self.saveChButton = tk.Button(root, text="Save Channel", command=self.saveCurrentChannel)
        self.saveChButton.grid(row=3,column=0)
        
        self.editPedalButton = tk.Button(root, text="Pedal 1", command=self.editPedal1)
        self.editPedalButton.grid(row=3,column=3)
        
        self.editChainButton = tk.Button(root, text="Chain", command=self.editChain)
        self.editChainButton.grid(row=3,column=4)
        
        self.editChainButton = tk.Button(root, text="TSL Loader", command=self.patchLoader)
        self.editChainButton.grid(row=3,column=5)
        
        self.selectedChannel = -1
        
        self.hwButtonPressTime = {}
        for i in range(16):
            self.hwButtonPressTime[i] = 0
            
        PEDAL_WAH_OPTION = [(FX_WAH_PEDAL,0,100),(MOD_WAH_PEDAL,0,100), (FX_EVH_WAH_PEDAL,0,100), (MOD_EVH_WAH_PEDAL,0,100)]
        PEDAL_VOLUME_OPTION = [(VOLUME_PEDAL,0,100)]
        PEDAL_DELAY_TIME_OPTION = [(DELAY_TIME_PEDAL,1,2000)]
        PEDAL_TREMOLO_RATE_OPTION = [(MOD_TREMOLO_PEDAL,0,100),(FX_TREMOLO_PEDAL,0,100)]
        PEDAL_FX_BLEND_OPTION = [(FX_BLEND_PEDAL,0,100)]
        PEDAL_FX_BEND_OPTION = [(FX_BEND_PEDAL,0,100)]
            
        self.pedal_options = {'Wah':PEDAL_WAH_OPTION,'Volume':PEDAL_VOLUME_OPTION,'Delay':PEDAL_DELAY_TIME_OPTION,'Tremolo':PEDAL_TREMOLO_RATE_OPTION,'FX Blend':PEDAL_FX_BLEND_OPTION,'FX Bend':PEDAL_FX_BEND_OPTION}
        self.pedal_map = {}
        
        self.pedal_vars = {}
        self.pedal_1_frame = tk.Toplevel(root, width=480, height=320)
        self.pedal_1_editor = PedalEditor(self.katana, "Pedal 1 Option", self.pedal_options, 'Wah', self.pedal_1_frame)
        self.pedal_vars[adc_exp_pedal] = (self.pedal_1_editor.pedal_option)

        self.pedal_1_frame.withdraw()
        
        self.chain_editor = ChainEditor(root, self.katana, self, 'Effect Chain')
        
        self.subscribe(range(16), self.hardware_button)
        
        self.subscribe([adc_exp_pedal], self.pedal_change)
                
        
    def editPedal1(self):
        log("Edit pedal 1")
        self.pedal_1_editor.show()      
    
    def editChain(self):
        log("Edit Effect Chain")
        self.chain_editor.read()
        self.chain_editor.show()
        
    def patchLoader(self):
        f = tk.Toplevel(root)
        l = librarian.Librarian(f)
        centerTK.center(root, f)
        l.setKatana(self.katana)
        l.loadDir('/home/pi/tsl_files')
    
    def saveCurrentChannel(self):
        
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        
        data = {}
        
        data["Channel"] = {}
        data["Channel"][ch] = {}
        data["Channel"][ch]["STATE"] = []
        data["Channel"][ch]["STATE"].append(('label', self.katana.get_patch_name_addr(ch), self.katana.get_patch_name(ch).strip(), 16))
        
        self.saveEffect("Boost", ch, data)
        self.saveEffect("Mod", ch, data)
        self.saveEffect("FX", ch, data)
        self.saveEffect("Delay", ch, data)
        self.saveEffect("Reverb", ch, data)
        self.saveEQ(ch, data)
        self.saveAmp(ch, data)
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = '/home/pi/channel_' + str(ch) + '_' + timestr + '.json'
        with open(f, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            
    def saveAll(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = '/home/pi/amp_settings' + '_' + timestr + '.json'
        data = {}
        for i in range(0,9):
            
            data["Channel"] = {}
            data["Channel"][i] = {}
            data["Channel"][i]["STATE"] = []
            data["Channel"][i]["STATE"].append(('label', self.katana.get_patch_name_addr(i), self.katana.get_patch_name(i).strip(), 16))
             
            self.saveEffect("Boost", i, data)
            self.saveEffect("Mod", i, data)
            self.saveEffect("FX", i, data)
            self.saveEffect("Delay", i, data)
            self.saveEffect("Reverb", i, data)
            self.saveEQ(i, data)
            self.saveAmp(i, data)
            
        with open(f, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            
    def saveEQ(self, ch, data):
        log("Saving EQ settings")
        #ParametricEQ = {'LOWCUT':(0, 0, 0, 17, (0x00, 0x00, 0x00, 0x13)),'L
        eqTypeAddr = channelAddress(CHANNEL_EQ_TYPE, ch)
        eqSwAddr = channelAddress(CHANNEL_EQ_SW, ch)
        data['EQ'] = {}
        data['EQ'][ch] = {}
        data['EQ'][ch]['STATE'] = []
        data['EQ'][ch]['STATE'].append(('toggle', eqSwAddr, self.katana.query_sysex_byte(eqSwAddr)))
        data['EQ'][ch]['STATE'].append(('type', eqTypeAddr, self.katana.query_sysex_byte(eqSwAddr)))
        data['EQ'][ch]['PEQ'] = []
        for setting in ChParametricEQ:
            chAddr = channelAddress(ChParametricEQ[setting][4], ch)
            val = self.katana.query_sysex_byte(chAddr)
            log(str(setting) + " = " + str(val))
            data['EQ'][ch]['PEQ'].append((setting, chAddr, val, 1))
        data['EQ'][ch]['GEQ'] = []
        for setting in ChGraphicEQ:
            chAddr = channelAddress(ChGraphicEQ[setting][4], ch)
            val = self.katana.query_sysex_byte(chAddr)
            log(str(setting) + " = " + str(val))
            data['EQ'][ch]['GEQ'].append((setting, chAddr, val, 1))
            
    def saveEffect(self, effectType, ch, data):
#         FX1_ADCOMP.append(('SUSTAIN', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x17)))
        effectsSettings = self.effect_settings[effectType]
        data[effectType] = {}
        log("Saving state for " + effectType)
        #for i in range(0,9):
        log("Reading " + effectType + " from channel " + str(ch))
        data[effectType][ch] = {}
        data[effectType][ch]['STATE'] = []
        toggle_addr = channelAddress(TOGGLE_MAP[effectType], ch)
        data[effectType][ch]['STATE'].append(('toggle', toggle_addr, self.katana.query_sysex_byte(toggle_addr), 1))
        color_addr = channelAddress(COLOR_MAP[effectType], ch)
        data[effectType][ch]['STATE'].append(('color', color_addr, self.katana.query_sysex_byte(color_addr), 1))
        
        #get current color assignments, and only store settings for those
        color_assign_addr = COLOR_ASSIGN_MAP[effectType]
        clr_assignments = self.katana.query_color_assignment(effectType)
        color_names = ['Green','Red','Orange']
        color_effect_names = []
        for i in range(3):
            addr = self.katana.effective_addr(color_assign_addr, i)
            addr = channelAddress(addr, ch)
            data[effectType][ch]['STATE'].append((color_names[i], addr, clr_assignments[i], 1))
            color_effect_names.append(EFFECT_INDEX_TO_NAME[effectType][clr_assignments[i]])
        
        log(str(color_effect_names))
        
        for effectName in color_effect_names:
            log("Reading " + effectName)
            list = effectsSettings[effectName]
            data[effectType][ch][effectName] = []
            for setting in list:
                #log("Reading " + str(setting))
                chAddr = channelAddress(setting[5], ch)
                val = self.katana.query_sysex_int(chAddr, setting[6])# - setting[1]
                #if val > -1 and val < 128:
                data[effectType][ch][effectName].append((setting[0], chAddr, val, setting[6]))
                #else:
                #    log("Failed to store value " + val + " for " + effectName + setting[0] + " = " + str(val))
        
    def saveAmp(self, ch, data):
        log("Saving Amp setting")
        #ParametricEQ = {'LOWCUT':(0, 0, 0, 17, (0x00, 0x00, 0x00, 0x13)),'L
        ampAddr = channelAddress(QUERY_AMP, ch)
        data['AMP'] = {}
        data['AMP'][ch] = {}
        data['AMP'][ch]['STATE'] = []
        data['AMP'][ch]['STATE'].append(('type', ampAddr, self.katana.query_sysex_byte(ampAddr), 1))
        data['AMP'][ch]['STATE'].append(('gain', AmpPanel['Gain'][4], self.katana.query_sysex_byte(AmpPanel['Gain'][4]), 1))
        data['AMP'][ch]['STATE'].append(('volume', AmpPanel['Volume'][4], self.katana.query_sysex_byte(AmpPanel['Volume'][4]), 1))
        data['AMP'][ch]['STATE'].append(('bass', AmpPanel['Bass'][4], self.katana.query_sysex_byte(AmpPanel['Bass'][4]), 1))
        data['AMP'][ch]['STATE'].append(('mid', AmpPanel['Mid'][4], self.katana.query_sysex_byte(AmpPanel['Mid'][4]), 1))
        data['AMP'][ch]['STATE'].append(('treble', AmpPanel['Treble'][4], self.katana.query_sysex_byte(AmpPanel['Treble'][4]), 1))
        data['AMP'][ch]['STATE'].append(('presence', AmpPanel['Presence'][4], self.katana.query_sysex_byte(AmpPanel['Presence'][4]), 1))
        #data['AMP'][ch]['STATE'].append(('bright', AmpPanel['Bright'][4], self.katana.query_sysex_byte(AmpPanel['Bright'][4]), 1))
        
    def restoreFile(self):
        filename = fdialog.askopenfilename(initialdir = "/home/pi",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename is not None:
            log(filename)
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                log("Restoring settings from file")
                answer = messagebox.askyesnocancel("Question", "Load into current channel?")
                if answer is None:
                    return
                if answer:
                    d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
                    ch = d[1][0][1]
                    self.restore(data, ch)
                else:
                    self.restore(data)
                    
                #self.katana.set_patch_name(1,'test')
                log("Reading amp settings into UI")
            
            self.read()
        
    
    def restore(self, data, targetCh=-1):
        log("Restoring data", 1)
        
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        curr_ch = d[1][0][1]
        
        if targetCh > -1 and targetCh != curr_ch:
            ChannelButton.channel.set(targetCh)
        
        for item in data:
            for ch in data[item]:
                for group in data[item][ch]:
                    log("Restoring " + group)
                    for setting in data[item][ch][group]:
                        addr = setting[1]
                        log(str(setting))
                        ich = int(ch)
                        log(setting[0] + " -> " + str(setting[2]) + " @" + str(addr) + " for ch " + str(ich) + "/" + str(curr_ch))
                        tmpAddr = None
                        tmpCh = ich
                        if targetCh > -1:
                            tmpCh = targetCh
                            addr = channelAddress(setting[1], targetCh)
                            tmpAddr = tempAddress(setting[1])
                        elif ich == curr_ch:
                            addr = channelAddress(setting[1], ich)
                            tmpAddr = tempAddress(setting[1])
                        else:
                            addr = channelAddress(setting[1], ich)
                            #tmpAddr = tempAddress(setting[1])
                                                   
                        val = setting[2]
                        if len(setting) > 3:
                            if setting[3] == 2:
                                self.katana.send_sysex_int(addr, val, setting[3])
                                if tmpAddr is not None:
                                    self.katana.send_sysex_int(tmpAddr, val, setting[3])
                            if setting[3] > 2:#only thing > 2 is patch name
                                self.katana.set_patch_name(tmpCh, val)
                                    
                        else:
                            self.katana.send_sysex_int(addr, val, 1)
                            if tmpAddr is not None:
                                self.katana.send_sysex_int(tmpAddr, val, 1)

    def pedal_change(self, msg):
        channel = msg[0]
        value = msg[1]
        read_time = msg[2]
        log("pedal value changed: " + str(value))
        if not channel in self.pedal_vars:
            log(str(channel) + " not associated with pedal")
            return
        pedal_var = self.pedal_vars[channel]
        #log(pedal_var.get() + " changed, raw value = " + str(value))
        settings = self.pedal_options[pedal_var.get()] # a list of (address, min, max)
        for setting in settings:
            minVal = float(setting[1])
            maxVal = float(setting[2])
            mapVal = int(minVal + int(float(value) / 255.0 * maxVal))
            #log("Setting value = " + str(mapVal))
            sz = 1
            if maxVal > 127:
                sz = 2
            self.katana.send_sysex_int(setting[0], mapVal, sz)     
        
    def hardware_button(self, msg): #piso, btn, val, read_time):
        btn = msg[0]
        val = msg[1]
        read_time = msg[2]
        
        if val == 0:
            elapsed = read_time - self.hwButtonPressTime[btn]
        else:
            self.hwButtonPressTime[btn] = read_time
            return
        
        HOLD_TIME = 1
        
        LONG_HOLD_TIME = 3.0
        
        hold = False
        
        longHold = False
        
        #log("Elapsed time: " + str(elapsed))
        if elapsed > LONG_HOLD_TIME:
            longHold = True
        elif elapsed > HOLD_TIME:
            hold = True
            #log("Detected HOLD")
        
        val = 1
        
        #bigMessage("Button " + str(btn), 2)
        log("Button: " + str(btn) + " = " + str(val))
        if btn < 5:
            
            for e in editors:
                if editors[e][0].isShowing():
                    editors[e][0].hide()
                    return
            
            if longHold:
                clr = self.effects[btn].color.get()
                if clr == 2:
                    clr = 0
                else:
                    clr = clr + 1
                self.effects[btn].color.set(clr)
            elif hold:
                if self.eq.isEditing():
                    self.eq.stopEditing()
                self.effects[btn].edit()
            else:                
                if self.effects[btn].toggle.get() == 1:
                    self.effects[btn].toggle.set(0)
                else:
                    self.effects[btn].toggle.set(1)
                    
        elif btn < 10:
            if hold:
                log("Saving preset", 1)
                ch = btn - 5
                log("Channel is " + str(ch), 1)
                chSel = ch 
                if ch > 0 and self.ab.toggle.get():
                    chSel = ch + 4
                log("Saving to preset " + str(chSel), 1)
                self.katana.save_to_preset(chSel)
                return
            log("Changing channel to " + str(btn-5), 1)
            ChannelButton.channel.set(btn-5)
        elif btn == AMP_HW_BUTTON:
            self.sendOutput(AMP_HW_BUTTON, 1)
            self.nextAmp.nextItem()
            self.sendOutput(AMP_HW_BUTTON, 0)
        elif btn == NEXT_HW_BUTTON:
            self.sendOutput(NEXT_HW_BUTTON, 1)
            self.nextEffect.nextItem()
            self.sendOutput(NEXT_HW_BUTTON, 0)
        elif btn == AB_HW_BUTTON:
            if self.ab.toggle.get() == 1:
                self.ab.toggle.set(0)
            else:
                self.ab.toggle.set(1)
        elif btn == MUTE_HW_BUTTON:
            if self.amp_panel.isEditing():
                self.amp_panel.stopEditing()
                return
            if hold:
                self.amp_panel.edit()
            elif self.mute.toggle.get() == 1:
                self.mute.toggle.set(0)
            else:
                self.mute.toggle.set(1)
        elif btn == EQ_HW_BUTTON:
            if self.eq.isEditing():
                self.eq.stopEditing()
                return
            if hold:
                self.eq.editEQ()
            elif self.eq.toggle.get() == 1:
                self.eq.toggle.set(0)
            else:
                self.eq.toggle.set(1)            
        
    def readChannel(self):
        log("Reading channel info")
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        abval = 0
        if ch > 4:
            abval = 1
        self.ab.toggle.trace_vdelete('w', self.ab_trace)
        self.ab.toggle.set(abval)
        self.sendOutput(AB_HW_BUTTON, abval)
        self.ab_trace = self.ab.toggle.trace('w', self.abStateChanged)
        log("Channel is " + str(ch))
        chSel = -1
        if ch <= 4 and self.ab.toggle.get() == 0:
            chSel = ch
        elif ch > 4 and self.ab.toggle.get():
            chSel = ch - 4
        ChannelButton.channel.trace_vdelete('w', self.channel_trace)
        log("Setting channel selected button" + str(chSel))
        ChannelButton.channel.set(chSel)
        for i in range(0,5):
            self.sendOutput(i+5,0)
        if chSel >= 0:
            self.sendOutput(chSel+5, 1)
        self.channel_trace = ChannelButton.channel.trace('w', self.channelStateChanged)
        self.readPatchNames()

                
    def readPatchNames(self):
        names = self.katana.get_patch_names()
        self.channels[0].text.set("Ch." + str(0) + " " + names[0])
        if self.ab.toggle.get() == 0:
            for i in range(1,5):
                self.channels[i].text.set("Ch." + str(i) + " " + names[i])
        else:
            for i in range(5,9):
                self.channels[i-4].text.set("Ch." + str(i) + " " + names[i])        
        
    def readAmp(self):
        log("Reading amp info")
        amp_selection = self.katana.query_amp()
        log("Amp selection is " + str(amp_selection))
        ampName = AMP_MAP[amp_selection]
        log("Selecting " + ampName)
        self.nextAmp.setSelection((amp_selection, ampName))
        
    def readEQ(self):
        eqState = self.katana.query_sysex_byte(CHANNEL_EQ_SW)
        self.eq.toggle.trace_vdelete('w', self.eq_trace)
        self.eq.toggle.set(eqState)
        self.eq_trace = self.eq.toggle.trace('w', self.eqStateChanged)
        self.sendOutput(13, eqState)
        self.eq.read()
        
    def read(self):
        self.readChannel()
        for effect in self.effects:
            effect.read()
        self.readAmp()
        self.readEQ()
        
    def abStateChanged(self, *args):
        abVal = self.ab.toggle.get()
        if abVal == 1:
            bigMessage("A/B: B", 1.5)
        else:
            bigMessage("A/B: A", 1.5)
        log("AB set to " + str(abVal), 1)
 
        self.readPatchNames()
        if ChannelButton.channel.get() > -1:
            log("setting channel to -1", 1)
            self.selectedChannel = ChannelButton.channel.get()
            ChannelButton.channel.set(-1)
        else:
            log("setting channel to " + str(self.selectedChannel))
            ChannelButton.channel.set(self.selectedChannel)
              
#         for i in range(0,9):
#             log("selecting channel " + str(i), 1)
#             self.katana.select_channel(i)
#             time.sleep(3)
        
    def channelStateChanged(self, *args):
        log("Channel state changed to " + str(ChannelButton.channel.get()),1)
        ch = ChannelButton.channel.get()
        log("Raw channel value =  " + str(ch),1)
        chSel = -1
        if ch >= 0:
            chSel = ch
            
        for i in range(0,5):
            self.sendOutput(i+5,0)
        if chSel >= 0:
            log("output " + str(chSel+5) + " set to 1", 1)
            self.sendOutput(chSel+5, 1)
            
        log("chSel value = " + str(chSel), 1)
        if ch == 0:
            ch = 4 #panel 0x04
            log("Selecting channel 4",1)
            bigMessage("Panel", 2.5)
            self.katana.select_channel(ch)
            
        elif ch > 0:
            if self.ab.toggle.get() == 0:
                ch = ch - 1
                log("ab 0 katana.select " + str(ch), 1)
                self.katana.select_channel(ch)
                bigMessage("Ch. " + str(ch+1),2.5)
                
            else:
                ch = ch + 4
                log("ab 1 katana.select " + str(ch), 1)
                self.katana.select_channel(ch)
                bigMessage("Ch. " + str(ch),2.5)
        else:
            log("channel -1", 1)
                
        #time.sleep(1.2)
        self.readPatchNames()
        for effect in self.effects:
            effect.read()
        self.readAmp()
        self.readEQ()
        
    def eqStateChanged(self,*args):
        log("Eq state changed")
        if self.eq.toggle.get():
            log("Setting Eq on")
            self.katana.send_sysex_data(CHANNEL_EQ_SW, (0x01,))
            self.sendOutput(13,1)
            bigMessage("Eq: On",1.5)
        else:
            log("Setting Eq off")
            self.katana.send_sysex_data(CHANNEL_EQ_SW, (0x00,))
            self.sendOutput(13,0)
            bigMessage("Eq: Off",1.5)
            
    def muteStateChanged(self, *args):
        if self.mute.toggle.get():
            log("Muting")
            bigMessage("Mute: On", 1.5)
            self.katana.mute()
        else:
            log("Unmuting")
            bigMessage("Mute: Off", 1.5)
            self.katana.unmute()
    
    def subscribe(self, pinRange, callback):
        update = False
        for pin in pinRange:
            log("subscribing pin " + str(pin))
            if pin not in self.subscribers:
                self.subscribers[pin] = []
                if pin > 15:
                    update = True
            self.subscribers[pin].append(callback)
        if update:
            pins = set()
            for pin in self.subscribers:
                if pin > 15:
                    pins.add(pin)
            self.hw_board.queue.put(pins)
            
    def unsubscribe(self, pinRange, callback):
        for pin in pinRange:
            log("unsubscribing pin " + str(pin))
            if pin in self.subscribers:
                self.subscribers[pin].remove(callback)
                if len(self.subscribers[pin]) == 0:
                    self.subscribers.pop(pin, None)
        pins = set()
        for pin in self.subscribers:
            if pin > 15:
                pins.add(pin)
        self.hw_board.queue.put(pins)        
                
    def clear_subscribers(self, pinRange):
        for pin in pinRange:
            if pin in self.subscribers:
                log("unsubscribing pin " + str(pin))
                self.subscribers[pin].clear()
                self.subscribers.pop(pin, None)
        pins = set()
        self.hw_board.queue.put(pins)                
                
    def sendOutput(self, pin, level):
        ticks = time.time()
        msg = (pin, level, ticks)
        self.hw_board.queue.put(msg)
    
    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                #hw_board = msg[0]
                # Check contents of message and do whatever is needed.
                log("process incoming")
                log("pin " + str(msg[1]) + " value = " + str(msg[2]))
                pin = msg[1]
                val = msg[2]
                ticks = msg[3]
                if pin in self.subscribers:
                    for s in self.subscribers[pin]:
                        s((pin,val,ticks))
                #val = msg[2]
                #if pin < 16:
                #    hw_board.queue.put(msg)
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
        
        self.hw_board = HWBoard()

        # Set up the GUI part
        self.gui = KatanaApp(master, self.queue, self.hw_board, self.endApplication)
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        
        self._next_time = time.time()
        
        reads_per_second = 60
        
        self._interval = 1.0 / reads_per_second
        
        self.hw_thread = threading.Thread(target=self.hw_update)
        self.hw_thread.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )
        #self.gui.subscribe(range(16,21), self.event)
        #self.gui.clear_subscribers(range(0,24))
        self.gui.read()
        
    def event(self, msg):
        log("Subscribed event triggered")
        log(msg)

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
                
        log("Digital read:" + str(avgDigitalReadTime/nReads))
        log("Analog read:" + str(avgAnalogReadTime/nReads))
        log("Total time to read:" + str(avgReadTime/nReads))        
        
        self.hw_board.stop()

    def endApplication(self):
        for i in range(0,16):
            self.gui.sendOutput(i,0)
        time.sleep(1)
        self.running = 0
        
    def close_window(self):
        log( "Window closed")
        self.endApplication()


client = ThreadedClient(root)

log("Ready")

log(str(sys.argv))
small = 0

if len(sys.argv) > 1:
    small = int(sys.argv[1])
else:
    small = 0

if small == 1:      
    log("Rendering small UI") 
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    scale_length = 64
else:
    log("Rendering large UI")

root.mainloop(  )