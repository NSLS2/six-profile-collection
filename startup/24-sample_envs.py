from ophyd import Device, Component as Cpt, EpicsMotor, PVPositioner, EpicsSignal, EpicsSignalRO

class Manipulator(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')
    t = Cpt(EpicsMotor, 'T}Mtr')

cryo = Manipulator('XF:02IDD-ES{SC:1-Cryo:S1_B-Ax:', name='cryo')


