from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt

class M1(Device):
    x = Cpt(EpicsMotor, '_Trans}Mtr')
    pit = Cpt(EpicsMotor, '_Pitch}Mtr')
    rol = Cpt(EpicsMotor, '_Roll}Mtr')

class MHexapod(Device):
    x = Cpt(EpicsMotor, '_X}Mtr')
    y = Cpt(EpicsMotor, '_Y}Mtr')
    z = Cpt(EpicsMotor, '_Z}Mtr')
    yaw = Cpt(EpicsMotor, '_Rx}Mtr')
    pit = Cpt(EpicsMotor, '_Ry}Mtr')
    rol = Cpt(EpicsMotor, '_Rz}Mtr')

    
m1 = M1('XF:02IDA-OP{Mir:1-Ax:4', name='m1')
m3 = MHexapod('XF:02IDC-OP{Mir:3-Ax:13', name='m3')
m4 = MHexapod('XF:02IDC-OP{Mir:4-Ax:18', name='m4')
