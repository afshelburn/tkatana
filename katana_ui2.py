#!/usr/bin/python3

import tkinter as tk

from tkinter import *
import tkinter.font as tkFont

import tkinter.filedialog as fdialog

from itertools import cycle
import time
import katana
import pigpio
import SN74HC165
import PatchData
import center_tk_window as centerTK
import json
from PatchData import *

root = tk.Tk()

root.attributes('-zoomed',True)

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

def destroyObj(obj):
    #print("Destroy object")
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
    def __init__(self, katana, hw_board, title, toggle_addr, color_addr, color_assign, effect_addr, level_addr, effects, hw_button, effectsSettings, parent):
        
        self.katana = katana
        self.hw_board = hw_board
        
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
        print("Editing " + self.base_title)
        print(self.effectName)
        if self.effectName in self.effectsSettings:
            #print(str(self.effectsSettings[self.effectName]))
            key = self.base_title + "." + self.effectName
            if key in editors:
                editors[key][0].read()
                editors[key][0].show()
            else:
                frm = tk.Toplevel(root, width=480, height=320)
                editors[key] = (EffectEditor(frm, self.katana, self.effectName, self.effectsSettings[self.effectName]), frm)
                editors[key][0].read()
                centerTK.center(root, frm)
                
    def write(self, *args):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        print("Write to channel " + str(ch))
        print("Writing " + self.base_title)
        print(self.effectName)
        if self.effectName in self.effectsSettings:
            for setting in self.effectsSettings[self.effectName]:
                addr = setting[5]
                sz = setting[6]
                #print(setting[0] + "->" + str(addr))
                addrNew = channelAddress(addr, ch)
                tmpVal = self.katana.query_sysex_int(addr, sz)
                curVal = self.katana.query_sysex_int(addrNew, sz)
                #print("Writing " + str(tmpVal) + " over " + str(curVal))
                if not tmpVal == curVal:
                    #print(str(setting))
                    #print("Writing " + str(tmpVal) + " over " + str(curVal))
                    self.katana.send_sysex_int(addrNew, tmpVal, sz)
                    
        tgl = self.toggle.get()
        ch_tgl_addr = channelAddress(self.toggle_addr, ch)
        self.katana.send_sysex_data(ch_tgl_addr, (tgl,))
        
        ch_assign_clr_addr = channelAddress(self.color_assign_addr, ch)
        
        clr = self.katana.query_sysex_byte(self.color_addr)
        
        ch_clr_addr = channelAddress(self.color_addr, ch)
        
        self.katana.send_sysex_data(ch_clr_addr, (self.color.get(),))
        
        print("Assigning effect " + str(self.effectIndex) + " to color " + str(clr))

        self.katana.assign_effect(ch_assign_clr_addr, clr, self.effectIndex)

        self.katana.send_sysex_data(channelAddress(self.effect_addr, ch), (self.effectIndex,))
        
        amp = self.katana.query_sysex_byte(QUERY_AMP)
        print("Writing amp " + str(amp) + " to patch")
        self.katana.send_sysex_data(channelAddress(QUERY_AMP,ch),(amp,))
        
    def nextEffect(self):
        print(str(self.color.get()))
        print("Selecting next effect for " + self.colors[self.color.get()] + ": " + self.label.get())
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
        print("Level changed")
        #lvl = self.level_slider.get()
        #print(self.label.get() + " level changed to " + str(lvl))
        #self.katana.send_sysex_data(self.level_addr[0], (lvl,))
        
    def toggleState(self, *args):
        self.katana.send_sysex_data(self.toggle_addr, (self.toggle.get(),))
        self.hw_board.set_led(self.hw_button, self.toggle.get())
        state = ": off"
        if self.toggle.get():
            state = ": on"
        bigMessage(self.effectName + state, 1.5)
    
    def readEffect(self):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        print("Read from channel " + str(ch))
        print("Color selected is " + str(self.color.get()) + " should be " + str(self.katana.query_sysex_byte(self.color_addr)))
        res = self.katana.query_sysex_byte(self.color_assign_addr, self.color.get())
        print("Setting " + self.label.get() + " effect state to " + str(self.effectMap[res]))
        val = next(self.effectCycle[self.color.get()])
        while val[0] != res:
            val = next(self.effectCycle[self.color.get()])
        self.label.set(self.base_title + ": " + val[1])
        self.effectName = val[1]
        self.effectIndex = val[0]
        self.label.set(self.base_title + ": " + val[1])

        
    def readToggle(self):
        res = self.katana.query_sysex_byte(self.toggle_addr)
        #print("Setting " + self.label.get() + " toggle state to " + str(res))
        self.toggle.trace_vdelete('w', self.toggle_trace)
        self.toggle.set(res)
        self.toggle_trace = self.toggle.trace('w', self.toggleState)
        self.hw_board.set_led(self.hw_button, self.toggle.get())
        
    def readColor(self):
        res = self.katana.query_sysex_byte(self.color_addr)
        #print("Setting " + self.label.get() + " color state to " + str(self.colors[res]))
        self.color.trace_vdelete('w', self.color_trace)
        self.color.set(res)
        self.color_trace = self.color.trace('w', self.changeColor)
        
    def read(self):
        if self.katana is None:
            return
        print("Reading state for " + self.label.get())
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
    def __init__(self, katana, hw_board, title, hw_button, parent):
        self.katana = katana
        self.toggle = IntVar(name=title + ".toggle", value=0)
        self.text = StringVar(name=title + ".text", value=title)
        self.labelWidget = Label(None, textvariable=self.text)
        self.title_frame = tk.LabelFrame(parent, labelwidget=self.labelWidget, padx=10, pady=5)
        self.toggle_button = tk.Checkbutton(self.title_frame, image=off_image, selectimage=on_image, indicatoron=False, variable=self.toggle)
        self.toggle_button.grid(row=1, column=0, sticky=N+W+S+E, columnspan=3)
        self.toggle_trace = self.toggle.trace('w', self.stateChanged)
        self.hw_board = hw_board
        self.hw_button = hw_button
        
    def stateChanged(self, *args):
        print(self.text.get() + " changed to " + str(self.toggle.get()))
        self.hw_board.set_led(self.hw_button, self.toggle.get())
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
        print(str(newVal))
        bigMessage(str(newVal[1]), 1.5)
        
    def get(self):
        return self.currentSelection
        
    def setSelection(self, selection):
        val = next(self.selectionPool)
        #print("Selection: " + str(selection))
        while val != selection:
            val = next(self.selectionPool)
            #print(str(val))
        print("Selected " + str(val))
        self.text.set(self.base_title + ": " + selection[1])
        
class EffectSelector(MomentaryButton):
    def __init__(self, katana, title, effectPanels, parent):
        super().__init__(katana, title, self.nextItem, parent)
        self.katana = katana
        self.effectPanels = effectPanels
        
    def nextItem(self):
        print(self.text.get())
        activePanel = None
        for panel in self.effectPanels:
            if panel.toggle.get() == 1:
                activePanel = panel
                break
                
        if activePanel is not None:
            activePanel.nextEffect()

class EQToggle(ToggleButton):
    def __init__(self, katana, hw_board, title, hw_button, parent):
        super().__init__(katana, hw_board, title, hw_button, parent)
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
        self.peq = EQEditor(self.katana, "P-EQ", ParametricEQ, ChParametricEQ, self.peq_frame)

        self.geq_frame = tk.Toplevel(root, width=480, height=320)
        self.geq = EQEditor(self.katana, "G-EQ", GraphicEQ, ChGraphicEQ, self.geq_frame)
        
        self.geq_frame.withdraw()
        self.peq_frame.withdraw()
        
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
    def selectEQ(self, *args):
        print("EQ state changed: " + str(args))
        self.eq_type.trace_vdelete('w', self.eq_type_trace)
        val = self.eq_type.get()
        self.katana.send_sysex_data(CHANNEL_EQ_TYPE, (val,))
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
    def editEQ(self):
        print("Edit EQ")
        if self.eq_type.get() == 0:
            self.peq_frame.deiconify()
            self.peq_frame.attributes("-topmost", True)
        else:
            self.geq_frame.deiconify()
            self.geq_frame.attributes("-topmost", True)
        
    def writeEQ(self):
        print("Write EQ")
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        print("Writing EQ data to channel " + str(ch))
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
        print("EQ Type is " + str(eq_type))
        self.eq_type.trace_vdelete('w', self.eq_type_trace)
        self.eq_type.set(eq_type)
        self.eq_type_trace = self.eq_type.trace('w', self.selectEQ)
        
class EQEditor:
    def __init__(self, katana, title, levelInfo, chLevelInfo, parent):
        
        self.katana = katana

        self.title_frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        
        self.parent = parent

        self.levels = []
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
            slider = Scale(self.title_frame, variable=l, from_=levelInfo[level][3], to=levelInfo[level][2], orient=o, length=100)
            slider.grid(row=row,column=col,columnspan=columnspan)
            label = Label(self.title_frame, text=level, anchor="center", padx=2, font=customFont)
            label.grid(row=(row+1),column=col,columnspan=columnspan)
            col = col + 1
            trace_level = l.trace('w', self.stateChanged)
            self.levels.append([l,slider,trace_level,chLevelInfo[level][4],levelInfo[level][0], levelInfo[level][1], chLevelInfo[level][4]])
            
        self.title_frame.grid(row=0,column=0)
            
        self.reset = tk.Button(self.title_frame, text="Reset", command=self.reset)
        self.reset.grid(row = 2, column = 0)
        
        self.close = tk.Button(self.title_frame, text="Close", command=self.hide)
        self.close.grid(row = 2, column = len(levelInfo)-1)
        
        self.activeEditor = None
        
    def reset(self):
        print("Reset")
        for level in self.levels:
            level[1].set(level[5])
            #self.katana.send_sysex_data(addr, (level[5],))
            
    def write(self):
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        print("Writing EQ data to channel " + str(ch))
        for level in self.levels:
            #print("Writing value = " + str(level[0].get()+level[4]))
            self.katana.send_sysex_data(channelAddress(level[6], ch), (level[0].get()+level[4],))
            #val = self.katana.query_sysex_byte(channelAddress(level[6], ch))
            #print("Read channel value = " + str(val))
            #val = self.katana.query_sysex_byte(level[6])
            #print("Read immediate value = " + str(val))
            #level[1].set(level[5])
            
    def hide(self):
        print("Close")
        self.parent.withdraw()
        
    def show(self):
        print("Showing")
        self.parent.deiconify()
            
    def stateChanged(self, *args):
        print("Eq state changed")
        for level in self.levels:
            if level[0]._name == args[0]:
                addr = level[3]
                #print(str(addr))
                val = level[0].get()
                #print("Updating " + level[0]._name + " to value " + str(val))
                self.katana.send_sysex_data(addr, (val+level[4],))
        
    def read(self):
        print("Reading Eq state")
        for level in self.levels:
            addr = level[3]
            #print(str(addr))
            val = self.katana.query_sysex_byte(addr)
            #print("Updating " + level[0]._name + " to value " + str(val))
            level[0].trace_vdelete('w', level[2])
            level[0].set(val - level[4])
            level[2] = level[0].trace('w', self.stateChanged)
            


class EffectEditor:
    def __init__(self, parent, katana, title, settings):
        self.katana = katana

        self.title_frame = tk.LabelFrame(parent, text=title, padx=10, pady=5)
        
        self.parent = parent
        
        #('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x02))
        
        self.settings = settings.copy()
        col = 0
        
        self.trace = {}
        #('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x02))
        for setting in self.settings:
            #print(str(setting))
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
            
        self.reset = tk.Button(self.title_frame, text="Reset", command=self.reset)
        self.reset.grid(row = row + 2, column = 0)
        
        self.close = tk.Button(self.title_frame, text="Close", command=self.hide)
        self.close.grid(row = row + 2, column = len(settings)-1)
            
        self.title_frame.grid(row=0,column=0)
    
    def reset(self):
        print("Reset")
        for i in range(0, len(self.settings)):
            var = self.trace[i][1]
            setting = self.settings[i]
            var.set(setting[2])
            
    def hide(self):
        print("Closing")
        self.parent.withdraw()
        
    def show(self):
        print("Showing")
        self.parent.deiconify()
        
    def stateChanged(self, *args):
        #print(str(args))
        #print(args[0] + " state changed")
        for i in range(0,len(self.settings)):
            var = self.trace[i][1]
            if var._name == args[0]:
                setting = self.settings[i]
                addr = setting[5]
                sz = setting[6]
                val = var.get() + setting[1]
                #print(str(setting))
                #print("val = " + str(val))
                #print("sz = " + str(sz))
                self.katana.send_sysex_int(addr, val, sz)
                break

    def read(self):
        i = 0
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        print("Reading effect from channel " + str(ch))
        for setting in self.settings:
            addr = setting[5]
            sz = setting[6]
            #print("Setting:" + str(setting))
            #addrNew = (chOffset[0], chOffset[1], addr[2], addr[3])
            #print(str(addr))
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
        print("Closing")
        self.parent.withdraw()
        
    def show(self):
        print("Showing")
        self.parent.deiconify()
        
    def set_pedal_map(self,*args):
        print("Setting pedal map to " + self.pedal_option.get())
        
class KatanaUI:
    def __init__(self, katana):
        
        self.katana = katana
        
        self.pi = pigpio.pi()
   
        self.hw_board = SN74HC165.PISO(self.pi, SH_LD=16, OUTPUT_LATCH=26, chips=2, reads_per_second=60, adc_enable=5, adc_channels=1)
        
        self.effects = []
        self.channels = []
        self.controls = []

        layout = ["Boost", "Mod", "FX", "Delay", "Reverb"]

        effect_map = {"Boost":BOOST_OPTIONS, "Mod":EFFECT_OPTIONS, "FX":EFFECT_OPTIONS, "Delay":DELAY_OPTIONS, "Reverb":REVERB_OPTIONS}
        self.effect_settings = {"Boost":PatchData.BOOST_SETTINGS, "Mod":PatchData.FX1_SETTINGS, "FX":PatchData.FX2_SETTINGS, "Delay":PatchData.DELAY_SETTINGS, "Reverb":PatchData.REVERB_SETTINGS}
        col = 0

        for item in layout:
            panel = EffectPanel(self.katana, self.hw_board, item, TOGGLES[col], COLORS[col], COLOR_ASSIGN[col], EFFECTS[col], LEVELS[item], effect_map[item], HW_BUTTONS[col], self.effect_settings[item], root)
            panel.title_frame.grid(row=2, column=col)
            if col == 0:
                channel = ChannelButton(self.katana, "Panel", col, root)
            else:
                channel = ChannelButton(self.katana, "Ch." + str(col), col, root)
            channel.title_frame.grid(row=1, column=col)
            col = col + 1
            self.effects.append(panel)
            self.channels.append(channel)

        
        self.channel_trace = ChannelButton.channel.trace('w', self.channelStateChanged)
    
        self.mute = ToggleButton(self.katana, self.hw_board, "Mute", MUTE_HW_BUTTON, root)
        self.mute.title_frame.grid(row=0, column=4)
        self.mute_trace = self.mute.toggle.trace('w', self.muteStateChanged)

        self.ab = ToggleButton(self.katana, self.hw_board, "A/B", AB_HW_BUTTON, root)
        self.ab.title_frame.grid(row=0, column=2)
        self.ab_trace = self.ab.toggle.trace('w', self.abStateChanged)

        ampShortList = []
        for i in AMP_LOOP_SHORT:
            #print(AMP_MAP[i])
            ampShortList.append((i, AMP_MAP[i]))
            #ampNameList.append(AMP_MAP[i])
            
        self.ampCycle = cycle(ampShortList)
        self.nextAmp = RingSelector(self.katana, "Amp", QUERY_AMP, self.ampCycle, root)
        self.nextAmp.title_frame.grid(row=0, column=0)
        
        self.nextEffect = EffectSelector(self.katana, "Next Effect", self.effects, root)
        self.nextEffect.title_frame.grid(row=0, column=1)
        
        self.eq_type = tk.IntVar(name="eq.type", value=0)
                
        self.eq = EQToggle(self.katana, self.hw_board, "Eq", EQ_HW_BUTTON, root)
        self.eq.title_frame.grid(row=0,column=3)
        self.eq_trace = self.eq.toggle.trace('w', self.eqStateChanged)
        
        self.controls.append(self.nextAmp)
        self.controls.append(self.nextEffect)
        self.controls.append(self.ab)
        self.controls.append(self.eq)
        self.controls.append(self.mute)
        
        self.closeButton = tk.Button(root, text="Close", command=self.exit)
        self.closeButton.grid(row=3,column=4)

        self.restoreButton = tk.Button(root, text="Restore", command=self.restoreFile)
        self.restoreButton.grid(row=3,column=1)

        self.saveButton = tk.Button(root, text="Backup", command=self.saveAll)
        self.saveButton.grid(row=3,column=2)
        
        self.saveChButton = tk.Button(root, text="Save Channel", command=self.saveCurrentChannel)
        self.saveChButton.grid(row=3,column=0)
        
        self.editPedalButton = tk.Button(root, text="Pedal 1", command=self.editPedal1)
        self.editPedalButton.grid(row=3,column=3)
        
        self.selectedChannel = -1
        
        self.hwButtonPressTime = {}
        for i in range(0,15):
            self.hwButtonPressTime[i] = 0
            
        PEDAL_WAH_OPTION = [(FX_WAH_PEDAL,0,100),(MOD_WAH_PEDAL,0,100), (FX_EVH_WAH_PEDAL,0,100), (MOD_EVH_WAH_PEDAL,0,100)]
        PEDAL_VOLUME_OPTION = [(VOLUME_PEDAL,0,100)]
        PEDAL_DELAY_TIME_OPTION = [(DELAY_TIME_PEDAL,1,2000)]
        PEDAL_TREMOLO_RATE_OPTION = [(MOD_TREMOLO_PEDAL,0,100),(FX_TREMOLO_PEDAL,0,100)]
        PEDAL_FX_BLEND_OPTION = [(FX_BLEND_PEDAL,0,100)]
        PEDAL_FX_BEND_OPTION = [(FX_BEND_PEDAL,0,100)]
            
        self.pedal_options = {'Wah':PEDAL_WAH_OPTION,'Volume':PEDAL_VOLUME_OPTION,'Delay':PEDAL_DELAY_TIME_OPTION,'Tremolo':PEDAL_TREMOLO_RATE_OPTION,'FX Blend':PEDAL_FX_BLEND_OPTION,'FX Bend':PEDAL_FX_BEND_OPTION}
        self.pedal_map = {}
        
        self.pedal_vars = []
        self.pedal_1_frame = tk.Toplevel(root, width=480, height=320)
        self.pedal_1_editor = PedalEditor(self.katana, "Pedal 1 Option", self.pedal_options, 'Wah', self.pedal_1_frame)
        self.pedal_vars.append(self.pedal_1_editor.pedal_option)

        self.pedal_1_frame.withdraw()
                
        
    def editPedal1(self):
        print("Edit pedal 1")
        self.pedal_1_editor.show()      
    
    def saveCurrentChannel(self):
        
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        
        data = {}
        
        self.saveEffect("Boost", ch, data)
        self.saveEffect("Mod", ch, data)
        self.saveEffect("FX", ch, data)
        self.saveEffect("Delay", ch, data)
        self.saveEffect("Reverb", ch, data)
        self.saveEQ(ch, data)
        
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = '/home/pi/channel_' + str(ch) + '_' + timestr + '.json'
        with open(f, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            
    #def restoreChannel(self, ch)
            
    def saveAll(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        f = '/home/pi/amp_settings' + '_' + timestr + '.json'
        data = {}
        for i in range(0,9):
            self.saveEffect("Boost", i, data)
            self.saveEffect("Mod", i, data)
            self.saveEffect("FX", i, data)
            self.saveEffect("Delay", i, data)
            self.saveEffect("Reverb", i, data)
        with open(f, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            
    def saveEQ(self, ch, data):
        print("Saving EQ settings")
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
            data['EQ'][ch]['PEQ'].append((setting, chAddr, val, 1))
        data['EQ'][ch]['GEQ'] = []
        for setting in ChGraphicEQ:
            chAddr = channelAddress(ChGraphicEQ[setting][4], ch)
            val = self.katana.query_sysex_byte(chAddr)
            data['EQ'][ch]['GEQ'].append((setting, chAddr, val, 1))
            
    def saveEffect(self, effectType, ch, data):
#         FX1_ADCOMP.append(('SUSTAIN', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x17)))
        effectsSettings = self.effect_settings[effectType]
        data[effectType] = {}
        print("Saving state for " + effectType)
        #for i in range(0,9):
        print("Reading " + effectType + " from channel " + str(ch))
        data[effectType][ch] = {}
        data[effectType][ch]['STATE'] = []
        toggle_addr = channelAddress(TOGGLE_MAP[effectType], ch)
        data[effectType][ch]['STATE'].append(('toggle', toggle_addr, self.katana.query_sysex_byte(toggle_addr), 1))
        color_addr = channelAddress(COLOR_MAP[effectType], ch)
        data[effectType][ch]['STATE'].append(('color', color_addr, self.katana.query_sysex_byte(color_addr), 1))        
        for effectName in effectsSettings:
            print("Reading " + effectName)
            list = effectsSettings[effectName]
            data[effectType][ch][effectName] = []
            for setting in list:
                #print("Reading " + str(setting))
                chAddr = channelAddress(setting[5], ch)
                val = self.katana.query_sysex_int(chAddr, setting[6])# - setting[1]
                #if val > -1 and val < 128:
                data[effectType][ch][effectName].append((setting[0], chAddr, val, setting[6]))
                #else:
                #    print("Failed to store value " + val + " for " + effectName + setting[0] + " = " + str(val))
        
    def saveAmp(self, ch, data):
        print("Saving Amp setting")
        #ParametricEQ = {'LOWCUT':(0, 0, 0, 17, (0x00, 0x00, 0x00, 0x13)),'L
        ampAddr = channelAddress(QUERY_AMP, ch)
        data['AMP'] = {}
        data['AMP'][ch] = {}
        data['AMP'][ch]['STATE'] = []
        data['AMP'][ch]['STATE'].append(('type', ampAddr, self.katana.query_sysex_byte(ampAddr), 1))
        
    def restoreFile(self):
        filename = fdialog.askopenfilename(initialdir = "/home/pi",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        if filename is not None:
            print(filename)
            with open(filename, 'r') as json_file:
                data = json.load(json_file)
                print("Restoring settings from file")
                self.restore(data)
                print("Reading amp settings into UI")
            
            self.read()
#                 
#         time.sleep(3)
#         d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
#         ch = d[1][0][1]
#         if ch < 8:
#             #ChannelButton.channel.set(ch+1)
#             time.sleep(3)
#             ChannelButton.channel.set(ch)
#         else:
#             #ChannelButton.channel.set(ch-1)
#             time.sleep(3)
#             ChannelButton.channel.set(ch)
        
    
    def restore(self, data, targetCh=-1):
        print("Restoring data")
        
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        curr_ch = d[1][0][1]
        
        if targetCh > -1 and targetCh != curr_ch:
            ChannelButton.channel.set(targetCh)
        
        for item in data:
            for ch in data[item]:
                for group in data[item][ch]:
                    print("Restoring " + group)
                    for setting in data[item][ch][group]:
                        addr = setting[1]
                        print(str(setting))
                        ich = int(ch)
                        print(setting[0] + " -> " + str(setting[2]) + " @" + str(addr) + " for ch " + str(ich) + "/" + str(curr_ch))
                        tmpAddr = None
                        
                        if targetCh > -1:
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
                            self.katana.send_sysex_int(addr, val, setting[3])
                            if tmpAddr is not None:
                                self.katana.send_sysex_int(tmpAddr, val, setting[3])
                        else:
                            self.katana.send_sysex_int(addr, val, 1)
                            if tmpAddr is not None:
                                self.katana.send_sysex_int(tmpAddr, val, 1)

    def pedal_change(self, channel, value, read_time):
        pedal_var = self.pedal_vars[channel]
        #print(pedal_var.get() + " changed, raw value = " + str(value))
        settings = self.pedal_options[pedal_var.get()] # a list of (address, min, max)
        for setting in settings:
            minVal = float(setting[1])
            maxVal = float(setting[2])
            mapVal = int(minVal + int(float(value) / 255.0 * maxVal))
            #print("Setting value = " + str(mapVal))
            sz = 1
            if maxVal > 127:
                sz = 2
            self.katana.send_sysex_int(setting[0], mapVal, sz)     
        
    def hardware_button(self, btn, val, read_time):
        
        if val == 0:
            elapsed = read_time - self.hwButtonPressTime[btn]
        else:
            self.hwButtonPressTime[btn] = read_time
            return
        
        HOLD_TIME = 1.5
        
        hold = False
        
        #print("Elapsed time: " + str(elapsed))
        
        if elapsed > HOLD_TIME:
            hold = True
            #print("Detected HOLD")
        
        val = 1
        
        #bigMessage("Button " + str(btn), 2)
        print("Button: " + str(btn) + " = " + str(val))
        if btn < 5:
            if hold:
                clr = self.effects[btn].color.get()
                if clr == 2:
                    clr = 0
                else:
                    clr = clr + 1
                self.effects[btn].color.set(clr)
            else:                
                if self.effects[btn].toggle.get() == 1:
                    self.effects[btn].toggle.set(0)
                else:
                    self.effects[btn].toggle.set(1)
                    
        elif btn < 10:
            ChannelButton.channel.set(btn-5)
        elif btn == AMP_HW_BUTTON:
            self.hw_board.set_led(AMP_HW_BUTTON, 1)
            self.nextAmp.nextItem()
            self.hw_board.set_led(AMP_HW_BUTTON, 0)
        elif btn == NEXT_HW_BUTTON:
            self.hw_board.set_led(NEXT_HW_BUTTON, 1)
            self.nextEffect.nextItem()
            self.hw_board.set_led(NEXT_HW_BUTTON, 0)
        elif btn == AB_HW_BUTTON:
            if self.ab.toggle.get() == 1:
                self.ab.toggle.set(0)
            else:
                self.ab.toggle.set(1)
        elif btn == MUTE_HW_BUTTON:
            if self.mute.toggle.get() == 1:
                self.mute.toggle.set(0)
            else:
                self.mute.toggle.set(1)
        elif btn == EQ_HW_BUTTON:
            if self.eq.toggle.get() == 1:
                self.eq.toggle.set(0)
            else:
                self.eq.toggle.set(1)            
        
    def readChannel(self):
        print("Reading channel info")
        d = self.katana.query_sysex_data(CURRENT_PRESET_ADDR, CURRENT_PRESET_LEN)
        ch = d[1][0][1]
        abval = 0
        if ch > 4:
            abval = 1
        self.ab.toggle.trace_vdelete('w', self.ab_trace)
        self.ab.toggle.set(abval)
        self.hw_board.set_led(AB_HW_BUTTON, abval)
        self.ab_trace = self.ab.toggle.trace('w', self.abStateChanged)
        print("Channel is " + str(ch))
        chSel = -1
        if ch <= 4 and self.ab.toggle.get() == 0:
            chSel = ch
        elif ch > 4 and self.ab.toggle.get():
            chSel = ch - 4
        ChannelButton.channel.trace_vdelete('w', self.channel_trace)
        print("Setting channel selected button" + str(chSel))
        ChannelButton.channel.set(chSel)
        for i in range(0,5):
            self.hw_board.set_led(i+5,0)
        if chSel >= 0:
            self.hw_board.set_led(chSel+5, 1)
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
        print("Reading amp info")
        amp_selection = self.katana.query_amp()
        print("Amp selection is " + str(amp_selection))
        ampName = AMP_MAP[amp_selection]
        print("Selecting " + ampName)
        self.nextAmp.setSelection((amp_selection, ampName))
        
    def readEQ(self):
        eqState = self.katana.query_sysex_byte(CHANNEL_EQ_SW)
        self.eq.toggle.trace_vdelete('w', self.eq_trace)
        self.eq.toggle.set(eqState)
        self.eq_trace = self.eq.toggle.trace('w', self.eqStateChanged)
        self.hw_board.set_led(13, eqState)
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
            
        self.readPatchNames()
        if ChannelButton.channel.get() > -1:
            self.selectedChannel = ChannelButton.channel.get()
            ChannelButton.channel.set(-1)
        else:
            ChannelButton.channel.set(self.selectedChannel)
        
    def channelStateChanged(self, *args):
        print("Channel state changed to " + str(ChannelButton.channel.get()))
        ch = ChannelButton.channel.get()
        print("Raw channel value =  " + str(ch))
        chSel = -1
        if ch >= 0:
            chSel = ch
            
        for i in range(0,5):
            self.hw_board.set_led(i+5,0)
        if chSel >= 0:
            print(str(chSel+5) + " set to 1")
            self.hw_board.set_led(chSel+5, 1)
            
        print("chSel value = " + str(chSel))
        if ch == 0:
            ch = 4 #panel 0x04
            #print("Selecting channel 4")
            bigMessage("Panel", 2.5)
            self.katana.select_channel(ch)
            
        elif ch > 0:
            if self.ab.toggle.get() == 0:
                ch = ch - 1
                bigMessage("Ch. " + str(ch+1),2.5)
                self.katana.select_channel(ch)
                
            else:
                ch = ch + 4
                bigMessage("Ch. " + str(ch),2.5)
                self.katana.select_channel(ch)
                
                
        self.readPatchNames()
        for effect in self.effects:
            effect.read()
        self.readAmp()
        self.readEQ()
        
    def eqStateChanged(self,*args):
        print("Eq state changed")
        if self.eq.toggle.get():
            print("Setting Eq on")
            self.katana.send_sysex_data(CHANNEL_EQ_SW, (0x01,))
            self.hw_board.set_led(13,1)
            bigMessage("Eq: On",1.5)
        else:
            print("Setting Eq off")
            self.katana.send_sysex_data(CHANNEL_EQ_SW, (0x00,))
            self.hw_board.set_led(13,0)
            bigMessage("Eq: Off",1.5)
            
    def muteStateChanged(self, *args):
        if self.mute.toggle.get():
            print("Muting")
            bigMessage("Mute: On", 1.5)
            self.katana.mute()
        else:
            print("Unmuting")
            bigMessage("Mute: Off", 1.5)
            self.katana.unmute()

    def exit(self):
        root.destroy()
                 
#mido.set_backend('mido.backends.rtmidi')
katana = katana.Katana('KATANA MIDI 1',  0,  False)

#katana.send_sysex_data(EDIT_ON)
print("Sleeping...")
#time.sleep(2)
print("Ready")

#katana = katana.Katana('KATANA MIDI 1', 0, False)

katanaUI = KatanaUI(katana)

katanaUI.read()

katanaUI.hw_board.set_callback(katanaUI.hardware_button)
katanaUI.hw_board.set_adc_callback(katanaUI.pedal_change)

print(str(sys.argv))
small = 0

if len(sys.argv) > 1:
    
    small = int(sys.argv[1])
else:
    small = 0


if small == 1:      
    print("Rendering small UI") 
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    scale_length = 64
else:
    print("Rendering large UI")




#katanaUI.hw_board.set_led(11,1)
#katanaUI.hw_board.set_led(8,0)
#katanaUI.hw_board.set_led(12,1)
#katanaUI.hw_board.set_led(9,1)
#time.sleep(5)
#katanaUI.hw_board.set_led(8,1)

root.mainloop()

#katana.send_sysex_data(EDIT_OFF)

katanaUI.hw_board.set_callback(None)
katanaUI.hw_board.set_adc_callback(None)

for i in range(16):
    katanaUI.hw_board.set_led(i,0)

print("Sleeping...")
time.sleep(2)
print("Ready")

katanaUI.hw_board.cancel()
katanaUI.pi.stop()

