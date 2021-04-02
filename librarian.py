import json
import tsl
import os
import katana

class Librarian:
    def __init__(self, **kwargs):#, tkRoot, app, katana):
        #self.tkRoot = tkRoot
        #self.app = app
        #self.katana = katana
        self.data = None
        self.patches = {}
        self.mk2_params = {}
        self.sections = ('UserPatch%Patch_0', 'UserPatch%Patch_1', 'UserPatch%Patch_2', 'UserPatch%Delay(1)', 'UserPatch%Delay(2)', 'UserPatch%Fx(1)', 'UserPatch%Fx(2)')
        self.mk2_params[self.sections[0]] = tsl.patch0_tsl
        self.mk2_params[self.sections[1]] = tsl.patch1_tsl
        self.mk2_params[self.sections[2]] = tsl.patch2_tsl
        self.mk2_params[self.sections[3]] = tsl.delay1_tsl
        self.mk2_params[self.sections[4]] = tsl.delay2_tsl
        self.mk2_params[self.sections[5]] = tsl.fx1_tsl
        self.mk2_params[self.sections[6]] = tsl.fx2_tsl
        
        #tsl_dir = kwargs['dir']
        
    def loadDir(self, tsl_dir):
        for filename in os.listdir(tsl_dir):
            if filename.endswith(".tsl"):
                self.loadTSL(os.path.join(tsl_dir, filename))
        
    def loadTSL(self, file):
        with open(file, 'r') as handle:
            self.data = json.load(handle)

        if self.data['device'] == 'KATANA MkII':
            print(self.data['device'])
            
            for preset in self.data['data'][0]:
                name = preset['paramSet']['UserPatch%PatchName']
                #name[0] = '4C'
                test = int(name[0], 16)
                print(str(test))
                name = [int(i,16) for i in name]
                name = ''.join(map(chr, name))
                name = name.strip()
                print(name)
                self.patches[name] = []
                for section in self.sections:
                    print(section)
                    patch = preset['paramSet'][section]
                    params = self.mk2_params[section]
                    print("patch len = " + str(len(patch)))
                    print("section len = " + str(len(params)))
                    print(str(patch))
                    print(str(params))
                    sz = min(len(patch), len(params))
                    for i in range(sz):
                        self.patches[name].append((params[i], int(patch[i],16)))    
                    
        elif 'GT' in self.data['device']:
            print(self.data['device'])
            #print(self.data['patchList'][0]['params'])
            print("Reading patch " + self.data['patchList'][0]['params']['patchname'])
            patchName = self.data['patchList'][0]['params']['patchname']
            self.patches[patchName] = []
            for key in self.data['patchList'][0]['params']:
                if key not in tsl.tsl_params:
                    print("not found " + key)
                else:
                    self.patches[patchName].append((tsl.tsl_params[key], self.data['patchList'][0]['params']))
                #print(key + " = " + str(self.data['patchList'][0]['params'][key]))
    
    def loadPatch(self, katana, patchName, ch=-1):
        params = self.patches[patchName]
        self.load(katana, patchName, ch, params)
    
    def load(self, katana, patchName, ch, params):
        chAddr = {-1:(0x60,0x00),0:(0x10,0x00),1:(0x10,0x01),2:(0x10,0x02),3:(0x10,0x03),4:(0x10,0x04),5:(0x10,0x05),6:(0x10,0x06),7:(0x10,0x07),8:(0x10,0x08)}
        print("Channel addr = " + str(chAddr[ch]))
        for param in params:
            print(str(param))
            addr = (chAddr[ch][0], chAddr[ch][1], param[0][1][0], param[0][1][1])
            offs = param[0][0]
            value = param[1] + offs
            if katana is not None:
                katana.send_sysex_data(addr, value)
            else:
                print(str(addr) + " = " + str(value))
        if katana is not None and ch > -1:
            katana.set_patch_name(ch, patchName)
        else:
            print("done loading patch " + patchName + " into " + str(ch))
        
l = Librarian()
#l.loadTSL('/home/anthony/git_repos/tkatana/default_mk2.tsl')
#l.loadTSL('/home/anthony/git_repos/tkatana/default.tsl')
l.loadDir('/home/anthony/tsl_files')
print(str(l.patches.keys()))

katana = katana.Katana('KATANA MIDI 1',  0,  False)
