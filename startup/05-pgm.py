from ophyd import Component as Cpt, Device, EpicsMotor, EpicsSignalRO

class PGM(Device):
    cff = Cpt(EpicsMotor, '_Cff}Mtr')
    en = Cpt(EpicsMotor, '_Eng}Mtr')
    gr_x = Cpt(EpicsMotor, '_GT}Trans:Mtr')
    m2_pit = Cpt(EpicsMotor, '_MP}Mtr')
    gr_pit = Cpt(EpicsMotor, '_GP}Mtr')

    gr500 = Cpt(EpicsSignalRO, '_GT}Trans:GT1Inp')
    gr1200 = Cpt(EpicsSignalRO, '_GT}Trans:GT2Inp')
    gr1800 = Cpt(EpicsSignalRO, '_GT}Trans:GT3Inp')

# TODO changing gratign will require a plan + at least 1
# soft signal
    
pgm = PGM('XF:02IDB-OP{Mono:1-Ax:9', name='pgm')
