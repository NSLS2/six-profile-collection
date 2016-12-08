from ophyd import Device, Component as Cpt, EpicsMotor

class BaffleSlit(Device):
    hg = Cpt(EpicsMotor, '-Ax:HG}Mtr')
    hc = Cpt(EpicsMotor, '-Ax:HC}Mtr')
    vg = Cpt(EpicsMotor, '-Ax:VG}Mtr')
    vc = Cpt(EpicsMotor, '-Ax:VC}Mtr')


class FESlits(Device):
    hg = Cpt(EpicsMotor, '-Ax:X}size')
    hc = Cpt(EpicsMotor, '-Ax:X}center')
    vg = Cpt(EpicsMotor, '-Ax:Y}size')
    vc = Cpt(EpicsMotor, '-Ax:Y}center')

    
class ExitSlit(Device):
    hg = Cpt(EpicsMotor, '_HG}Mtr')
    vg = Cpt(EpicsMotor, '_VG}Mtr')
    hc = Cpt(EpicsMotor, '_HT}Mtr')

    
feslt = FESlits('FE:C02A-OP{Slt:12', name='fe_slits')

m1slt = BaffleSlit('XF:02IDA-OP{Mir:1-Slt:4_D_1', name='m1slt')

pgmslt_u = BaffleSlit('XF:02IDB-OP{Mono:1-Slt:8_U_1', name='pgmslt_u')
pgmslt_d = BaffleSlit('XF:02IDB-OP{Mono:1-Slt:9_D_1', name='pgmslt_d')

m3slt = BaffleSlit('XF:02IDC-OP{Mir:3-Slt:12_U_1', name='m3slt')
m4slt = BaffleSlit('XF:02IDC-OP{Mir:4-Slt:18_U_1', name='m4slt')

extslt = ExitSlit('XF:02IDC-OP{Slt:1-Ax:15', name='extslt')
