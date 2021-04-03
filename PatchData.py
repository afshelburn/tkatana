MOD_WAH_PEDAL = (0x60,0x00,0x01,0x11)# MOD
FX_WAH_PEDAL = (0x60,0x00,0x03,0x11) # FX

MOD_EVH_WAH_PEDAL = (0x60,0x00,0x02,0x4c)
FX_EVH_WAH_PEDAL = (0x60,0x00,0x04,0x4c)

VOLUME_PEDAL = (0x60,0x00,0x05,0x61)

DELAY_TIME_PEDAL = (0x60,0x00,0x05,0x02)

MOD_TREMOLO_PEDAL = (0x60,0x00,0x02,0x14)
FX_TREMOLO_PEDAL = (0x60,0x00,0x04,0x14)

FX_BLEND_PEDAL = (0x60,0x00,0x05,0x59) #   INTEGER1x7        0   50   0   100   'PEDAL POS'            PRM_PEDAL_FX_PEDAL_BEND_PEDAL_POS
FX_BEND_PEDAL = (0x60,0x00,0x05,0x5a) #   INTEGER1x7        0   100   0   100   'EFFECT LEVEL'         PRM_PEDAL_FX_PEDAL_BEND_EFFECT_LE


QUERY_EFFECT_CHAIN = (0x60, 0x00, 0x06, 0x00)
WRITE_EFFECT_CHAIN = (0x60, 0x00, 0x07, 0x20)

#editable parts of the chain
#EFFECT_CHAIN = {'CS':0x00, 'CHB':0x03, 'FX3':0x0a, 'PDL':0x0b, 'NS2':0x0e, 'USB':0x10, 'CN_S':0x11, 'CN_M1_S2':0x12, 'CN_M':0x13, 'Send/Return':0x01, 'Amp':0x02, 'Equalizer':0x04, 'Mod':0x05, 'Effect':0x06, 'Delay1':0x07, 'Delay2':0x08, 'Reverb':0x09, 'Vol. Pedal':0x0c, 'Noise Gate':0x0d, 'Boost':0x0f}
EFFECT_CHAIN = {'Send/Return':0x01, 'Amp':0x02, 'Equalizer':0x04, 'Mod':0x05, 'Effect':0x06, 'Delay1':0x07, 'Delay2':0x08, 'Reverb':0x09, 'Vol. Pedal':0x0c, 'Noise Gate':0x0d, 'Boost':0x0f}
EFFECT_CHAIN_LABEL = {}
for key in EFFECT_CHAIN:
    #print(str(EFFECT_CHAIN[key]) + "=>" + key)
    EFFECT_CHAIN_LABEL[EFFECT_CHAIN[key]] = key
    
#non editable parts of the chain
EFFECT_CHAIN_PRE = (0x11,)
EFFECT_CHAIN_POST = (0x0e, 0x12, 0x00, 0x03, 0x0b, 0x0a, 0x13, 0x10)
        
BOOST_HW_BUTTON = 0
MOD_HW_BUTTON = 1
FX_HW_BUTTON = 2
DELAY_HW_BUTTON = 3
REVERB_HW_BUTTON = 4

PANEL_HW_BUTTON = 5
CH1_HW_BUTTON = 6
CH2_HW_BUTTON = 7
CH3_HW_BUTTON = 8
CH4_HW_BUTTON = 9

AMP_HW_BUTTON = 10
MUTE_HW_BUTTON = 14
AB_HW_BUTTON = 12
#TAP_HW_BUTTON = 13
EQ_HW_BUTTON = 13
NEXT_HW_BUTTON = 11

HW_BUTTONS = [BOOST_HW_BUTTON, MOD_HW_BUTTON, FX_HW_BUTTON, DELAY_HW_BUTTON, REVERB_HW_BUTTON]

CURRENT_PRESET_ADDR = ( 0x00, 0x01, 0x00, 0x00 )
CURRENT_PRESET_LEN = 0x02

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

BOOST_OPTIONS = {0x00:"Mid Boost",0x01:"Clean Boost",0x02:"Treble Boost",0x03:"Crunch OD",0x04:"Natural OD",0x05:"Warm OD",0x06:"Fat DS",0x08:"Metal DS",0x09:"Oct Fuzz",0x0A:"Blues Drive",0x0B:"Overdrive",0x0C:"T-Scream",0x0D:"Turbo OD",0x0E:"Distortion",0x0F:"Rat",0x10:"Guv DS",0x11:"DST+",0x12:"Metal Zone",0x13:"60s Fuzz",0x14:"Muff Fuzz"}
#took out 0x07:"Lead DS",

EFFECT_OPTIONS = {0x00:"T Wah",0x01:"Auto Wah",0x02:"Pedal Wah",0x03:"Comp",0x04:"Limiter",0x06:"Graphic EQ",0x07:"Parametric EQ",0x09:"Guitar Sim",0x0A:"Slow Gear",0x0B:"?",0x0C:"Wave Synth",0x0E:"Octave",0x0F:"Pitch Shifter",0x10:"Harmonist",0x12:"AC Processor",0x13:"Phaser",0x14:"Flanger",0x15:"Tremolo",0x16:"Rotary",0x17:"Uni-V",0x19:"Slicer",0x1A:"Vibrato",0x1B:"Ring Mod",0x1C:"Humanizer",0x1D:"Chorus",0x1F:"AC Guitar Sim",0x26:"DC30",0x24:"Flanger117e",0x23:"Phaser90e",0x25:"Wah95e",0x27:"HeavyOctave"}

DELAY_OPTIONS = {0x00:"Digital",0x01:"Pan",0x02:"Stereo",0x06:"Reverse",0x07:"Analog",0x08:"Tape Echo",0x09:"Modulate",0x0A:"SDE3000"}

REVERB_OPTIONS = {0x00:"Ambience",0x01:"Room",0x02:"Hall 1",0x03:"Hall 2",0x04:"Plate",0x05:"Spring",0x06:"Modulate"}

EFFECT_INDEX_TO_NAME = {'Boost':BOOST_OPTIONS,'Mod':EFFECT_OPTIONS,'FX':EFFECT_OPTIONS,'Delay':DELAY_OPTIONS,'Reverb':REVERB_OPTIONS}

EQ_SW = (0x00,0x00,0x00,0x10)
BOOST_SW = (0x60,0x00,0x00,0x10)
MOD_SW = (0x60,0x00,0x01,0x00)
FX_SW = (0x60,0x00,0x03,0x00)
DELAY_SW = (0x60,0x00,0x05,0x00)
REVERB_SW = (0x60,0x00,0x05,0x40)

BOOST_COLOR = (0x60, 0x00, 0x06, 0x39)
MOD_COLOR = (0x60, 0x00, 0x06, 0x3A)
FX_COLOR = (0x60, 0x00, 0x06, 0x3B)
DELAY_COLOR = (0x60, 0x00, 0x06, 0x3C)
REVERB_COLOR = (0x60, 0x00, 0x06, 0x3D)

BOOST_ASSIGN_COLOR = (0x60,0x00,0x06,0x24)
MOD_ASSIGN_COLOR = (0x60,0x00,0x06,0x27)
FX_ASSIGN_COLOR = (0x60,0x00,0x06,0x2A)
DELAY_ASSIGN_COLOR = (0x60,0x00,0x06,0x2D)
REVERB_ASSIGN_COLOR = (0x60,0x00,0x06,0x30)

COLOR_ASSIGN = [BOOST_ASSIGN_COLOR, MOD_ASSIGN_COLOR, FX_ASSIGN_COLOR, DELAY_ASSIGN_COLOR, REVERB_ASSIGN_COLOR]

COLOR_ASSIGN_MAP = {'Boost':BOOST_ASSIGN_COLOR,'Mod':MOD_ASSIGN_COLOR,'FX':FX_ASSIGN_COLOR,'Delay':DELAY_ASSIGN_COLOR,'Reverb':REVERB_ASSIGN_COLOR}

MOD_TYPE = (0x60,0x00,0x01,0x01)
BOOST_TYPE = (0x60,0x00,0x00,0x11)
FX_TYPE = (0x60,0x00,0x03,0x01)
DELAY_TYPE = (0x60,0x00,0x05,0x01)
REVERB_TYPE = (0x60,0x00,0x05,0x41)
EQ_TYPE = (0x00,0x00,0x00,0x11)

CHANNEL_EQ_TYPE = (0x60,0x00,0x00,0x41)
CHANNEL_EQ_SW = (0x60,0x00,0x00,0x40)

TOGGLES = [BOOST_SW, MOD_SW, FX_SW, DELAY_SW, REVERB_SW]
COLORS = [BOOST_COLOR, MOD_COLOR, FX_COLOR, DELAY_COLOR, REVERB_COLOR]
EFFECTS = [BOOST_TYPE, MOD_TYPE, FX_TYPE, DELAY_TYPE, REVERB_TYPE]

BOOST_LEVEL = (0x60,0x00,0x00,0x12)
DELAY_LEVEL = (0x60,0x00,0x05,0x06)
REVERB_LEVEL = (0x60,0x00,0x05,0x48)

MOD_LEVEL = (0x60,0x00,0x06,0x58)
FX_LEVEL = (0x60,0x00,0x06,0x59)

TOGGLE_MAP = {'Boost':BOOST_SW,'Mod':MOD_SW,'FX':FX_SW,'Delay':DELAY_SW,'Reverb':REVERB_SW}

COLOR_MAP = {'Boost':BOOST_COLOR,'Mod':MOD_COLOR,'FX':FX_COLOR,'Delay':DELAY_COLOR,'Reverb':REVERB_COLOR}

LEVELS = {"Boost":(BOOST_LEVEL,0,120),"Mod":(MOD_LEVEL,0,100),"FX":(FX_LEVEL,0,100),"Delay":(DELAY_LEVEL,0,100),"Reverb":(REVERB_LEVEL,0,100)}

QUERY_AMP = ( 0x60, 0x00, 0x00, 0x21 )

ParametricEQ = {'LOWCUT':(0, 0, 0, 17, (0x00, 0x00, 0x00, 0x13)),'LOWGAIN':(20, 0, -20, 20, (0x00, 0x00, 0x00, 0x14)),'LOW-MIDFREQ':(0, 13, 0, 27, (0x00, 0x00, 0x00, 0x15)),'LOW-MIDQ':(0, 1, 0, 5, (0x00, 0x00, 0x00, 0x16)),'LOW-MIDGAIN':(20, 0, -20, 20, (0x00, 0x00, 0x00, 0x17)),'HIGH-MIDFREQ':(0, 23, 0, 27, (0x00, 0x00, 0x00, 0x18)),'HIGH-MIDQ':(0, 1, 0, 5, (0x00, 0x00, 0x00, 0x19)),'HIGH-MIDGAIN':(20, 0, -20, 20, (0x00, 0x00, 0x00, 0x1a)),'HIGHGAIN':(20, 0, -20, 20, (0x00, 0x00, 0x00, 0x1b)),'HIGHCUT':(0, 14, 0, 14, (0x00, 0x00, 0x00, 0x1c)),'LEVEL':(20, 0, -20, 20, (0x00, 0x00, 0x00, 0x1d))}
GraphicEQ = {'31Hz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x1e)),'62Hz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x1f)),'125Hz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x20)),'250Hz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x21)),'500Hz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x22)),'1KHz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x23)),'2KHz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x24)),'4KHz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x25)),'8KHz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x26)),'16KHz':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x27)),'LEVEL':(24, 0, -24, 24, (0x00, 0x00, 0x00, 0x28))}

AmpPanel = {'Gain':(0, 60, 0, 120, (0x60, 0x00, 0x00, 0x22)),'Volume':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x28)),'Bass':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x24)),'Mid':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x25)),'Treble':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x26)),'Presence':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x27)),'Bright':(0, 0, 0, 1, (0x60, 0x00, 0x00, 0x51))}

ChParametricEQ = {'LOWCUT':(0, 0, 0, 17, (0x60, 0x00, 0x00, 0x42)),'LOWGAIN':(20, 0, -20, 20, (0x60, 0x00, 0x00, 0x43)),'LOW-MIDFREQ':(0, 13, 0, 27, (0x60, 0x00, 0x00, 0x44)),'LOW-MIDQ':(0, 1, 0, 5, (0x60, 0x00, 0x00, 0x45)),'LOW-MIDGAIN':(20, 0, -20, 20, (0x60, 0x00, 0x00, 0x46)),'HIGH-MIDFREQ':(0, 23, 0, 27, (0x60, 0x00, 0x00, 0x47)),'HIGH-MIDQ':(0, 1, 0, 5, (0x60, 0x00, 0x00, 0x48)),'HIGH-MIDGAIN':(20, 0, -20, 20, (0x60, 0x00, 0x00, 0x49)),'HIGHGAIN':(20, 0, -20, 20, (0x60, 0x00, 0x00, 0x4a)),'HIGHCUT':(0, 14, 0, 14, (0x60, 0x00, 0x00, 0x4b)),'LEVEL':(20, 0, -20, 20, (0x60, 0x00, 0x00, 0x4c))}
ChGraphicEQ = {'31Hz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x4d)),'62Hz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x4e)),'125Hz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x4f)),'250Hz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x50)),'500Hz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x51)),'1KHz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x52)),'2KHz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x53)),'4KHz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x54)),'8KHz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x55)),'16KHz':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x56)),'LEVEL':(24, 0, -24, 24, (0x60, 0x00, 0x00, 0x57))}

ChAmpPanel = {'Gain':(0, 60, 0, 120, (0x60, 0x00, 0x00, 0x22)),'Volume':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x28)),'Bass':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x24)),'Mid':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x25)),'Treble':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x26)),'Presence':(0, 50, 0, 100, (0x60, 0x00, 0x00, 0x27)),'Bright':(0, 0, 0, 1, (0x60, 0x00, 0x00, 0x51))}

chAddr = {0:(0x10,0x00),1:(0x10,0x01),2:(0x10,0x02),3:(0x10,0x03),4:(0x10,0x04),5:(0x10,0x05),6:(0x10,0x06),7:(0x10,0x07),8:(0x10,0x08)}




FX1_TWAH = []
FX1_AWAH = []
FX1_SUBWAH = []
FX1_ADCOMP = []
FX1_LIMITER = []
FX1_GEQ = []
FX1_PEQ = []
FX1_GTRSIM = []
FX1_SLOWGEAR = []
FX1_WAVESYN = []
FX1_OCTAVE = []
FX1_PITCHSHIFT = []
FX1_HARMONIST = []
FX1_ACPROCESS = []
FX1_PHASER = []
FX1_FLANGER = []
FX1_TREMOLO = []
FX1_ROTARY = []
FX1_UNI = []
FX1_SLICER = []
FX1_VIBRATO = []
FX1_RINGMOD = []
FX1_HUMANIZER = []
FX1_2x2CHORUS = []
FX1_ACSIM = []
FX1_EVH = []
FX1_DC30 = []
FX1_HEAVY = []

FX2_TWAH = []
FX2_AWAH = []
FX2_SUBWAH = []
FX2_ADCOMP = []
FX2_LIMITER = []
FX2_GEQ = []
FX2_PEQ = []
FX2_GTRSIM = []
FX2_SLOWGEAR = []
FX2_WAVESYN = []
FX2_OCTAVE = []
FX2_PITCHSHIFT = []
FX2_HARMONIST = []
FX2_ACPROCESS = []
FX2_PHASER = []
FX2_FLANGER = []
FX2_TREMOLO = []
FX2_ROTARY = []
FX2_UNI = []
FX2_SLICER = []
FX2_VIBRATO = []
FX2_RINGMOD = []
FX2_HUMANIZER = []
FX2_2x2CHORUS = []
FX2_ACSIM = []
FX2_EVH = []
FX2_DC30 = []
FX2_HEAVY = []


FX1_TWAH.append(('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x02),1))
FX1_TWAH.append(('POLARITY', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x03),1))
FX1_TWAH.append(('SENS', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x04),1))
FX1_TWAH.append(('FREQ', 0, 35, 0, 100, (0x60, 0x00, 0x01, 0x05),1))
FX1_TWAH.append(('PEAK', 0, 35, 0, 100, (0x60, 0x00, 0x01, 0x06),1))
FX1_TWAH.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x07),1))
FX1_TWAH.append(('EFFECTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x08),1))
FX1_AWAH.append(('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x09),1))
FX1_AWAH.append(('FREQ', 0, 35, 0, 100, (0x60, 0x00, 0x01, 0x0a),1))
FX1_AWAH.append(('PEAK', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x0b),1))
FX1_AWAH.append(('RATE', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x0c),1))
FX1_AWAH.append(('DEPTH', 0, 60, 0, 100, (0x60, 0x00, 0x01, 0x0d),1))
FX1_AWAH.append(('DIRETMIX', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x0e),1))
FX1_AWAH.append(('EFFECTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x0f),1))
FX1_SUBWAH.append(('TYPE', 0, 0, 0, 5, (0x60, 0x00, 0x01, 0x10),1))
FX1_SUBWAH.append(('PEDALPOS', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x11),1))
FX1_SUBWAH.append(('PEDALMIN', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x12),1))
FX1_SUBWAH.append(('PEDALMAX', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x13),1))
FX1_SUBWAH.append(('EFFECTLEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x14),1))
FX1_SUBWAH.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x15),1))
FX1_ADCOMP.append(('TYPE', 0, 0, 0, 6, (0x60, 0x00, 0x01, 0x16),1))
FX1_ADCOMP.append(('SUSTAIN', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x17),1))
FX1_ADCOMP.append(('ATTACK', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x18),1))
FX1_ADCOMP.append(('TONE', 50, 0, -50, 50, (0x60, 0x00, 0x01, 0x19),1))
FX1_ADCOMP.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x1a),1))
FX1_LIMITER.append(('TYPE', 0, 0, 0, 2, (0x60, 0x00, 0x01, 0x1b),1))
FX1_LIMITER.append(('ATTACK', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x1c),1))
FX1_LIMITER.append(('THRESHOLD', 0, 30, 0, 100, (0x60, 0x00, 0x01, 0x1d),1))
FX1_LIMITER.append(('RATIO', 0, 11, 0, 17, (0x60, 0x00, 0x01, 0x1e),1))
FX1_LIMITER.append(('RELEASE', 0, 10, 0, 100, (0x60, 0x00, 0x01, 0x1f),1))
FX1_LIMITER.append(('LEVEL', 0, 30, 0, 100, (0x60, 0x00, 0x01, 0x20),1))
FX1_GEQ.append(('31Hz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x21),1))
FX1_GEQ.append(('62Hz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x22),1))
FX1_GEQ.append(('125Hz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x23),1))
FX1_GEQ.append(('250Hz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x24),1))
FX1_GEQ.append(('500Hz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x25),1))
FX1_GEQ.append(('1kHz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x26),1))
FX1_GEQ.append(('2kHz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x27),1))
FX1_GEQ.append(('4kHz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x28),1))
FX1_GEQ.append(('8kHz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x29),1))
FX1_GEQ.append(('16kHz', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x2a),1))
FX1_GEQ.append(('LEVEL', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x2b),1))
FX1_PEQ.append(('LOWCUT', 0, 0, 0, 17, (0x60, 0x00, 0x01, 0x2c),1))
FX1_PEQ.append(('LOWGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x2d),1))
FX1_PEQ.append(('LOW-MIDFREQ', 0, 13, 0, 27, (0x60, 0x00, 0x01, 0x2e),1))
FX1_PEQ.append(('LOW-MIDQ', 0, 1, 0, 5, (0x60, 0x00, 0x01, 0x2f),1))
FX1_PEQ.append(('LOW-MIDGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x30),1))
FX1_PEQ.append(('HIGH-MIDFREQ', 0, 23, 0, 27, (0x60, 0x00, 0x01, 0x31),1))
FX1_PEQ.append(('HIGH-MIDQ', 0, 1, 0, 5, (0x60, 0x00, 0x01, 0x32),1))
FX1_PEQ.append(('HIGH-MIDGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x33),1))
FX1_PEQ.append(('HIGHGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x34),1))
FX1_PEQ.append(('HIGHCUT', 0, 14, 0, 14, (0x60, 0x00, 0x01, 0x35),1))
FX1_PEQ.append(('LEVEL', 20, 0, -20, 20, (0x60, 0x00, 0x01, 0x36),1))
FX1_GTRSIM.append(('TYPE', 0, 0, 0, 7, (0x60, 0x00, 0x01, 0x37),1))
FX1_GTRSIM.append(('LOW', 50, 0, -50, 50, (0x60, 0x00, 0x01, 0x38),1))
FX1_GTRSIM.append(('HIGH', 50, 0, -50, 50, (0x60, 0x00, 0x01, 0x39),1))
FX1_GTRSIM.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x3a),1))
FX1_GTRSIM.append(('BODY', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x3b),1))
FX1_SLOWGEAR.append(('SENS', 0, 45, 0, 100, (0x60, 0x00, 0x01, 0x3c),1))
FX1_SLOWGEAR.append(('RISETIME', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x3d),1))
FX1_SLOWGEAR.append(('LEVEL', 0, 60, 0, 100, (0x60, 0x00, 0x01, 0x3e),1))
FX1_WAVESYN.append(('WAVE', 0, 0, 0, 1, (0x60, 0x00, 0x01, 0x3f),1))
FX1_WAVESYN.append(('CUTOFF', 0, 40, 0, 100, (0x60, 0x00, 0x01, 0x40),1))
FX1_WAVESYN.append(('RESONANCE', 0, 30, 0, 100, (0x60, 0x00, 0x01, 0x41),1))
FX1_WAVESYN.append(('FILTERSENS', 0, 40, 0, 100, (0x60, 0x00, 0x01, 0x42),1))
FX1_WAVESYN.append(('FILTERDECAY', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x43),1))
FX1_WAVESYN.append(('FILTERDEPTH', 0, 50, 0, 100, (0x60, 0x00, 0x01, 0x44),1))
FX1_WAVESYN.append(('SYNTHLEVEL', 0, 25, 0, 100, (0x60, 0x00, 0x01, 0x45),1))
FX1_WAVESYN.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x46),1))
FX1_OCTAVE.append(('RANGE', 0, 0, 0, 3, (0x60, 0x00, 0x01, 0x47),1))
FX1_OCTAVE.append(('EFFECTLEVEL', 0, 62, 0, 100, (0x60, 0x00, 0x01, 0x48),1))
FX1_OCTAVE.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x49),1))
FX1_PITCHSHIFT.append(('VOICE', 0, 0, 0, 1, (0x60, 0x00, 0x01, 0x4a),1))
FX1_PITCHSHIFT.append(('PS1:MODE', 0, 1, 0, 3, (0x60, 0x00, 0x01, 0x4b),1))
FX1_PITCHSHIFT.append(('PS1:PITCH', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x4c),1))
FX1_PITCHSHIFT.append(('PS1:FINE', 50, 10, -50, 50, (0x60, 0x00, 0x01, 0x4d),1))
FX1_PITCHSHIFT.append(('PS1:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x01, 0x4e),2))
FX1_PITCHSHIFT.append(('PS1:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x01, 0x50),1))
FX1_PITCHSHIFT.append(('PS2:MODE', 0, 1, 0, 3, (0x60, 0x00, 0x01, 0x51),1))
FX1_PITCHSHIFT.append(('PS2:PITCH', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x52),1))
FX1_PITCHSHIFT.append(('PS2:FINE', 50, -10, -50, 50, (0x60, 0x00, 0x01, 0x53),1))
FX1_PITCHSHIFT.append(('PS2:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x01, 0x54),2))
FX1_PITCHSHIFT.append(('PS2:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x01, 0x56),1))
FX1_PITCHSHIFT.append(('PS1:FEEDBACK', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x57),1))
FX1_PITCHSHIFT.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x58),1))
FX1_HARMONIST.append(('VOICE', 0, 1, 0, 1, (0x60, 0x00, 0x01, 0x59),1))
FX1_HARMONIST.append(('HR1:HARMONY', 0, 12, 0, 29, (0x60, 0x00, 0x01, 0x5a),1))
FX1_HARMONIST.append(('HR1:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x01, 0x5b),2))
FX1_HARMONIST.append(('HR1:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x01, 0x5d),1))
FX1_HARMONIST.append(('HR2:HARMONY', 0, 7, 0, 29, (0x60, 0x00, 0x01, 0x5e),1))
FX1_HARMONIST.append(('HR2:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x01, 0x5f),2))
FX1_HARMONIST.append(('HR2:LEVEL', 0, 80, 0, 100, (0x60, 0x00, 0x01, 0x61),1))
FX1_HARMONIST.append(('HR1:FEEDBACK', 0, 0, 0, 100, (0x60, 0x00, 0x01, 0x62),1))
FX1_HARMONIST.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x01, 0x63),1))
FX1_HARMONIST.append(('HR1:C', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x64),1))
FX1_HARMONIST.append(('HR1:Db', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x65),1))
FX1_HARMONIST.append(('HR1:D', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x66),1))
FX1_HARMONIST.append(('HR1:Eb', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x67),1))
FX1_HARMONIST.append(('HR1:E', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x68),1))
FX1_HARMONIST.append(('HR1:F', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x69),1))
FX1_HARMONIST.append(('HR1:F#', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6a),1))
FX1_HARMONIST.append(('HR1:G', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6b),1))
FX1_HARMONIST.append(('HR1:Ab', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6c),1))
FX1_HARMONIST.append(('HR1:A', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6d),1))
FX1_HARMONIST.append(('HR1:Bb', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6e),1))
FX1_HARMONIST.append(('HR1:B', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x6f),1))
FX1_HARMONIST.append(('HR2:C', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x70),1))
FX1_HARMONIST.append(('HR2:Db', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x71),1))
FX1_HARMONIST.append(('HR2:D', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x72),1))
FX1_HARMONIST.append(('HR2:Eb', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x73),1))
FX1_HARMONIST.append(('HR2:E', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x74),1))
FX1_HARMONIST.append(('HR2:F', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x75),1))
FX1_HARMONIST.append(('HR2:F#', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x76),1))
FX1_HARMONIST.append(('HR2:G', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x77),1))
FX1_HARMONIST.append(('HR2:Ab', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x78),1))
FX1_HARMONIST.append(('HR2:A', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x79),1))
FX1_HARMONIST.append(('HR2:Bb', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x7a),1))
FX1_HARMONIST.append(('HR2:B', 24, 0, -24, 24, (0x60, 0x00, 0x01, 0x7b),1))
FX1_ACPROCESS.append(('TYPE', 0, 1, 0, 3, (0x60, 0x00, 0x01, 0x7c),1))
FX1_ACPROCESS.append(('BASS', 50, 0, -50, 50, (0x60, 0x00, 0x01, 0x7d),1))
FX1_ACPROCESS.append(('MIDDLE', 50, 0, -50, 50, (0x60, 0x00, 0x01, 0x7e),1))
FX1_ACPROCESS.append(('MIDDLEFREQ', 0, 16, 0, 27, (0x60, 0x00, 0x01, 0x7f),1))
FX1_ACPROCESS.append(('TREBLE'          , 50, 0, -50, 50, (0x60, 0x00, 0x02, 0x00),1))
FX1_ACPROCESS.append(('PRESENCE'        , 50, 0, -50, 50, (0x60, 0x00, 0x02, 0x01),1))
FX1_ACPROCESS.append(('LEVEL'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x02),1))
FX1_PHASER.append(('TYPE'            , 0, 0, 0, 3, (0x60, 0x00, 0x02, 0x03),1))
FX1_PHASER.append(('RATE'            , 0, 70, 0, 100, (0x60, 0x00, 0x02, 0x04),1))
FX1_PHASER.append(('DEPTH'           , 0, 40, 0, 100, (0x60, 0x00, 0x02, 0x05),1))
FX1_PHASER.append(('MANUAL'          , 0, 55, 0, 100, (0x60, 0x00, 0x02, 0x06),1))
FX1_PHASER.append(('RESONANCE'       , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x07),1))
FX1_PHASER.append(('STEP RATE'       , 1, -1, -1, 100, (0x60, 0x00, 0x02, 0x08),1))
FX1_PHASER.append(('EFFECT LEVEL'    , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x09),1))
FX1_PHASER.append(('DIRECT MIX'      , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x0a),1))
FX1_FLANGER.append(('RATE'            , 0, 31, 0, 100, (0x60, 0x00, 0x02, 0x0b),1))
FX1_FLANGER.append(('DEPTH'           , 0, 40, 0, 100, (0x60, 0x00, 0x02, 0x0c),1))
FX1_FLANGER.append(('MANUAL'          , 0, 82, 0, 100, (0x60, 0x00, 0x02, 0x0d),1))
FX1_FLANGER.append(('RESONANCE'       , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x0e),1))
FX1_FLANGER.append(('LOW CUT'         , 0, 0, 0, 10, (0x60, 0x00, 0x02, 0x10),1))
FX1_FLANGER.append(('EFFECT LEVEL'    , 0, 60, 0, 100, (0x60, 0x00, 0x02, 0x11),1))
FX1_FLANGER.append(('DIRECT MIX'      , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x12),1))
FX1_TREMOLO.append(('WAVE SHAPE'      , 0, 70, 0, 100, (0x60, 0x00, 0x02, 0x13),1))
FX1_TREMOLO.append(('RATE'            , 0, 85, 0, 100, (0x60, 0x00, 0x02, 0x14),1))
FX1_TREMOLO.append(('DEPTH'           , 0, 65, 0, 100, (0x60, 0x00, 0x02, 0x15),1))
FX1_TREMOLO.append(('LEVEL'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x16),1))
FX1_ROTARY.append(('RATE'            , 0, 85, 0, 100, (0x60, 0x00, 0x02, 0x19),1))
FX1_ROTARY.append(('DEPTH'           , 0, 60, 0, 100, (0x60, 0x00, 0x02, 0x1c),1))
FX1_ROTARY.append(('LEVEL'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x1d),1))
FX1_UNI.append(('RATE'            , 0, 70, 0, 100, (0x60, 0x00, 0x02, 0x1e),1))
FX1_UNI.append(('DEPTH'           , 0, 60, 0, 100, (0x60, 0x00, 0x02, 0x1f),1))
FX1_UNI.append(('LEVEL'           , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x20),1))
FX1_SLICER.append(('PATTERN'         , 0, 0, 0, 19, (0x60, 0x00, 0x02, 0x21),1))
FX1_SLICER.append(('RATE'            , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x22),1))
FX1_SLICER.append(('TRIGGER SENS'    , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x23),1))
FX1_SLICER.append(('EFFECT LEVEL'    , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x24),1))
FX1_SLICER.append(('DIRECT MIX'      , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x25),1))
FX1_VIBRATO.append(('RATE'            , 0, 80, 0, 100, (0x60, 0x00, 0x02, 0x26),1))
FX1_VIBRATO.append(('DEPTH'           , 0, 45, 0, 100, (0x60, 0x00, 0x02, 0x27),1))
FX1_VIBRATO.append(('LEVEL'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x2a),1))
FX1_RINGMOD.append(('MODE'            , 0, 0, 0, 1, (0x60, 0x00, 0x02, 0x2b),1))
FX1_RINGMOD.append(('FREQUENCY'       , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x2c),1))
FX1_RINGMOD.append(('EFFECT LEVEL'    , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x2d),1))
FX1_RINGMOD.append(('DIRECT MIX'      , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x2e),1))
FX1_HUMANIZER.append(('MODE'            , 0, 1, 0, 1, (0x60, 0x00, 0x02, 0x2f),1))
FX1_HUMANIZER.append(('VOWEL1'          , 0, 0, 0, 4, (0x60, 0x00, 0x02, 0x30),1))
FX1_HUMANIZER.append(('VOWEL2'          , 0, 2, 0, 4, (0x60, 0x00, 0x02, 0x31),1))
FX1_HUMANIZER.append(('SENS'            , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x32),1))
FX1_HUMANIZER.append(('RATE'            , 0, 80, 0, 100, (0x60, 0x00, 0x02, 0x33),1))
FX1_HUMANIZER.append(('DEPTH'           , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x34),1))
FX1_HUMANIZER.append(('MANUAL'          , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x35),1))
FX1_HUMANIZER.append(('LEVEL'           , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x36),1))
FX1_2x2CHORUS.append(('XOVER FREQUENCY' , 0, 4, 0, 16, (0x60, 0x00, 0x02, 0x37),1))
FX1_2x2CHORUS.append(('LOW RATE'        , 0, 43, 0, 100, (0x60, 0x00, 0x02, 0x38),1))
FX1_2x2CHORUS.append(('LOW DEPTH'       , 0, 46, 0, 100, (0x60, 0x00, 0x02, 0x39),1))
FX1_2x2CHORUS.append(('LOW PRE DELAY'   , 0, 3, 0, 80, (0x60, 0x00, 0x02, 0x3a),1))
FX1_2x2CHORUS.append(('LOW LEVEL'       , 0, 75, 0, 100, (0x60, 0x00, 0x02, 0x3b),1))
FX1_2x2CHORUS.append(('HIGH RATE'       , 0, 33, 0, 100, (0x60, 0x00, 0x02, 0x3c),1))
FX1_2x2CHORUS.append(('HIGH DEPTH'      , 0, 48, 0, 100, (0x60, 0x00, 0x02, 0x3d),1))
FX1_2x2CHORUS.append(('HIGH PRE DELAY'  , 0, 3, 0, 80, (0x60, 0x00, 0x02, 0x3e),1))
FX1_2x2CHORUS.append(('HIGH LEVEL'      , 0, 65, 0, 100, (0x60, 0x00, 0x02, 0x3f),1))
FX1_2x2CHORUS.append(('DIRECT MIX'      , 0, 80, 0, 100, (0x60, 0x00, 0x02, 0x40),1))
FX1_ACSIM.append(('HIGH'            , 50, 0, -50, 50, (0x60, 0x00, 0x02, 0x41),1))
FX1_ACSIM.append(('BODY'            , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x42),1))
FX1_ACSIM.append(('LOW'             , 50, 0, -50, 50, (0x60, 0x00, 0x02, 0x43),1))
FX1_ACSIM.append(('LEVEL'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x45),1))
FX1_EVH.append(('SCRIPT'          , 0, 1, 0, 1, (0x60, 0x00, 0x02, 0x46),1))
FX1_EVH.append(('SPEED'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x47),1))
FX1_EVH.append(('MANUAL'          , 0, 45, 0, 100, (0x60, 0x00, 0x02, 0x48),1))
FX1_EVH.append(('WIDTH'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x49),1))
FX1_EVH.append(('SPEED'           , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x4a),1))
FX1_EVH.append(('REGEN.'          , 0, 80, 0, 100, (0x60, 0x00, 0x02, 0x4b),1))
FX1_EVH.append(('PEDAL POS'       , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x4c),1))
FX1_EVH.append(('PEDAL MIN'       , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x4d),1))
FX1_EVH.append(('PEDAL MAX'       , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x4e),1))
FX1_EVH.append(('EFFECT LEVEL'    , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x4f),1))
FX1_EVH.append(('DIRECT MIX'      , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x50),1))
FX1_DC30.append(('SELECT'          , 0, 0, 0, 1, (0x60, 0x00, 0x02, 0x51),1))
FX1_DC30.append(('INPUT VOLUME'    , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x52),1))
FX1_DC30.append(('CHORUS INTENSITY', 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x53),1))
FX1_DC30.append(('ECHO REPEAT RATE', 0, 400, 40, 600, (0x60, 0x00, 0x02, 0x54),2))
FX1_DC30.append(('ECHO INTENSISTY' , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x56),1))
FX1_DC30.append(('ECHO VOLUME'     , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x57),1))
FX1_DC30.append(('TONE'            , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x58),1))
FX1_DC30.append(('OUTPUT'          , 0, 0, 0, 1, (0x60, 0x00, 0x02, 0x59),1))
FX1_HEAVY.append(('1OCT LEVEL'      , 0, 50, 0, 100, (0x60, 0x00, 0x02, 0x5a),1))
FX1_HEAVY.append(('2OCT LEVEL'      , 0, 0, 0, 100, (0x60, 0x00, 0x02, 0x5b),1))
FX1_HEAVY.append(('DIRECT MIX'      , 0, 100, 0, 100, (0x60, 0x00, 0x02, 0x5c),1))

FX2_TWAH.append(('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x03, 0x02),1))
FX2_TWAH.append(('POLARITY', 0, 1, 0, 1, (0x60, 0x00, 0x03, 0x03),1))
FX2_TWAH.append(('SENS', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x04),1))
FX2_TWAH.append(('FREQ', 0, 35, 0, 100, (0x60, 0x00, 0x03, 0x05),1))
FX2_TWAH.append(('PEAK', 0, 35, 0, 100, (0x60, 0x00, 0x03, 0x06),1))
FX2_TWAH.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x07),1))
FX2_TWAH.append(('EFFECTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x08),1))
FX2_AWAH.append(('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x03, 0x09),1))
FX2_AWAH.append(('FREQ', 0, 35, 0, 100, (0x60, 0x00, 0x03, 0x0a),1))
FX2_AWAH.append(('PEAK', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x0b),1))
FX2_AWAH.append(('RATE', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x0c),1))
FX2_AWAH.append(('DEPTH', 0, 60, 0, 100, (0x60, 0x00, 0x03, 0x0d),1))
FX2_AWAH.append(('DIRETMIX', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x0e),1))
FX2_AWAH.append(('EFFECTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x0f),1))
FX2_SUBWAH.append(('TYPE', 0, 0, 0, 5, (0x60, 0x00, 0x03, 0x10),1))
FX2_SUBWAH.append(('PEDALPOS', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x11),1))
FX2_SUBWAH.append(('PEDALMIN', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x12),1))
FX2_SUBWAH.append(('PEDALMAX', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x13),1))
FX2_SUBWAH.append(('EFFECTLEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x14),1))
FX2_SUBWAH.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x15),1))
FX2_ADCOMP.append(('TYPE', 0, 0, 0, 6, (0x60, 0x00, 0x03, 0x16),1))
FX2_ADCOMP.append(('SUSTAIN', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x17),1))
FX2_ADCOMP.append(('ATTACK', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x18),1))
FX2_ADCOMP.append(('TONE', 50, 0, -50, 50, (0x60, 0x00, 0x03, 0x19),1))
FX2_ADCOMP.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x1a),1))
FX2_LIMITER.append(('TYPE', 0, 0, 0, 2, (0x60, 0x00, 0x03, 0x1b),1))
FX2_LIMITER.append(('ATTACK', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x1c),1))
FX2_LIMITER.append(('THRESHOLD', 0, 30, 0, 100, (0x60, 0x00, 0x03, 0x1d),1))
FX2_LIMITER.append(('RATIO', 0, 11, 0, 17, (0x60, 0x00, 0x03, 0x1e),1))
FX2_LIMITER.append(('RELEASE', 0, 10, 0, 100, (0x60, 0x00, 0x03, 0x1f),1))
FX2_LIMITER.append(('LEVEL', 0, 30, 0, 100, (0x60, 0x00, 0x03, 0x20),1))
FX2_GEQ.append(('31Hz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x21),1))
FX2_GEQ.append(('62Hz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x22),1))
FX2_GEQ.append(('125Hz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x23),1))
FX2_GEQ.append(('250Hz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x24),1))
FX2_GEQ.append(('500Hz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x25),1))
FX2_GEQ.append(('1kHz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x26),1))
FX2_GEQ.append(('2kHz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x27),1))
FX2_GEQ.append(('4kHz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x28),1))
FX2_GEQ.append(('8kHz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x29),1))
FX2_GEQ.append(('16kHz', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x2a),1))
FX2_GEQ.append(('LEVEL', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x2b),1))
FX2_PEQ.append(('LOWCUT', 0, 0, 0, 17, (0x60, 0x00, 0x03, 0x2c),1))
FX2_PEQ.append(('LOWGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x2d),1))
FX2_PEQ.append(('LOW-MIDFREQ', 0, 13, 0, 27, (0x60, 0x00, 0x03, 0x2e),1))
FX2_PEQ.append(('LOW-MIDQ', 0, 1, 0, 5, (0x60, 0x00, 0x03, 0x2f),1))
FX2_PEQ.append(('LOW-MIDGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x30),1))
FX2_PEQ.append(('HIGH-MIDFREQ', 0, 23, 0, 27, (0x60, 0x00, 0x03, 0x31),1))
FX2_PEQ.append(('HIGH-MIDQ', 0, 1, 0, 5, (0x60, 0x00, 0x03, 0x32),1))
FX2_PEQ.append(('HIGH-MIDGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x33),1))
FX2_PEQ.append(('HIGHGAIN', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x34),1))
FX2_PEQ.append(('HIGHCUT', 0, 14, 0, 14, (0x60, 0x00, 0x03, 0x35),1))
FX2_PEQ.append(('LEVEL', 20, 0, -20, 20, (0x60, 0x00, 0x03, 0x36),1))
FX2_GTRSIM.append(('TYPE', 0, 0, 0, 7, (0x60, 0x00, 0x03, 0x37),1))
FX2_GTRSIM.append(('LOW', 50, 0, -50, 50, (0x60, 0x00, 0x03, 0x38),1))
FX2_GTRSIM.append(('HIGH', 50, 0, -50, 50, (0x60, 0x00, 0x03, 0x39),1))
FX2_GTRSIM.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x3a),1))
FX2_GTRSIM.append(('BODY', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x3b),1))
FX2_SLOWGEAR.append(('SENS', 0, 45, 0, 100, (0x60, 0x00, 0x03, 0x3c),1))
FX2_SLOWGEAR.append(('RISETIME', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x3d),1))
FX2_SLOWGEAR.append(('LEVEL', 0, 60, 0, 100, (0x60, 0x00, 0x03, 0x3e),1))
FX2_WAVESYN.append(('WAVE', 0, 0, 0, 1, (0x60, 0x00, 0x03, 0x3f),1))
FX2_WAVESYN.append(('CUTOFF', 0, 40, 0, 100, (0x60, 0x00, 0x03, 0x40),1))
FX2_WAVESYN.append(('RESONANCE', 0, 30, 0, 100, (0x60, 0x00, 0x03, 0x41),1))
FX2_WAVESYN.append(('FILTERSENS', 0, 40, 0, 100, (0x60, 0x00, 0x03, 0x42),1))
FX2_WAVESYN.append(('FILTERDECAY', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x43),1))
FX2_WAVESYN.append(('FILTERDEPTH', 0, 50, 0, 100, (0x60, 0x00, 0x03, 0x44),1))
FX2_WAVESYN.append(('SYNTHLEVEL', 0, 25, 0, 100, (0x60, 0x00, 0x03, 0x45),1))
FX2_WAVESYN.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x46),1))
FX2_OCTAVE.append(('RANGE', 0, 0, 0, 3, (0x60, 0x00, 0x03, 0x47),1))
FX2_OCTAVE.append(('EFFECTLEVEL', 0, 62, 0, 100, (0x60, 0x00, 0x03, 0x48),1))
FX2_OCTAVE.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x49),1))
FX2_PITCHSHIFT.append(('VOICE', 0, 0, 0, 1, (0x60, 0x00, 0x03, 0x4a),1))
FX2_PITCHSHIFT.append(('PS1:MODE', 0, 1, 0, 3, (0x60, 0x00, 0x03, 0x4b),1))
FX2_PITCHSHIFT.append(('PS1:PITCH', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x4c),1))
FX2_PITCHSHIFT.append(('PS1:FINE', 50, 10, -50, 50, (0x60, 0x00, 0x03, 0x4d),1))
FX2_PITCHSHIFT.append(('PS1:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x03, 0x4e),2))
FX2_PITCHSHIFT.append(('PS1:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x03, 0x50),1))
FX2_PITCHSHIFT.append(('PS2:MODE', 0, 1, 0, 3, (0x60, 0x00, 0x03, 0x51),1))
FX2_PITCHSHIFT.append(('PS2:PITCH', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x52),1))
FX2_PITCHSHIFT.append(('PS2:FINE', 50, -10, -50, 50, (0x60, 0x00, 0x03, 0x53),1))
FX2_PITCHSHIFT.append(('PS2:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x03, 0x54),2))
FX2_PITCHSHIFT.append(('PS2:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x03, 0x56),1))
FX2_PITCHSHIFT.append(('PS1:FEEDBACK', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x57),1))
FX2_PITCHSHIFT.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x58),1))
FX2_HARMONIST.append(('VOICE', 0, 1, 0, 1, (0x60, 0x00, 0x03, 0x59),1))
FX2_HARMONIST.append(('HR1:HARMONY', 0, 12, 0, 29, (0x60, 0x00, 0x03, 0x5a),1))
FX2_HARMONIST.append(('HR1:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x03, 0x5b),2))
FX2_HARMONIST.append(('HR1:LEVEL', 0, 70, 0, 100, (0x60, 0x00, 0x03, 0x5d),1))
FX2_HARMONIST.append(('HR2:HARMONY', 0, 7, 0, 29, (0x60, 0x00, 0x03, 0x5e),1))
FX2_HARMONIST.append(('HR2:PREDELAY', 0, 0, 0, 300, (0x60, 0x00, 0x03, 0x5f),2))
FX2_HARMONIST.append(('HR2:LEVEL', 0, 80, 0, 100, (0x60, 0x00, 0x03, 0x61),1))
FX2_HARMONIST.append(('HR1:FEEDBACK', 0, 0, 0, 100, (0x60, 0x00, 0x03, 0x62),1))
FX2_HARMONIST.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x03, 0x63),1))
FX2_HARMONIST.append(('HR1:C', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x64),1))
FX2_HARMONIST.append(('HR1:Db', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x65),1))
FX2_HARMONIST.append(('HR1:D', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x66),1))
FX2_HARMONIST.append(('HR1:Eb', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x67),1))
FX2_HARMONIST.append(('HR1:E', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x68),1))
FX2_HARMONIST.append(('HR1:F', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x69),1))
FX2_HARMONIST.append(('HR1:F#', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6a),1))
FX2_HARMONIST.append(('HR1:G', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6b),1))
FX2_HARMONIST.append(('HR1:Ab', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6c),1))
FX2_HARMONIST.append(('HR1:A', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6d),1))
FX2_HARMONIST.append(('HR1:Bb', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6e),1))
FX2_HARMONIST.append(('HR1:B', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x6f),1))
FX2_HARMONIST.append(('HR2:C', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x70),1))
FX2_HARMONIST.append(('HR2:Db', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x71),1))
FX2_HARMONIST.append(('HR2:D', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x72),1))
FX2_HARMONIST.append(('HR2:Eb', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x73),1))
FX2_HARMONIST.append(('HR2:E', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x74),1))
FX2_HARMONIST.append(('HR2:F', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x75),1))
FX2_HARMONIST.append(('HR2:F#', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x76),1))
FX2_HARMONIST.append(('HR2:G', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x77),1))
FX2_HARMONIST.append(('HR2:Ab', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x78),1))
FX2_HARMONIST.append(('HR2:A', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x79),1))
FX2_HARMONIST.append(('HR2:Bb', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x7a),1))
FX2_HARMONIST.append(('HR2:B', 24, 0, -24, 24, (0x60, 0x00, 0x03, 0x7b),1))
FX2_ACPROCESS.append(('TYPE', 0, 1, 0, 3, (0x60, 0x00, 0x03, 0x7c),1))
FX2_ACPROCESS.append(('BASS', 50, 0, -50, 50, (0x60, 0x00, 0x03, 0x7d),1))
FX2_ACPROCESS.append(('MIDDLE', 50, 0, -50, 50, (0x60, 0x00, 0x03, 0x7e),1))
FX2_ACPROCESS.append(('MIDDLEFREQ', 0, 16, 0, 27, (0x60, 0x00, 0x03, 0x7f),1))
FX2_ACPROCESS.append(('TREBLE', 50, 0, -50, 50, (0x60, 0x00, 0x04, 0x00),1))
FX2_ACPROCESS.append(('PRESENCE', 50, 0, -50, 50, (0x60, 0x00, 0x04, 0x01),1))
FX2_ACPROCESS.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x02),1))
FX2_PHASER.append(('TYPE', 0, 0, 0, 3, (0x60, 0x00, 0x04, 0x03),1))
FX2_PHASER.append(('RATE', 0, 70, 0, 100, (0x60, 0x00, 0x04, 0x04),1))
FX2_PHASER.append(('DEPTH', 0, 40, 0, 100, (0x60, 0x00, 0x04, 0x05),1))
FX2_PHASER.append(('MANUAL', 0, 55, 0, 100, (0x60, 0x00, 0x04, 0x06),1))
FX2_PHASER.append(('RESONANCE', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x07),1))
FX2_PHASER.append(('STEPRATE', 1, -1, -1, 100, (0x60, 0x00, 0x04, 0x08),1))
FX2_PHASER.append(('EFFECTLEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x09),1))
FX2_PHASER.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x0a),1))
FX2_FLANGER.append(('RATE', 0, 31, 0, 100, (0x60, 0x00, 0x04, 0x0b),1))
FX2_FLANGER.append(('DEPTH', 0, 40, 0, 100, (0x60, 0x00, 0x04, 0x0c),1))
FX2_FLANGER.append(('MANUAL', 0, 82, 0, 100, (0x60, 0x00, 0x04, 0x0d),1))
FX2_FLANGER.append(('RESONANCE', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x0e),1))
FX2_FLANGER.append(('LOWCUT', 0, 0, 0, 10, (0x60, 0x00, 0x04, 0x10),1))
FX2_FLANGER.append(('EFFECTLEVEL', 0, 60, 0, 100, (0x60, 0x00, 0x04, 0x11),1))
FX2_FLANGER.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x12),1))
FX2_TREMOLO.append(('WAVESHAPE', 0, 70, 0, 100, (0x60, 0x00, 0x04, 0x13),1))
FX2_TREMOLO.append(('RATE', 0, 85, 0, 100, (0x60, 0x00, 0x04, 0x14),1))
FX2_TREMOLO.append(('DEPTH', 0, 65, 0, 100, (0x60, 0x00, 0x04, 0x15),1))
FX2_TREMOLO.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x16),1))
FX2_ROTARY.append(('RATE', 0, 85, 0, 100, (0x60, 0x00, 0x04, 0x19),1))
FX2_ROTARY.append(('DEPTH', 0, 60, 0, 100, (0x60, 0x00, 0x04, 0x1c),1))
FX2_ROTARY.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x1d),1))
FX2_UNI.append(('RATE', 0, 70, 0, 100, (0x60, 0x00, 0x04, 0x1e),1))
FX2_UNI.append(('DEPTH', 0, 60, 0, 100, (0x60, 0x00, 0x04, 0x1f),1))
FX2_UNI.append(('LEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x20),1))
FX2_SLICER.append(('PATTERN', 0, 0, 0, 19, (0x60, 0x00, 0x04, 0x21),1))
FX2_SLICER.append(('RATE', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x22),1))
FX2_SLICER.append(('TRIGGERSENS', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x23),1))
FX2_SLICER.append(('EFFECTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x24),1))
FX2_SLICER.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x25),1))
FX2_VIBRATO.append(('RATE', 0, 80, 0, 100, (0x60, 0x00, 0x04, 0x26),1))
FX2_VIBRATO.append(('DEPTH', 0, 45, 0, 100, (0x60, 0x00, 0x04, 0x27),1))
FX2_VIBRATO.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x2a),1))
FX2_RINGMOD.append(('MODE', 0, 0, 0, 1, (0x60, 0x00, 0x04, 0x2b),1))
FX2_RINGMOD.append(('FREQUENCY', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x2c),1))
FX2_RINGMOD.append(('EFFECTLEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x2d),1))
FX2_RINGMOD.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x2e),1))
FX2_HUMANIZER.append(('MODE', 0, 1, 0, 1, (0x60, 0x00, 0x04, 0x2f),1))
FX2_HUMANIZER.append(('VOWEL1', 0, 0, 0, 4, (0x60, 0x00, 0x04, 0x30),1))
FX2_HUMANIZER.append(('VOWEL2', 0, 2, 0, 4, (0x60, 0x00, 0x04, 0x31),1))
FX2_HUMANIZER.append(('SENS', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x32),1))
FX2_HUMANIZER.append(('RATE', 0, 80, 0, 100, (0x60, 0x00, 0x04, 0x33),1))
FX2_HUMANIZER.append(('DEPTH', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x34),1))
FX2_HUMANIZER.append(('MANUAL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x35),1))
FX2_HUMANIZER.append(('LEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x36),1))
FX2_2x2CHORUS.append(('XOVERFREQUENCY', 0, 4, 0, 16, (0x60, 0x00, 0x04, 0x37),1))
FX2_2x2CHORUS.append(('LOWRATE', 0, 43, 0, 100, (0x60, 0x00, 0x04, 0x38),1))
FX2_2x2CHORUS.append(('LOWDEPTH', 0, 46, 0, 100, (0x60, 0x00, 0x04, 0x39),1))
FX2_2x2CHORUS.append(('LOWPREDELAY', 0, 3, 0, 80, (0x60, 0x00, 0x04, 0x3a),1))
FX2_2x2CHORUS.append(('LOWLEVEL', 0, 75, 0, 100, (0x60, 0x00, 0x04, 0x3b),1))
FX2_2x2CHORUS.append(('HIGHRATE', 0, 33, 0, 100, (0x60, 0x00, 0x04, 0x3c),1))
FX2_2x2CHORUS.append(('HIGHDEPTH', 0, 48, 0, 100, (0x60, 0x00, 0x04, 0x3d),1))
FX2_2x2CHORUS.append(('HIGHPREDELAY', 0, 3, 0, 80, (0x60, 0x00, 0x04, 0x3e),1))
FX2_2x2CHORUS.append(('HIGHLEVEL', 0, 65, 0, 100, (0x60, 0x00, 0x04, 0x3f),1))
FX2_2x2CHORUS.append(('DIRECTMIX', 0, 80, 0, 100, (0x60, 0x00, 0x04, 0x40),1))
FX2_ACSIM.append(('HIGH', 50, 0, -50, 50, (0x60, 0x00, 0x04, 0x41),1))
FX2_ACSIM.append(('BODY', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x42),1))
FX2_ACSIM.append(('LOW', 50, 0, -50, 50, (0x60, 0x00, 0x04, 0x43),1))
FX2_ACSIM.append(('LEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x45),1))
FX2_EVH.append(('SCRIPT', 0, 1, 0, 1, (0x60, 0x00, 0x04, 0x46),1))
FX2_EVH.append(('SPEED', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x47),1))
FX2_EVH.append(('MANUAL', 0, 45, 0, 100, (0x60, 0x00, 0x04, 0x48),1))
FX2_EVH.append(('WIDTH', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x49),1))
FX2_EVH.append(('SPEED', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x4a),1))
FX2_EVH.append(('REGEN.', 0, 80, 0, 100, (0x60, 0x00, 0x04, 0x4b),1))
FX2_EVH.append(('PEDALPOS', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x4c),1))
FX2_EVH.append(('PEDALMIN', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x4d),1))
FX2_EVH.append(('PEDALMAX', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x4e),1))
FX2_EVH.append(('EFFECTLEVEL', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x4f),1))
FX2_EVH.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x50),1))
FX2_DC30.append(('SELECT', 0, 0, 0, 1, (0x60, 0x00, 0x04, 0x51),1))
FX2_DC30.append(('INPUTVOLUME', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x52),1))
FX2_DC30.append(('CHORUSINTENSITY', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x53),1))
FX2_DC30.append(('ECHOREPEATRATE', 0, 400, 40, 600, (0x60, 0x00, 0x04, 0x54),2))
FX2_DC30.append(('ECHOINTENSISTY', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x56),1))
FX2_DC30.append(('ECHOVOLUME', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x57),1))
FX2_DC30.append(('TONE', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x58),1))
FX2_DC30.append(('OUTPUT', 0, 0, 0, 1, (0x60, 0x00, 0x04, 0x59),1))
FX2_HEAVY.append(('1OCTLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x04, 0x5a),1))
FX2_HEAVY.append(('2OCTLEVEL', 0, 0, 0, 100, (0x60, 0x00, 0x04, 0x5b),1))
FX2_HEAVY.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x04, 0x5c),1))

DLY1_DIGITAL = []
DLY1_DIGITAL.append(('DELAYTIME', 0, 400, 1, 2000, (0x60, 0x00, 0x05, 0x02),2))
DLY1_DIGITAL.append(('FEEDBACK', 0, 22, 0, 100, (0x60, 0x00, 0x05, 0x04),1))
DLY1_DIGITAL.append(('HIGHCUT', 0, 10, 0, 14, (0x60, 0x00, 0x05, 0x05),1))
DLY1_DIGITAL.append(('EFFECTLEVEL', 0, 50, 0, 120, (0x60, 0x00, 0x05, 0x06),1))
DLY1_DIGITAL.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x05, 0x07),1))

DLY1_PAN = DLY1_DIGITAL.copy()
DLY1_PAN.append(('TAPTIME', 0, 50, 0, 100, (0x60, 0x00, 0x05, 0x08),1))

DLY1_MODULATE = DLY1_DIGITAL.copy()
DLY1_MODULATE.append(('MODRATE', 0, 40, 0, 100, (0x60, 0x00, 0x05, 0x13),1))
DLY1_MODULATE.append(('MODDEPTH', 0, 55, 0, 100, (0x60, 0x00, 0x05, 0x14),1))

DLY1_SDE = DLY1_MODULATE.copy()
DLY1_SDE.append(('RANGE', 0, 1, 0, 1, (0x60, 0x00, 0x05, 0x15),1))
DLY1_SDE.append(('FILTER', 0, 0, 0, 1, (0x60, 0x00, 0x05, 0x16),1))
DLY1_SDE.append(('FEEDBACKPHASE', 0, 0, 0, 1, (0x60, 0x00, 0x05, 0x17),1))
DLY1_SDE.append(('DELAYPHASE', 0, 0, 0, 1, (0x60, 0x00, 0x05, 0x18),1))
DLY1_SDE.append(('MODSW', 0, 0, 0, 1, (0x60, 0x00, 0x05, 0x19),1))

DLY1_STEREO = DLY1_DIGITAL.copy()
DLY1_REVERSE = DLY1_DIGITAL.copy()
DLY1_ANALOG = DLY1_DIGITAL.copy()
DLY1_TAPE = DLY1_DIGITAL.copy()

DELAY_SETTINGS = {"Digital":DLY1_DIGITAL,"Pan":DLY1_PAN,"Stereo":DLY1_STEREO,"Reverse":DLY1_REVERSE,"Analog":DLY1_ANALOG,"Tape Echo":DLY1_TAPE,"Modulate":DLY1_MODULATE,"SDE3000":DLY1_SDE}

RVB_AMBIENCE = []
RVB_AMBIENCE.append(('REVERBTIME', -1, 30, 1, 100, (0x60, 0x00, 0x05, 0x42),1))
RVB_AMBIENCE.append(('PREDELAY', 0, 10, 0, 500, (0x60, 0x00, 0x05, 0x43),2))
RVB_AMBIENCE.append(('LOWCUT', 0, 14, 0, 17, (0x60, 0x00, 0x05, 0x45),1))
RVB_AMBIENCE.append(('HIGHCUT', 0, 8, 0, 14, (0x60, 0x00, 0x05, 0x46),1))
RVB_AMBIENCE.append(('DENSITY', 0, 8, 0, 10, (0x60, 0x00, 0x05, 0x47),1))
RVB_AMBIENCE.append(('EFFECTLEVEL', 0, 35, 0, 100, (0x60, 0x00, 0x05, 0x48),1))
RVB_AMBIENCE.append(('DIRECTMIX', 0, 100, 0, 100, (0x60, 0x00, 0x05, 0x49),1))

RVB_ROOM = RVB_AMBIENCE.copy()
RVB_HALL1 = RVB_AMBIENCE.copy()
RVB_HALL2 = RVB_AMBIENCE.copy()
RVB_PLATE = RVB_AMBIENCE.copy()
RVB_SPRING = RVB_AMBIENCE.copy()
RVB_MODULATE = RVB_AMBIENCE.copy()

RVB_SPRING.append(('SPRINGCOLOR', 0, 50, 0, 100, (0x60, 0x00, 0x05, 0x4b),1))

REVERB_SETTINGS = {"Ambience":RVB_AMBIENCE,"Room":RVB_ROOM,"Hall 1":RVB_HALL1,"Hall 2":RVB_HALL2,"Plate":RVB_PLATE,"Spring":RVB_SPRING,"Modulate":RVB_MODULATE}

#BOOST_SETTINGS = 
FX1_SETTINGS = {'T Wah':FX1_TWAH, 'Auto Wah':FX1_AWAH, 'Pedal Wah':FX1_SUBWAH, 'Comp':FX1_ADCOMP, 'Limiter':FX1_LIMITER, 'Graphic EQ':FX1_GEQ, 'Parametric EQ':FX1_PEQ, 'Guitar Sim':FX1_GTRSIM, 'Slow Gear':FX1_SLOWGEAR, 'Wave Synth':FX1_WAVESYN, 'Octave':FX1_OCTAVE, 'Pitch Shifter':FX1_PITCHSHIFT, 'Harmonist':FX1_HARMONIST, 'AC Processor':FX1_ACPROCESS, 'Phaser':FX1_PHASER, 'Flanger':FX1_FLANGER, 'Tremolo':FX1_TREMOLO, 'Rotary':FX1_ROTARY, 'Uni-V':FX1_UNI, 'Slicer':FX1_SLICER, 'Vibrato':FX1_VIBRATO, 'Ring Mod':FX1_RINGMOD, 'Humanizer':FX1_HUMANIZER, 'Chorus':FX1_2x2CHORUS, 'AC Guitar Sim':FX1_ACSIM, 'Phaser90e':FX1_EVH, 'DC30':FX1_DC30, 'HeavyOctave':FX1_HEAVY, 'Flanger117e':FX1_FLANGER, 'Wah95e':FX1_SUBWAH}
FX2_SETTINGS = {'T Wah':FX2_TWAH,'Auto Wah':FX2_AWAH,'Pedal Wah':FX2_SUBWAH,'Comp':FX2_ADCOMP,'Limiter':FX2_LIMITER,'Graphic EQ':FX2_GEQ,'Parametric EQ':FX2_PEQ,'Guitar Sim':FX2_GTRSIM,'Slow Gear':FX2_SLOWGEAR,'Wave Synth':FX2_WAVESYN,'Octave':FX2_OCTAVE,'Pitch Shifter':FX2_PITCHSHIFT,'Harmonist':FX2_HARMONIST,'AC Processor':FX2_ACPROCESS,'Phaser':FX2_PHASER,'Flanger':FX2_FLANGER,'Tremolo':FX2_TREMOLO,'Rotary':FX2_ROTARY,'Uni-V':FX2_UNI,'Slicer':FX2_SLICER,'Vibrato':FX2_VIBRATO,'Ring Mod':FX2_RINGMOD,'Humanizer':FX2_HUMANIZER,'Chorus':FX2_2x2CHORUS,'AC Guitar Sim':FX2_ACSIM,'Phaser90e':FX2_EVH,'DC30':FX2_DC30,'HeavyOctave':FX2_HEAVY,'Flanger117e':FX2_FLANGER,'Wah95e':FX2_SUBWAH}

BOOST_MID = []
BOOST_CLEAN = []
BOOST_TREBLE = []
BOOST_CRUNCH = []
BOOST_NATURAL = []
BOOST_WARM = []
BOOST_FLAT = []
BOOST_LEAD = []
BOOST_METAL = []
BOOST_OCTFUZZ = []
BOOST_BLUES = []
BOOST_OVERDRIVE = []
BOOST_TSCREAM = []
BOOST_TURBO = []
BOOST_DIST = []
BOOST_RAT = []
BOOST_GUVDS = []
BOOST_DST = []
BOOST_METALZ = []
BOOST_60 = []
BOOST_MUFF = []

BOOST_MID.append(('DRIVE', 0, 50, 0, 120, (0x60, 0x00, 0x00, 0x12),1))
BOOST_MID.append(('BOTTOM', 50, 10, -50, 50, (0x60, 0x00, 0x00, 0x13),1))
BOOST_MID.append(('TONE', 50, 0, -50, 50, (0x60, 0x00, 0x00, 0x14),1))
BOOST_MID.append(('SOLOSW', 0, 0, 0, 1, (0x60, 0x00, 0x00, 0x15),1))
BOOST_MID.append(('SOLOLEVEL', 0, 50, 0, 100, (0x60, 0x00, 0x00, 0x16),1))
BOOST_MID.append(('EFFECTLEVEL', 0, 40, 0, 100, (0x60, 0x00, 0x00, 0x17),1))
BOOST_MID.append(('DIRECTMIX', 0, 0, 0, 100, (0x60, 0x00, 0x00, 0x18),1))

BOOST_CLEAN = BOOST_MID.copy()
BOOST_TREBLE = BOOST_MID.copy()
BOOST_CRUNCH = BOOST_MID.copy()
BOOST_NATURAL = BOOST_MID.copy()
BOOST_WARM = BOOST_MID.copy()
BOOST_FLAT = BOOST_MID.copy()
BOOST_LEAD = BOOST_MID.copy()
BOOST_METAL = BOOST_MID.copy()
BOOST_OCTFUZZ = BOOST_MID.copy()
BOOST_BLUES = BOOST_MID.copy()
BOOST_OVERDRIVE = BOOST_MID.copy()
BOOST_TSCREAM = BOOST_MID.copy()
BOOST_TURBO = BOOST_MID.copy()
BOOST_DIST = BOOST_MID.copy()
BOOST_RAT = BOOST_MID.copy()
BOOST_GUVDS = BOOST_MID.copy()
BOOST_DST = BOOST_MID.copy()
BOOST_METALZ = BOOST_MID.copy()
BOOST_60 = BOOST_MID.copy()
BOOST_MUFF = BOOST_MID.copy()

BOOST_SETTINGS = {'Mid Boost':BOOST_MID,'Clean Boost':BOOST_CLEAN,'Treble Boost':BOOST_TREBLE,'Crunch OD':BOOST_CRUNCH,'Natural OD':BOOST_NATURAL,'Warm OD':BOOST_WARM,'Fat DS':BOOST_FLAT,'Lead DS':BOOST_LEAD,'Metal DS':BOOST_METAL,'Oct Fuzz':BOOST_OCTFUZZ,'Blues Drive':BOOST_BLUES,'Overdrive':BOOST_OVERDRIVE,'T-Scream':BOOST_TSCREAM,'Turbo OD':BOOST_TURBO,'Distortion':BOOST_DIST,'Rat':BOOST_RAT,'Guv DS':BOOST_GUVDS,'DST+':BOOST_DST,'Metal Zone':BOOST_METALZ,'60s Fuzz':BOOST_60,'Muff Fuzz':BOOST_MUFF}


