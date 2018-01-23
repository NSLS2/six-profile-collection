from ophyd import Device, Component as Cpt, EpicsMotor, PVPositioner, EpicsSignal, EpicsSignalRO

# Cryostat B Manipulator
class Manipulator(Device):
    x = Cpt(EpicsMotor, 'X}Mtr')
    y = Cpt(EpicsMotor, 'Y}Mtr')
    z = Cpt(EpicsMotor, 'Z}Mtr')
    t = Cpt(EpicsMotor, 'T}Mtr')

cryo = Manipulator('XF:02IDD-ES{SC:1-Cryo:S1_B-Ax:', name='cryo')

# Optics Wheel Theta -- TO DO: probably to be changed into M5 Theta when M5 is integrated
ow = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:S1_2T}Mtr', name='ow')
