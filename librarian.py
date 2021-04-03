import json
import tsl
import os
import katana
import tkinter as tk

from tkinter import *
import tkinter.font as tkFont

import tkinter.filedialog as fdialog
import tkinter.messagebox as messagebox

from globals import *
from PatchData import *

import getpass as gp

class Librarian(tk.Frame):
    def __init__(self, master=None, **kwargs):#, tkRoot, app, katana):
        tk.Frame.__init__(self, master)

        self.lastDir = '/home/' + gp.getuser()
        
        self.data = None
        self.patches = {}
        self.mk2_params = {}
        # put patch1 data after patch2 in case effect chain setting is present
        self.sections = ('UserPatch%Patch_0', 'UserPatch%Fx(1)', 'UserPatch%Fx(2)', 'UserPatch%Delay(1)', 'UserPatch%Delay(2)', 'UserPatch%Patch_1', 'UserPatch%Patch_2')
        self.mk2_params[self.sections[0]] = tsl.patch0_tsl
        self.mk2_params[self.sections[1]] = tsl.patch1_tsl
        self.mk2_params[self.sections[2]] = tsl.patch2_tsl
        self.mk2_params[self.sections[3]] = tsl.delay1_tsl
        self.mk2_params[self.sections[4]] = tsl.delay2_tsl
        self.mk2_params[self.sections[5]] = tsl.fx1_tsl
        self.mk2_params[self.sections[6]] = tsl.fx2_tsl
        
        title = "Patch Loader"
        
        self.grid()
        
        self.scrollbar = tk.Scrollbar(self, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=2, sticky=tk.NW+tk.S)
        
        self.list = tk.Listbox(self, yscrollcommand=self.scrollbar.set, height=14)
        self.list.grid(row=0, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        items = ["one", "two", "three"]
        self.list.insert(0, *items)
        
        self.scrollbar['command'] = self.list.yview
        
        close = tk.Button(self, text="Close", command=master.destroy)
        close.grid(row=3, column=0, columnspan=2)

        load = tk.Button(self, text="Load", command=self.loadSelected)
        load.grid(row=1, column=0, columnspan=1)
        
        clear = tk.Button(self, text="Clear", command=self.reset)
        clear.grid(row=1, column=1, columnspan=1)
        
        browse = tk.Button(self, text="Browse Files", command=self.browseFiles)
        browse.grid(row=2, column=0)
        
        browseDir = tk.Button(self, text="Browse Folder", command=self.browseDir)
        browseDir.grid(row=2, column=1)
        
        self.patch_values = {}

        self.katana = None
        
    def setKatana(self, katana):
        self.katana = katana
        
    def loadSelected(self):
        curr = self.list.get(self.list.curselection())
        print("Loading " + curr)
        self.loadPatch(self.katana, curr)
        
    def reset(self):
        self.patches.clear()
        self.refreshList()
        
    def loadDir(self, tsl_dir):
        for filename in os.listdir(tsl_dir):
            if filename.endswith(".tsl"):
                self.loadTSL(os.path.join(tsl_dir, filename))
                
        self.refreshList()
        
    def refreshList(self):
        if self.list.size() > 0:
            self.list.delete(0, tk.END)
        self.list.insert(0, *self.patches.keys())
        
    def browseFiles(self):
        filenames = tk.filedialog.askopenfilenames(initialdir = self.lastDir, title = "Select a File", filetypes = (("TSL files", "*.tsl"), ("all files", "*.*")))
        for filename in filenames:
            print(filename)
            self.loadTSL(filename)
            self.lastDir = os.path.dirname(filename)
        self.refreshList()
        
    def browseDir(self):
        filename = tk.filedialog.askdirectory(initialdir = self.lastDir, title = "Select a Folder")
        print(filename)
        self.loadDir(filename)
        self.lastDir = filename
        #self.refreshList()
    
    def loadTSL(self, file):
        fileData = None
        try:
            with open(file, 'r') as handle:
                fileData = json.load(handle)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed for ' + file)
        
        if fileData is None:
            print("No data for " + file)
            return
        
        if fileData['device'] == 'KATANA MkII':
            print(fileData['device'])
            
            for preset in fileData['data'][0]:
                name = preset['paramSet']['UserPatch%PatchName']
                #name[0] = '4C'
                test = int(name[0], 16)
                print(str(test))
                name = [int(i,16) for i in name]
                name = ''.join(map(chr, name))
                name = name.strip()
                print(name)
                self.patches[name] = []
                self.patch_values[name] = {}
                for section in self.sections:
                    print(section)
                    patch = preset['paramSet'][section]
                    params = self.mk2_params[section]
                    print("patch len = " + str(len(patch)))
                    print("section len = " + str(len(params)))
                    #print(str(patch))
                    #print(str(params))
                    if section == 'UserPatch%Patch_1':
                        if len(params) > 83:
                            print(name + " contains fx chain data")
                    sz = min(len(patch), len(params))
                    for i in range(sz):
                        p = params[i]
                        #p[0][0] = 0 #zero offset if coming from mk2 patch
                        self.patches[name].append((p, int(patch[i],16)))
                        if p in addr_map.keys():
                            self.patch_values[arr_map[p]] = int(patch[i],16)
                    
        elif 'GT' in fileData['device']:
            print(fileData['device'])
            #print(self.data['patchList'][0]['params'])
            print("Reading patch " + fileData['patchList'][0]['params']['patchname'])
            patchName = fileData['patchList'][0]['params']['patchname']
            self.patches[patchName] = []
            self.patch_values[patchName] = {}
            nParams = len(fileData['patchList'][0]['params'])
            nFound = 0
            for key in fileData['patchList'][0]['params']:
                if key in tsl.tsl_params:
                    if key == 'chain_ptn' and ('fx_chain_position1' in tsl.tsl_params or 'position1' in tsl.tsl_params):
                        print("skipping " + key + " because custom chain position data present")
                        continue
                    self.patches[patchName].append((tsl.tsl_params[key], fileData['patchList'][0]['params'][key]))
                    self.patch_values[patchName][key] = fileData['patchList'][0]['params'][key]
                    nFound = nFound+1
            print("found matches for " + str(nFound) + " out of " + str(nParams) + " parameters")
            
    def loadPatch(self, katana, patchName, ch=-1):
        params = self.patches[patchName]
        self.load(katana, patchName, ch, params)
    
    def load(self, katana, patchName, ch, params):
        chAddr = {-1:(0x60,0x00),0:(0x10,0x00),1:(0x10,0x01),2:(0x10,0x02),3:(0x10,0x03),4:(0x10,0x04),5:(0x10,0x05),6:(0x10,0x06),7:(0x10,0x07),8:(0x10,0x08)}
        print("Channel addr = " + str(chAddr[ch]))
        for param in params:
            #print(str(param))
            addr = (chAddr[ch][0], chAddr[ch][1], param[0][1][0], param[0][1][1])
            offs = 0#param[0][0]
            value = param[1] + offs
            if value > 127:
                print("value = " + str(value) + " at " + str(param[0][1][0]) + ", " + str(param[0][1][1]))
                continue
            if katana is not None:
                katana.send_sysex_data(addr, (value,))
            #else:
             #   print(str(addr) + " = " + str(value))
        if katana is not None and ch > -1:
            katana.set_patch_name(ch, patchName)
        else:
            print("done loading patch " + patchName + " into " + str(ch))
            
        self.summary(patchName)
            
    def getValue(self, patchName, paramName):
        if not patchName in self.patches.keys():
            return 'None'
            
        if paramName in self.patch_values[patchName].keys():
            return self.patch_values[patchName][paramName]
        else:
            return 'Not found'
        
    def summary(self, patchName):
        print(patchName + " Summary:")
        print("Amp:" + AMP_TYPES[self.getValue(patchName, 'preamp_a_type')])
        print("EQ:" + str(self.getValue(patchName, 'eq_on_off')))
        print("EQ type:" + str(self.getValue(patchName, 'eq_type')))
        print("Boost:" + str(self.getValue(patchName, 'od_ds_on_off')))
        print("Boost type:" + BOOST_OPTIONS[self.getValue(patchName, 'od_ds_type')])
        print("Mod:" + str(self.getValue(patchName, 'fx1_on_off')))
        print("Mod type:" + EFFECT_OPTIONS[self.getValue(patchName, 'fx1_fx_type')])
        print("FX:" + str(self.getValue(patchName, 'fx2_on_off')))
        print("FX type:" + EFFECT_OPTIONS[self.getValue(patchName, 'fx2_fx_type')])
        print("Delay1:" + str(self.getValue(patchName, 'delay_on_off')))
        print("Delay1 type:" + DELAY_OPTIONS[self.getValue(patchName, 'delay_type')])
        print("Delay2:" + str(self.getValue(patchName, 'delay2_on_off')))
        print("Delay2 type:" + DELAY_OPTIONS[self.getValue(patchName, 'delay2_type')])        
        print("Reverb:" + str(self.getValue(patchName, 'reverb_on_off')))
        print("Reverb type:" + REVERB_OPTIONS[self.getValue(patchName, 'reverb_type')])
        
#         
#         
#         color_data = {}
#         color_data["fxbox_asgn_fx1a_g"] = (0x06,0x24)
#         color_data["fxbox_asgn_fx1a_r"] = (0x06,0x25)
#         color_data["fxbox_asgn_fx1a_y"] = (0x06,0x26)
#         color_data["fxbox_asgn_fx1b_g"] = (0x06,0x27)
#         color_data["fxbox_asgn_fx1b_r"] = (0x06,0x28)
#         color_data["fxbox_asgn_fx1b_y"] = (0x06,0x29)
#         color_data["fxbox_asgn_fx2a_g"] = (0x06,0x2a)
#         color_data["fxbox_asgn_fx2a_r"] = (0x06,0x2b)
#         color_data["fxbox_asgn_fx2a_y"] = (0x06,0x2c)
#         color_data["fxbox_asgn_fx2b_g"] = (0x06,0x2d)
#         color_data["fxbox_asgn_fx2b_r"] = (0x06,0x2e)
#         color_data["fxbox_asgn_fx2b_y"] = (0x06,0x2f)
#         color_data["fxbox_asgn_fx3_g"] = (0x06,0x30)
#         color_data["fxbox_asgn_fx3_r"] = (0x06,0x31)
#         color_data["fxbox_asgn_fx3_y"] = (0x06,0x32)
#         color_data["fxbox_asgn_fx3b_g"] = (0x06,0x33)
#         color_data["fxbox_asgn_fx3b_r"] = (0x06,0x34)
#         color_data["fxbox_asgn_fx3b_y"] = (0x06,0x35)
#         color_data["fxbox_layer_fx3_g"] = (0x06,0x36)
#         color_data["fxbox_layer_fx3_r"] = (0x06,0x37)
#         color_data["fxbox_layer_fx3_y"] = (0x06,0x38)
#         color_data["fxbox_sel_fx1a"] = (0x06,0x39)
#         color_data["fxbox_sel_fx1b"] = (0x06,0x3a)
#         color_data["fxbox_sel_fx2a"] = (0x06,0x3b)
#         color_data["fxbox_sel_fx2b"] = (0x06,0x3c)
#         color_data["fxbox_sel_fx3"] = (0x06,0x3d)
#         
#         for k in color_data.keys():
#             if 'fx1a' in k or 'fx2' in k:
#                 print(k + " = " + EFFECT_OPTIONS[self.getValue(patchName, k)])
        
if __name__ == '__main__':
    root = tk.Tk()
    
    test = tk.Toplevel(root)
    
    katana = None #katana.Katana('KATANA MIDI 1',  0,  False)
    l = Librarian(master=test)
    #l.loadTSL('/home/anthony/git_repos/tkatana/default_mk2.tsl')
    l.loadTSL('/home/pi/tsl_files/Dumble Clean Homage.tsl')
    #l.loadDir('/home/anthony/tsl_files')
    print(str(l.patches.keys()))
    
    l.refreshList()
    l.setKatana(katana)
    

    
    
    root.mainloop()
