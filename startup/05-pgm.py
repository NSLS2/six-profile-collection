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

class PGMjoe(Device):
    # cff = Cpt(EpicsMotor, '_Cff}Mtr')
    # en = Cpt(EpicsMotor, '_Eng}Mtr')
    gr_x = Cpt(EpicsMotor, '_GT}Trans:Mtr')
    m2_pit = Cpt(EpicsMotor, '_MP}Mtr')
    gr_pit = Cpt(EpicsMotor, '_GP}Mtr')

    gr500 = Cpt(EpicsSignalRO, '_GT}Trans:GT1Inp')
    gr1200 = Cpt(EpicsSignalRO, '_GT}Trans:GT2Inp')
    gr1800 = Cpt(EpicsSignalRO, '_GT}Trans:GT3Inp')

# TODO changing gratign will require a plan + at least 1
# soft signal

class PGM_ES(Device):
    cff = Cpt(EpicsMotor, 'cff}Mtr')
    en = Cpt(EpicsMotor, 'E}Mtr')
    gr_x = Cpt(EpicsMotor, 'GXRaw}Mtr')
    m7_pit = Cpt(EpicsMotor, 'MP}Mtr')
    gr_pit = Cpt(EpicsMotor, 'GP}Mtr')


pgm = PGM('XF:02IDB-OP{Mono:1-Ax:9', name='pgm')
pgmjoe = PGMjoe('XF:02IDB-OP{Mono:1-Ax:9', name='pgmjoe')
espgm = PGM_ES('XF:02IDD-ES{Mono:2-Ax:',name='espgm')
