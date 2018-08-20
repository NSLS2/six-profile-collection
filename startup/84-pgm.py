from ophyd import Component as Cpt, Device, EpicsMotor, EpicsSignalRO, EpicsSignal

class PGM(PreDefinedPositions):
    cff = Cpt(EpicsMotor, '-Ax:9_Cff}Mtr')
    en = Cpt(EpicsMotor, '-Ax:9_Eng}Mtr')
    grx = Cpt(EpicsMotor, '-Ax:9_GT}Trans:Mtr')
    m2pit = Cpt(EpicsMotor, '-Ax:9_MP}Mtr')
    grpit = Cpt(EpicsMotor, '-Ax:9_GP}Mtr')

    gr500 = Cpt(EpicsSignalRO, '-Ax:9_GT}Trans:GT1Inp')
    gr1200 = Cpt(EpicsSignalRO, '-Ax:9_GT}Trans:GT2Inp')
    gr1800 = Cpt(EpicsSignalRO, '-Ax:9_GT}Trans:GT3Inp')

    groff = Cpt(EpicsSignal, '-Ax:9_GP}Mtr.OFF')
    m2off = Cpt(EpicsSignal, '-Ax:9_MP}Mtr.OFF')
    grlines = Cpt(EpicsSignal, '}:LINES')


class PGMjoe(Device):
    # cff = Cpt(EpicsMotor, '_Cff}Mtr')
    # en = Cpt(EpicsMotor, '_Eng}Mtr')
    grx = Cpt(EpicsMotor, '_GT}Trans:Mtr')
    m2pit = Cpt(EpicsMotor, '_MP}Mtr')
    grpit = Cpt(EpicsMotor, '_GP}Mtr')

    gr500 = Cpt(EpicsSignalRO, '_GT}Trans:GT1Inp')
    gr1200 = Cpt(EpicsSignalRO, '_GT}Trans:GT2Inp')
    gr1800 = Cpt(EpicsSignalRO, '_GT}Trans:GT3Inp')


# TODO changing gratign will require a plan + at least 1
# soft signal

class PGM_ES(Device):
    cff = Cpt(EpicsMotor, 'cff}Mtr')
    en = Cpt(EpicsMotor, 'E}Mtr')
    grx = Cpt(EpicsMotor, 'GXRaw}Mtr')
    m7pit = Cpt(EpicsMotor, 'MP}Mtr')
    grpit = Cpt(EpicsMotor, 'GP}Mtr')
    grxrb = Cpt(EpicsSignalRO,'GXEnc}Mtr.RBV')

pgm = PGM('XF:02IDB-OP{Mono:1', name='pgm', locations = {
         'mbg': ['groff', 82.102040,'m2off', 84.244630, 'grx', -63.0, 'grlines', 500], 
	 'hbg': ['groff', 82.080270, 'm2off', 84.208460, 'grx', -2.5,'grlines', 1200] })
pgmjoe = PGMjoe('XF:02IDB-OP{Mono:1-Ax:9', name='pgmjoe')
espgm = PGM_ES('XF:02IDD-ES{Mono:2-Ax:',name='espgm')



