from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt

#defines the sample chamber Device
class SCdevice(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')

sc = SCdevice('XF:02IDD-ES{SC:Pvt-Ax:',name='sc')

#defines the spectrometer arm Device
class Brdevice(Device): 
    yin = Cpt(EpicsMotor, 'YUI}Mtr')
    you = Cpt(EpicsMotor, 'YUO}Mtr')
    ydn = Cpt(EpicsMotor, 'YD}Mtr')
    pit = Cpt(EpicsMotor, 'Pch}Mtr')
    roll = Cpt(EpicsMotor, 'Roll}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    
br = Brdevice('XF:02IDD-ES{BT:1-Ax:',name='br')

#defines the Optics chamber Device
class OCdevice(Device):
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')
    roll  = Cpt(EpicsMotor, 'Roll}Mtr')
    twoth = Cpt(EpicsMotor, '2T}Mtr')
    wlin = Cpt(EpicsMotor, 'YI}Mtr')
    wlot = Cpt(EpicsMotor, 'YO}Mtr')
    
oc = OCdevice('XF:02IDD-ES{3AA:1-Ax:',name='oc')


#defines the Polarimeter chamber Device
class DCdevice(Device):
    z = Cpt(EpicsMotor, 'Z}Mtr')
    twoth = Cpt(EpicsMotor, '2T}Mtr')

dc = DCdevice('XF:02IDD-ES{DC:1-Ax:',name='dc')

