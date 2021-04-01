import json

class Librarian:
    def __init__(self):#, tkRoot, app, katana):
        #self.tkRoot = tkRoot
        #self.app = app
        #self.katana = katana
        self.data = None
    def loadTSL(self, file):
        with open(file, 'r') as handle:
            self.data = json.load(handle)

        if self.data['device'] == 'KATANA MkII':
            print(self.data['device'])
            sections = ('UserPatch%Patch_0', 'UserPatch%Patch_1', 'UserPatch%Patch_2', 'UserPatch%Delay(1)', 'UserPatch%Delay(2)', 'UserPatch%Fx(1)', 'UserPatch%Fx(2)')
            for preset in self.data['data'][0]:
                name = preset['paramSet']['UserPatch%PatchName']
                #name[0] = '4C'
                test = int(name[0], 16)
                print(str(test))
                name = [int(i,16) for i in name]
                name = ''.join(map(chr, name))
                name = name.strip()
                print(name)
                for section in sections:
                    print(section)
                    patch = preset['paramSet'][section]
                    print(str(patch))
                    
        elif 'GT' in self.data['device']:
            print(self.data['device'])
            #print(self.data['patchList'][0]['params'])
            for key in self.data['patchList'][0]['params']:
                print(key + " = " + str(self.data['patchList'][0]['params'][key]))

            
        
l = Librarian()
l.loadTSL('/home/pi/tkatana/default_mk2.tsl')
l.loadTSL('/home/pi/tkatana/default.tsl')