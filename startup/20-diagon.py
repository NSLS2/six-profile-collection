from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt


class DIAGON(Device):
    hml = Cpt(EpicsMotor, '_HLPM}Mtr')
    hyag = Cpt(EpicsMotor, '_HLPF}Mtr')
    vml = Cpt(EpicsMotor, '_VLPM}Mtr')
    vyag = Cpt(EpicsMotor, '_VLPF}Mtr')    
    
diagon = DIAGON('XF:02IDA-OP{Diag:1-Ax:3', name='diagon')
