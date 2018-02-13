from ophyd import EpicsMotor

m6_msk = EpicsMotor('XF:02IDD-ES{Msk:Mir6-Ax:Y}Mtr',name='m6_msk')

espgm_msk = EpicsMotor('XF:02IDD-ES{Msk:Mono2-Ax:Y}Mtr',name='espgm_msk')

m5_msk = EpicsMotor('XF:02IDD-ES{Msk:Mir5-Ax:Y}Mtr',name='m5_msk')
