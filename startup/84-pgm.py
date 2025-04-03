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

    m3slt_hs = Cpt(EpicsMotor, prefix='XF:02IDC-OP{Mir:3-Slt:12_U_1-Ax:HS}Mtr')
    m3slt_ha = Cpt(EpicsMotor, prefix='XF:02IDC-OP{Mir:3-Slt:12_U_1-Ax:HA}Mtr')


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
    #grx = Cpt(EpicsMotor, 'GXRaw}Mtr') #Commented on  12/15/2020 because it doesn't work with BS
    grx = Cpt(EpicsMotor, 'GX}Mtr')
    m7pit = Cpt(EpicsMotor, 'MP}Mtr')
    grpit = Cpt(EpicsMotor, 'GP}Mtr')
    grxrb = Cpt(EpicsSignalRO,'GXEnc}Mtr.RBV')

    #grlines = Cpt(EpicsSignalRO, prefix='XF:02IDD-ES{Mono:2-Grt:1}Name-I.VAL') # Added on 12/15/2020

# Before moving PGM, remember to Kill the motors for grpit and m2pit:
# on May 2024 all grating X positions have been adjusted by -2.5mm compared to previous values.
# The GR500 was not directly checked, so if possible one would need to dobule check that -65.5mm is good (previously was -63mm).
pgm = PGM('XF:02IDB-OP{Mono:1', name='pgm', locations = {
         'mbg': ['m2off', 84.1967687, 'groff', 82.072196,'grx', -65.5, 'grlines', 500, 'm3slt_hs', -37.8,
				 'm3slt_ha',-17.6], # last correction 20240523
                 # 20240929 m2off 84.19919 groff 82.076584
                 # 20240522 -> 'm2off', 84.1951147473, 'groff', 82.0717671
                 # 20230914 -> 'm2off', 84.1983417173, 'groff', 82.07381828
                 # offset before 20230127 'm2off', 84.2004597573, 'groff', 82.07204739;
                
                 
         'hbg': ['m2off', 84.1962152973, 'groff',  82.133440903303,'grx', 58.0, 'grlines', 1200, 'm3slt_hs', -38.0,
				 'm3slt_ha',-17.8], 
                 # 20240930 -> 'm2off', 84.19821348730001, 'groff',  82.1369613933033
                 # 20230913 -> 'm2off', 84.1991382173, 'groff',  82.1336183933033
                 # 20230127 ->'m2off', 84.2033182673, 'groff',  82.1366541933033
                 # 20220915 -> offset m2off 84.199606602; 'groff', 82.1314578049,'grx', 61.0,
                 # offset values before 20220125 m2 84.201175342; groff 82.1322482849

	 	 'ubg': ['m2off', 84.19988039699999, 'groff', 82.07982024, 'grx', -3.5,'grlines', 1800, 'm3slt_hs', -37.5,
				 'm3slt_ha',-17.8] }) #at 20240523 'm2off', 84.20149823, 'groff', 82.11328655
                 # at 20230127 ->'m2off', 84.20009535, 'groff', 82.1145797096
                 # before 20220918 'm2off', 84.20377334307703, 'groff', 82.132248343, 'grx', -1
                  #before 01/16/2020 'm2off', 84.2072359100, 'groff', 82.105016851 
                                      
pgmjoe = PGMjoe('XF:02IDB-OP{Mono:1-Ax:9', name='pgmjoe')
espgm = PGM_ES('XF:02IDD-ES{Mono:2-Ax:',name='espgm')

# pgm = PGM('XF:02IDB-OP{Mono:1', name='pgm', locations = {
#           'mbg': ['m2off', 84.20549404, 'groff', 82.07813352 ,'grx', -63.0, 'grlines', 500], #'offset values changed on 08/11/2019 ['m2off', 84.20033028, 'groff', 82.0737638 ,'grx', -63.0, 'grlines', 500]
#  	       'ubg': ['m2off', 84.20861191, 'groff', 82.1055395916 , 'grx', -1,'grlines', 1800] }) #before 08/10/2019 'ubg': ['m2off', 84.20265344, 'groff', 82.1012242016 , 'grx', -1,'grlines', 1800] })


