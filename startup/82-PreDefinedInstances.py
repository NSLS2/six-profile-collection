from ophyd import EpicsMotor
import collections
import time
import math


#Definition of SIX specific classes
    
#Class for single ('y') motion axis devices.
class DiagAndSingleAxisMaskClass(PreDefinedPositions):
    '''
    A class that is used to define a PreDefinedPositions child class for use with a single 'y' motion axis. 
    It is a child of the PreDefinedPositions class which allows for defining a set of pre-defined positions, in addition 
    these have a single, "y", axis that is used to move to the different locations.
    '''

    y = Cpt(EpicsMotor, '')



#class for single ('th') motion axis devices
class OpticsWheelClass(PreDefinedPositions):
    '''
    A class that is used to define a PreDefinedPositions child class for use with a single 'th' motion axis . It is a child of the 
    PreDefinedPositions class which allows for defining a set of pre-defined positions, in addition 
    these have a single, "th", axis that is used to move to the different locations.
    '''
    
    th = Cpt(EpicsMotor, '')


#class for 8 ('in','out','bottom','top','hc','hg','vc','vg') motion axis devices
class BaffleSlitClass(PreDefinedPositions):
    '''
    A class that is used to define a PreDefinedPositions child class for use with 8 motion axis ('in','out','bottom','top','hc','hg',
    'vc','vg'). It is a child of the PreDefinedPositions class which allows for defining a set of pre-defined positions, in addition 
    these have 8 axes associated with a type of baffle slits ('in','out','bottom','top','hc','hg','vc','vg') axis that is used to move 
    to the different locations.
    '''
    #top level baffle slit axes
    hg = Cpt(EpicsMotor, '-Ax:HG}Mtr')
    hc = Cpt(EpicsMotor, '-Ax:HC}Mtr')
    vg = Cpt(EpicsMotor, '-Ax:VG}Mtr')
    vc = Cpt(EpicsMotor, '-Ax:VC}Mtr')
    #low level real motor axes
    inb = Cpt(EpicsMotor, '-Ax:I}Mtr')
    out = Cpt(EpicsMotor, '-Ax:O}Mtr')
    bot = Cpt(EpicsMotor, '-Ax:B}Mtr')
    top = Cpt(EpicsMotor, '-Ax:T}Mtr')
 
#class for 8 ('hs','ha','vs','va','hc','hg','vc','vg') motion axis devices
class BaffleSlitSAClass(PreDefinedPositions):
    '''
    A class that is used to define a PreDefinedPositions child class for use with 8 motion axis ('hs','ha','vs','va','hc','hg',
    'vc','vg'). It is a child of the PreDefinedPositions class which allows for defining a set of pre-defined positions, in addition 
    these have 8 axes associated with a type of baffle slits ('hs','ha','vs','va','hc','hg','vc','vg') axis that is used to move 
    to the different locations.
    '''
    #top level baffle slit axes
    hg = Cpt(EpicsMotor, '-Ax:HG}Mtr')
    hc = Cpt(EpicsMotor, '-Ax:HC}Mtr')
    vg = Cpt(EpicsMotor, '-Ax:VG}Mtr')
    vc = Cpt(EpicsMotor, '-Ax:VC}Mtr')
    #low level real motor axes
    hs = Cpt(EpicsMotor, '-Ax:HS}Mtr')
    ha = Cpt(EpicsMotor, '-Ax:HA}Mtr')
    vs = Cpt(EpicsMotor, '-Ax:VS}Mtr')
    va = Cpt(EpicsMotor, '-Ax:VA}Mtr')




#Definition of Devices
    
#Masks

            
m5mask = DiagAndSingleAxisMaskClass('XF:02IDD-ES{Msk:Mir5-Ax:Y}Mtr',
                         locations = {'open':['y',54], 'thin':['y',34], 'wide':['y',21], 'thru':['y',8],},
                         vis_path_options={'fig_size':[10,10],'axis_labels':['arbitrary axis','m5mask_y'],
                                           'pos':{'open':[0,54],'thin':[0,34],'wide':[0,21],'thru':[0,8]}},
                         name = 'm5mask')

espgmmask = DiagAndSingleAxisMaskClass('XF:02IDD-ES{Msk:Mono2-Ax:Y}Mtr',
                         locations= {'yag':['y',-43.4],'out':['y',0]},
                         vis_path_options={'fig_size':[10,10],'axis_labels':['arbitrary axis','espgm_y'],
                                           'pos':{'out':[0,0],'yag':[0,-43.4]}},
                         cam_list = [sc_4],
                         name='espgmmask')

#Diagnostic units


m3diag = DiagAndSingleAxisMaskClass('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',
                         locations = {'diode':['y',-76.4],'grid':['y',-97.5], 'out':['y',-1],
                                      'yag':['y',-49.4,'cam.roi1_minx',582,'cam.roi1_sizex',44,'cam.roi1_miny',
                                             540,'cam.roi1_sizey',225]},
                         vis_path_options={'fig_size':[10,10],'axis_labels':['arbitrary axis','m3diag_y'],
                                           'pos':{'diode':[0,-76.4],'grid':[0,-97.5],'out':[0,-1],'yag':[0,-49.4]}},
                         cam_list = [m3_diag_cam], qem_list = [qem05],
                         name = 'm3diag')

gcdiag = DiagAndSingleAxisMaskClass('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',
                         locations = {'diode':['y',-71.4], 'yag':['y',-43.4], 'grid':['y',-95.4], 'out':['y',-1]},
                         vis_path_options={'fig_size':[10,10],'axis_labels':['arbitrary axis','gcdiag_y'],
                                           'pos':{'diode':[0,-71.4],'grid':[0,-95.4],'out':[0,-1],'yag':[0,-43.4]}},
                         cam_list = [gc_diag_cam], qem_list = [qem07],  
                         name = 'gcdiag')

#Optics wheel

ow = OpticsWheelClass('XF:02IDD-ES{Mir:5-Ax:S1_2T}Mtr',
                         locations={'m5in':['th',-30],'m5out':['th',-90],'yag_reflected':['th',100.3],
                                    'yag_postcryo':['th',-26.5],'yag_precryo':['th',-209.7],'door':['th',113],
                                    'diode':['th',68.9]},
                         vis_path_options={'fig_size':[20,20],'axis_labels':['cryo_x','cryo_z'],
                                           'pos': {'diode': [-0.14953534344370978, 0.9887563810470058],
                                           'door': [-0.7954734808548956, 0.6059884002657115],
                                           'm5in': [0.9999862922474267, -0.005235963831419821],
                                           'm5out': [0.4954586684324072, -0.8686315144381914],
                                           'yag_postcryo': [0.998440764181981, 0.05582150499316376],
                                           'yag_precryo': [-1.0, 0.0],
                                           'yag_reflected': [-0.6427876096865393, 0.7660444431189781]} },
                         name='ow')
    
#defining some parameters for the visulization of the paths

###BELOW IS USED TO GENERATE THE VIS_PATH_OPTIONS "POS" DICTIONARY FOR THE OW
#new_dict={}
#for key in ow.locations.keys():
#    new_dict[key]=[-1* math.cos(math.radians(ow.locations[key][1]+209.7)),math.sin(math.radians(ow.locations[key][1]+209.7))]



#Baffle Slits

dcslt = BaffleSlitClass('XF:02IDD-ES{DC:1-Slt:1',
                           locations={'baffle':['inb',18,'out',45,'bot',11,'top',10],
                                      'retract':['inb',46,'out',46,'bot',38,'top',33]},
                           name='dcslt')

m4slt = BaffleSlitClass('XF:02IDC-OP{Mir:4-Slt:18_U_1',
                           locations={'baffle':['inb',5,'out',5,'bot',5,'top',-8],
                                      'retract':['inb',0,'out',10,'bot',0,'top',0]}, 
                           name='m4slt')



#Definition of Device Groups

diagnostics = PreDefinedPositionsGroup([m3diag,gcdiag],{'test_location':['m3diag','out','gcdiag','out']},name='diagnostics')








#Below is some carry over definitions for devices that should be defined above but which are yet to be.


m4_diag1 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:1}Mtr',name='m4_diag1')
m4_diag2 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:2}Mtr',name='m4_diag2')
m4_diag3 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:3}Mtr',name='m4_diag3')

m5_RPD = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:RPD}Mtr', name='m5_RPD')

SC_QPD = EpicsMotor('XF:02IDD-ES{SC:1-Ax:QPD}Mtr', name='SC_QPD')
SC_IO = EpicsMotor('XF:02IDD-ES{SC:1-Ax:IO}Mtr', name='m5_RPD')
