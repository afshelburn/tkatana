#!/usr/bin/python3

import tkinter as tk
import mido
import sys
import katana
from tkinter import *
import tkinter.font as tkFont

from itertools import cycle

root = tk.Tk()
root.attributes('-zoomed',True)

bh = 84
bw = 112

on_image = tk.PhotoImage(width=bw, height=bh)
off_image = tk.PhotoImage(width=bw, height=bh)
on_image.put(("magenta",), to=(0, 0, bw-1, bh-1))
off_image.put(("gray",), to=(0, 0, bw-1, bh-1))

AMP_TYPE_ACOUSTIC = 0x01
AMP_TYPE_ACOUSTIC_V = 0x1C

AMP_TYPE_CLEAN = 0x08
AMP_TYPE_CLEAN_V = 0x1d

AMP_TYPE_CRUNCH = 0x0b
AMP_TYPE_CRUNCH_V = 0x1e

AMP_TYPE_LEAD = 0x18
AMP_TYPE_LEAD_V = 0x20

AMP_TYPE_BROWN = 0x17
AMP_TYPE_BROWN_V = 0x1F

AMP_TYPE_NATURAL_CLEAN = 0x00

AMP_TYPE_CLEAN_TWIN = 0x09

AMP_TYPE_COMBO_CRUNCH = 0x02

AMP_TYPE_PRO_CRUNCH = 0x0A

AMP_TYPE_DELUX_CRUNCH = 0x0C

AMP_TYPE_STACK_CRUNCH = 0x03

AMP_TYPE_VO_DRIVE = 0x0D

AMP_TYPE_BG_DRIVE = 0x11

AMP_TYPE_MATCH_DRIVE = 0x0F

AMP_TYPE_POWER_DRIVE = 0x05

AMP_TYPE_VO_LEAD = 0x0E

AMP_TYPE_BG_LEAD = 0x10

AMP_TYPE_EXTREME_LEAD = 0x06

AMP_TYPE_T_AMP_LEAD = 0x16

AMP_TYPE_MS_1959_I = 0x12

AMP_TYPE_MS_1959_II = 0x13

AMP_TYPE_HIGH_GAIN_STACK = 0x04

AMP_TYPE_R_FIER_VINTAGE = 0x14

AMP_TYPE_R_FIER_MODERN = 0x15

AMP_NAMES = ["ACOUSTIC","ACOUSTIC_V","CLEAN","CLEAN_V","CRUNCH","CRUNCH_V","LEAD","LEAD_V","BROWN","BROWN_V","NATURAL_CLEAN","CLEAN_TWIN","COMBO_CRUNCH","PRO_CRUNCH","DELUX_CRUNCH","STACK_CRUNCH","VO_DRIVE","BG_DRIVE","MATCH_DRIVE","POWER_DRIVE","VO_LEAD","BG_LEAD","EXTREME_LEAD","T_AMP_LEAD","MS_1959_I","MS_1959_II","HIGH_GAIN_STACK","R_FIER_VINTAGE","R_FIER_MODERN"]

AMP_LOOP =[AMP_TYPE_ACOUSTIC,AMP_TYPE_ACOUSTIC_V,AMP_TYPE_CLEAN,AMP_TYPE_CLEAN_V,AMP_TYPE_CRUNCH,AMP_TYPE_CRUNCH_V,AMP_TYPE_LEAD,AMP_TYPE_LEAD_V,AMP_TYPE_BROWN,AMP_TYPE_BROWN_V,AMP_TYPE_NATURAL_CLEAN,AMP_TYPE_CLEAN_TWIN,AMP_TYPE_COMBO_CRUNCH,AMP_TYPE_PRO_CRUNCH,AMP_TYPE_DELUX_CRUNCH,AMP_TYPE_STACK_CRUNCH,AMP_TYPE_VO_DRIVE,AMP_TYPE_BG_DRIVE,AMP_TYPE_MATCH_DRIVE,AMP_TYPE_POWER_DRIVE,AMP_TYPE_VO_LEAD,AMP_TYPE_BG_LEAD,AMP_TYPE_EXTREME_LEAD,AMP_TYPE_T_AMP_LEAD,AMP_TYPE_MS_1959_I,AMP_TYPE_MS_1959_II,AMP_TYPE_HIGH_GAIN_STACK,AMP_TYPE_R_FIER_VINTAGE,AMP_TYPE_R_FIER_MODERN]

AMP_LOOP_SHORT = [AMP_TYPE_ACOUSTIC,AMP_TYPE_ACOUSTIC_V,AMP_TYPE_CLEAN,AMP_TYPE_CLEAN_V,AMP_TYPE_CRUNCH,AMP_TYPE_CRUNCH_V,AMP_TYPE_LEAD,AMP_TYPE_LEAD_V,AMP_TYPE_BROWN,AMP_TYPE_BROWN_V,AMP_TYPE_NATURAL_CLEAN,AMP_TYPE_CLEAN_TWIN,AMP_TYPE_COMBO_CRUNCH,AMP_TYPE_PRO_CRUNCH,AMP_TYPE_DELUX_CRUNCH,AMP_TYPE_T_AMP_LEAD,AMP_TYPE_R_FIER_VINTAGE]
AMP_MAP = {}
AMP_MAP[AMP_TYPE_ACOUSTIC] = AMP_NAMES[0]
AMP_MAP[AMP_TYPE_ACOUSTIC_V] = AMP_NAMES[1]
AMP_MAP[AMP_TYPE_CLEAN] = AMP_NAMES[2]
AMP_MAP[AMP_TYPE_CLEAN_V] = AMP_NAMES[3]
AMP_MAP[AMP_TYPE_CRUNCH] = AMP_NAMES[4]
AMP_MAP[AMP_TYPE_CRUNCH_V] = AMP_NAMES[5]
AMP_MAP[AMP_TYPE_LEAD] = AMP_NAMES[6]
AMP_MAP[AMP_TYPE_LEAD_V] = AMP_NAMES[7]
AMP_MAP[AMP_TYPE_BROWN] = AMP_NAMES[8]
AMP_MAP[AMP_TYPE_BROWN_V] = AMP_NAMES[9]
AMP_MAP[AMP_TYPE_NATURAL_CLEAN] = AMP_NAMES[10]
AMP_MAP[AMP_TYPE_CLEAN_TWIN] = AMP_NAMES[11]
AMP_MAP[AMP_TYPE_COMBO_CRUNCH] = AMP_NAMES[12]
AMP_MAP[AMP_TYPE_PRO_CRUNCH] = AMP_NAMES[13]
AMP_MAP[AMP_TYPE_DELUX_CRUNCH] = AMP_NAMES[14]
AMP_MAP[AMP_TYPE_STACK_CRUNCH] = AMP_NAMES[15]
AMP_MAP[AMP_TYPE_VO_DRIVE] = AMP_NAMES[16]
AMP_MAP[AMP_TYPE_BG_DRIVE] = AMP_NAMES[17]
AMP_MAP[AMP_TYPE_MATCH_DRIVE] = AMP_NAMES[18]
AMP_MAP[AMP_TYPE_POWER_DRIVE] = AMP_NAMES[19]
AMP_MAP[AMP_TYPE_VO_LEAD] = AMP_NAMES[20]
AMP_MAP[AMP_TYPE_BG_LEAD] = AMP_NAMES[21]
AMP_MAP[AMP_TYPE_EXTREME_LEAD] = AMP_NAMES[22]
AMP_MAP[AMP_TYPE_T_AMP_LEAD] = AMP_NAMES[23]
AMP_MAP[AMP_TYPE_MS_1959_I] = AMP_NAMES[24]
AMP_MAP[AMP_TYPE_MS_1959_II] = AMP_NAMES[25]
AMP_MAP[AMP_TYPE_HIGH_GAIN_STACK] = AMP_NAMES[26]
AMP_MAP[AMP_TYPE_R_FIER_VINTAGE] = AMP_NAMES[27]
AMP_MAP[AMP_TYPE_R_FIER_MODERN] = AMP_NAMES[28]

BOOST_OPTIONS = {0x00:"Mid Boost",0x01:"Clean Boost",0x02:"Treble Boost",0x03:"Crunch OD",0x04:"Natural OD",0x05:"Warm OD",0x06:"Fat DS",0x08:"Metal DS",0x09:"Oct Fuzz",0x0A:"Blues Drive",0x0B:"Overdrive",0x0C:"T-Scream",0x0D:"Turbo OD",0x0E:"Distortion",0x0F:"Rat",0x10:"Guv DS",0x11:"DST+",0x12:"Metal Zone",0x13:"'60s Fuzz",0x14:"Muff Fuzz"}
#took out 0x07:"Lead DS",

EFFECT_OPTIONS = {0x00:"T Wah",0x01:"Auto Wah",0x02:"Pedal Wah",0x03:"Comp",0x04:"Limiter",0x06:"Graphic EQ",0x07:"Parametric EQ",0x09:"Guitar Sim",0x0A:"Slow Gear",0x0B:"",0x0C:"Wave Synth",0x0E:"Octave",0x0F:"Pitch Shifter",0x10:"Harmonist",0x12:"AC Processor",0x13:"Phaser",0x14:"Flanger",0x15:"Tremolo",0x16:"Rotary",0x17:"Uni-V",0x19:"Slicer",0x1A:"Vibrato",0x1B:"Ring Mod",0x1C:"Humanizer",0x1D:"Chorus",0x1F:"AC Guitar Sim",0x26:"DC30",0x24:"Flanger117e",0x23:"Phaser90e",0x25:"Wah95e",0x27:"HeavyOctave"}

DELAY_OPTIONS = {0x00:"Digital",0x01:"Pan",0x02:"Stereo",0x03:"Dual Series",0x04:"Dual Parallel",0x05:"Dual L/R",0x06:"Reverse",0x07:"Analog",0x08:"Tape Echo",0x09:"Modulate",0x0A:"SDE3000"}

REVERB_OPTIONS = {0x00:"Ambience",0x01:"Room",0x02:"Hall 1",0x03:"Hall 2",0x04:"Plate",0x05:"Spring",0x06:"Modulate"}

scale_length = 100

class EffectPanel:
    channel = tk.IntVar(name="Channel", value=1)
    #channel_callback = channel_cb
    def __init__(self, parent, title, chTitle, iChannel, feature, featureCallback, colorCallback, levelCallback, toggleCallback):#, channelCallback):
        
        channelName = chTitle
        self.channelID = iChannel
        
        self.level = tk.IntVar(name=title + '.level', value=50)
        self.color = tk.IntVar(name=title + '.color', value=0)
        self.toggle = tk.IntVar(name=title + '.toggle', value=0)
        
        self.level.trace('w', self.change_level)
        self.color.trace('w',  self.change_color)
        self.toggle.trace('w',  self.change_toggle)
        
        self.color_cb = colorCallback
        self.level_cb = levelCallback
        self.toggle_cb = toggleCallback
        
        frame = tk.Frame(parent)
        
        self.panel_frame = tk.LabelFrame(frame, text=title) 
        self.green_button = tk.Radiobutton(self.panel_frame, padx=5,text="G", variable=self.color, indicatoron=False, value=0, width=4, fg="green")
        self.red_button = tk.Radiobutton(self.panel_frame, padx=5, text="R", variable=self.color, indicatoron=False, value=1, width=4, fg="red")
        self.orange_button = tk.Radiobutton(self.panel_frame, padx=5, text="O", variable=self.color, indicatoron=False, value=2, width=4, fg="orange")
        self.green_button.grid(row=0, column=0)
        self.red_button.grid(row=0, column=1)
        self.orange_button.grid(row=0, column=2)
        scale = Scale(self.panel_frame, variable=self.level, orient="horizontal", from_=0, to=127, length=scale_length)
        scale.grid(row=1, column=0, columnspan=3, sticky=W+E)
        button = Checkbutton(self.panel_frame, image=off_image, selectimage=on_image, indicatoron=False, onvalue=1, offvalue=0, variable=self.toggle)
        button.grid(row=2, column=0, sticky=N+W+S+E, columnspan=3)
        
        channel_frame = tk.LabelFrame(frame, text=channelName)
        chButton = Radiobutton(channel_frame, image=off_image, selectimage=on_image, indicatoron=False, value=self.channelID, variable=self.channel)
        chButton.pack() #grid(row=0, column=0, sticky=N+W+S+E)
        self.channelLabel = tk.Label(channel_frame, text=chTitle)
        self.channelLabel.pack()
        
        self.feature_frame = tk.LabelFrame(frame, text=feature)
        self.featureButton = Button(self.feature_frame, image=off_image, command=featureCallback)
        self.featureButton.pack()
        #self.featureLabel = tk.Label(text="Amp")
        #self.featureLabel.pack(side="bottom")
        
        self.feature_frame.grid(row=0, column=0, sticky=N+W+S+E)
        channel_frame.grid(row=1, column=0, sticky=N+W+S+E)
        self.panel_frame.grid(row=2, column=0, sticky=N+W+S+E)
        
        frame.pack(side="left")
               
    def change_color(self, *args):
        #varName = args[0]
        #print(varName + " = " + str(self.color.get()))
        self.color_cb(self.color.get())
        
    def change_level(self, *args):
        #varName = args[0]
        #print(varName + " = " + str(self.level.get()))
        amt = self.level.get() # 63+int((127.0-64.0)*(float(self.level.get()/100.0)))
        print(amt)
        self.level_cb(amt) #self.level.get())
 
    def change_toggle(self, *args):
        #varName = args[0]
        #print(varName + " = " + str(self.toggle.get()))
        self.toggle_cb(self.toggle.get())
        
    def change_feature(self, *args):
        #varName = args[0]
        #print(varName + " = " + str(self.toggle.get()))
        self.feature_cb(self.featureState.get())
    

class KatanaUI:
    def __init__(self, tkRoot):
        self.katana = katana.Katana('KATANA MIDI 1', 0, False)
        
        EffectPanel.channel.trace('w', self.channel_cb) 
        self.channelOffset = 0
        #self.ampSelect = ListBox(tkRoot)
        self.boostPanel = EffectPanel(tkRoot, "Boost", "Panel", 4, "Amp", self.amp_cb, self.boost_color_cb, self.boost_level_cb, self.boost_toggle_cb)#, self.channel_cb)
        self.modPanel = EffectPanel(tkRoot,  "Mod", "Ch1/5", 0, "Mute", self.mute_cb, self.mod_color_cb, self.mod_level_cb, self.mod_toggle_cb)#, self.channel_cb)
        self.fxPanel = EffectPanel(tkRoot,  "FX", "Ch2/6", 1, "A/B", self.ab_cb, self.fx_color_cb, self.fx_level_cb, self.fx_toggle_cb)#, self.channel_cb)
        self.delayPanel = EffectPanel(tkRoot,  "Delay", "Ch3/7", 2, "Tap", self.tap_cb, self.delay_color_cb, self.delay_level_cb, self.delay_toggle_cb)#, self.channel_cb)
        self.reverbPanel = EffectPanel(tkRoot,  "Reverb", "Ch4/8", 3, "Next", self.write_cb, self.reverb_color_cb, self.reverb_level_cb, self.reverb_toggle_cb)#, self.channel_cb)
        self.amp_selection = 0
        self.mute = 0
        self.ab = 0
        #self.amp_types = {0:'Acoustic', 1:'Clean', 2:'Brown', 3:'Lead', 4:'Crunch'}
        #amp_cycle = [0, 1, 2, 3, 4]
        self.amp_pool = cycle(AMP_LOOP_SHORT)
        self.amp_selection = next(self.amp_pool)

        self.color_assignments = []
        self.boost_pool = cycle(BOOST_OPTIONS.keys())
        self.mod_pool = cycle(EFFECT_OPTIONS.keys())
        self.fx_pool = cycle(EFFECT_OPTIONS.keys())
        self.delay_pool = cycle(DELAY_OPTIONS.keys())
        self.reverb_pool = cycle(REVERB_OPTIONS.keys())

        self.katana.busy = 0

        

    def read(self):
        print("Reading settings")
        self.katana.busy = 1
        self.amp_selection = self.katana.query_amp()
        print("Amp selection is " + str(self.amp_selection))
        test = next(self.amp_pool)
        while test != self.amp_selection:
            test = next(self.amp_pool)
        ampName = AMP_MAP[self.amp_selection]
        self.boostPanel.feature_frame.config(text="Amp: " + ampName)

        boostColor = self.katana.query_boost_color()
        self.boostPanel.color.set(boostColor)

        modColor = self.katana.query_mod_color()
        self.modPanel.color.set(modColor)

        fxColor = self.katana.query_fx_color()
        self.fxPanel.color.set(fxColor)

        delayColor = self.katana.query_delay_color()
        self.delayPanel.color.set(delayColor)

        reverbColor = self.katana.query_reverb_color()
        self.reverbPanel.color.set(reverbColor)
 
        print("Boost type:" + BOOST_OPTIONS[self.katana.query_boost_type()])
        print("Mod type:" + EFFECT_OPTIONS[self.katana.query_mod_type()])

        self.boostPanel.panel_frame.config(text="Boost: " + BOOST_OPTIONS[self.katana.query_boost_type()])
        self.modPanel.panel_frame.config(text="Mod: " + EFFECT_OPTIONS[self.katana.query_mod_type()])
        self.fxPanel.panel_frame.config(text="FX: " + EFFECT_OPTIONS[self.katana.query_fx_type()])
        self.delayPanel.panel_frame.config(text="Delay: " + DELAY_OPTIONS[self.katana.query_delay_type()])
        self.reverbPanel.panel_frame.config(text="Reverb: " + REVERB_OPTIONS[self.katana.query_reverb_type()])

        self.boostPanel.level.set(self.katana.query_boost_level())
        self.modPanel.level.set(self.katana.query_mod_level())
        self.fxPanel.level.set(self.katana.query_fx_level())
        self.delayPanel.level.set(self.katana.query_delay_level())
        self.reverbPanel.level.set(self.katana.query_reverb_level())

        self.boostPanel.toggle.set(self.katana.query_boost_sw())
        self.modPanel.toggle.set(self.katana.query_mod_sw())
        self.fxPanel.toggle.set(self.katana.query_fx_sw())
        self.delayPanel.toggle.set(self.katana.query_delay_sw())
        self.reverbPanel.toggle.set(self.katana.query_reverb_sw())

        self.set_patch_names(self.get_patch_names())

        self.color_assignments = self.katana.query_color_assignment()
        print("Boost Green Red Orange assigned to:")
        for i in range(0,3):
            print("  " + BOOST_OPTIONS[self.color_assignments[i]])
        print("Mod Green Red Orange assigned to:")
        for i in range(3,6):
            print("  " + EFFECT_OPTIONS[self.color_assignments[i]])
        print("FX Green Red Orange assigned to:")
        for i in range(6,9):
            print("  " + EFFECT_OPTIONS[self.color_assignments[i]])
        print("Delay Green Red Orange assigned to:")
        for i in range(9,12):
            print("  " + DELAY_OPTIONS[self.color_assignments[i]])
        print("Reverb Green Red Orange assigned to:")
        for i in range(12,15):
            print("  " + REVERB_OPTIONS[self.color_assignments[i]])

        self.katana.busy = 0
        
    def set_patch_names(self, names):
        self.boostPanel.channelLabel.config(text=names[0])
        self.modPanel.channelLabel.config(text=names[1 + self.channelOffset])
        self.fxPanel.channelLabel.config(text=names[2 + self.channelOffset])
        self.delayPanel.channelLabel.config(text=names[3 + self.channelOffset])
        self.reverbPanel.channelLabel.config(text=names[4 + self.channelOffset])
        
    def boost_level_cb(self, val):
        print("Boost level changed to " + str(val))
        #if self.katana.busy == 0:
        self.katana.set_boost(val)
        
    def mod_level_cb(self, val):
        print("Mod level changed to " + str(val))
        
    def fx_level_cb(self, val):
        print("Effect level changed to " + str(val))
        
    def delay_level_cb(self, val):
        print("Delay level changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.set_delay(val)
        
    def reverb_level_cb(self, val):
        print("Reverb level changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.set_reverb(val)
        
    def boost_color_cb(self, val):
        print("Boost color changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.boost_color(val)
            self.read()
        
    def mod_color_cb(self, val):
        print("Mod color changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.mod_color(val)       
            self.read() 

    def fx_color_cb(self, val):
        print("Effect color changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.fx_color(val)
            self.read()
        
    def delay_color_cb(self, val):
        print("Delay color changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.delay_color(val)
            self.read()
        
    def reverb_color_cb(self, val):
        print("Reverb color changed to " + str(val))
        if self.katana.busy == 0:
            self.katana.reverb_color(val)
            self.read()
        
    def boost_toggle_cb(self, val):
        print("Boost on/off changed to " + str(val))
        self.katana.set_boost_sw(val)
        
    def mod_toggle_cb(self, val):
        print("Mod on/off changed to " + str(val))
        self.katana.set_mod_sw(val)

    def fx_toggle_cb(self, val):
        print("Effect on/off changed to " + str(val))
        self.katana.set_fx_sw(val)

    def delay_toggle_cb(self, val):
        print("Delay on/off changed to " + str(val))
        self.katana.set_delay_sw(val)

    def reverb_toggle_cb(self, val):
        print("Reverb on/off changed to " + str(val))
        self.katana.set_reverb_sw(val)

    def channel_cb(self, *val):
        print("Channel changed to " + str(EffectPanel.channel.get() + self.channelOffset))
        if self.katana.busy == 0:
            ch = EffectPanel.channel.get() + self.channelOffset
            if ch > 8:
                ch = 4
            self.katana.select_channel(ch)
            self.read()
        
    def amp_cb(self):
        print("Amp callback")
        self.amp_selection = next(self.amp_pool)
        print(self.amp_selection)
        ampName = AMP_MAP[self.amp_selection]
        print(ampName)
        self.boostPanel.feature_frame.config(text="Amp: " + ampName)
        self.katana.set_amp(self.amp_selection)
        
    def mute_cb(self):
        if self.mute == 0:
            self.mute = 1
            self.katana.mute()
        else:
            self.mute = 0
            self.katana.unmute()
        print("Mute: " + str(self.mute))
        
        
    def ab_cb(self):
        if self.ab == 0:
            self.ab = 1
            print("A/B: B")
            self.fxPanel.feature_frame.config(text="A/B: B")
        else:
            self.ab = 0   
            print("A/B: A")
            self.fxPanel.feature_frame.config(text="A/B: A")
        self.channelOffset = self.ab*4
        self.set_patch_names(self.get_patch_names())
        
    def tap_cb(self):
        print("Tap")
        
    def write_cb(self):
        print("Next Effect")
        #which effect is enabled?
        if self.boostPanel.toggle.get():
            clr = self.boostPanel.color.get()
            sel_eff = self.color_assignments[clr]
            print("Current Boost is " + BOOST_OPTIONS[sel_eff])
            test = next(self.boost_pool)
            while test != sel_eff:
                test = next(self.boost_pool)
                print(str(test))
            test = next(self.boost_pool)
            print("Changed Boost to " + BOOST_OPTIONS[test])
            self.katana.assign_boost(clr, test)
        elif self.modPanel.toggle.get():
            clr = self.modPanel.color.get()
            sel_eff = self.color_assignments[3+clr]
            print("Current Mod is " + EFFECT_OPTIONS[sel_eff])
            test = next(self.mod_pool)
            while test != sel_eff:
                test = next(self.mod_pool)
                print(str(test))
            test = next(self.mod_pool)
            print("Changed Mod to " + EFFECT_OPTIONS[test])
            self.katana.assign_mod(clr, test)
        elif self.fxPanel.toggle.get():
            clr = self.fxPanel.color.get()
            sel_eff = self.color_assignments[6+clr]
            print("Current FX is " + EFFECT_OPTIONS[sel_eff])
            test = next(self.fx_pool)
            while test != sel_eff:
                test = next(self.fx_pool)
                print(str(test))
            test = next(self.fx_pool)
            print("Changed FX to " + EFFECT_OPTIONS[test])
            self.katana.assign_fx(clr, test)
        elif self.delayPanel.toggle.get():
            clr = self.delayPanel.color.get()
            sel_eff = self.color_assignments[9+clr]
            print("Current Delay is " + DELAY_OPTIONS[sel_eff])
            test = next(self.delay_pool)
            while test != sel_eff:
                test = next(self.delay_pool)
                print(str(test))
            test = next(self.delay_pool)
            print("Changed Delay to " + DELAY_OPTIONS[test])
            self.katana.assign_delay(clr, test)
        elif self.reverbPanel.toggle.get():
            clr = self.reverbPanel.color.get()
            sel_eff = self.color_assignments[12+clr]
            print("Current Reverb is " + REVERB_OPTIONS[sel_eff])
            test = next(self.reverb_pool)
            while test != sel_eff:
                test = next(self.reverb_pool)
                print(str(test))
            test = next(self.reverb_pool)
            print("Changed Reverb to " + REVERB_OPTIONS[test])
            self.katana.assign_reverb(clr, test)
        self.read()

    def get_patch_names(self):
        #names = ['Clean', 'Clean Twin', 'Crunch', 'Allman','Panel', 'Clean2', 'Clean Twin2', 'Crunch2', 'Allman2']
        return self.katana.get_patch_names()
        #return names

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

frame = Frame(width=480, height=320)

katanaUI = KatanaUI(frame)

#frame.pack_propagate(0)

frame.pack()

katanaUI.katana.assign_boost(1,0x0A)

katanaUI.read()



#boostPanel.color.set(2)
#fxPanel.level.set(100)
#reverbPanel.toggle.set(1)

#katanaUI.boostPanel.channelLabel.config(text="Clean")

#names = ['Clean', 'Clean Twin', 'Crunch', 'Allman', 'Clean2', 'Clean Twin2', 'Crunch2', 'Allman2']

#katanaUI.set_patch_names(names)

root.mainloop()
