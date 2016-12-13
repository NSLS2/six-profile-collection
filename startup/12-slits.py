from ophyd import Device, Component as Cpt, EpicsMotor, PVPositioner

class BaffleSlit(Device):
    hg = Cpt(EpicsMotor, '-Ax:HG}Mtr')
    hc = Cpt(EpicsMotor, '-Ax:HC}Mtr')
    vg = Cpt(EpicsMotor, '-Ax:VG}Mtr')
    vc = Cpt(EpicsMotor, '-Ax:VC}Mtr')


class VirtualGap(PVPositioner):
    readback = Cpt(EpicsSignalRO, 't2.C')
    setpoint = Cpt(EpicsSignal, 'size')
    done = Cpt(EpicsSignalRO, 'DMOV')
    done_value = 1


class VirtualCenter(PVPositioner):
    readback = Cpt(EpicsSignalRO, 't2.D')
    setpoint = Cpt(EpicsSignal, 'center')
    done = Cpt(EpicsSignalRO, 'DMOV')
    done_value = 1


class VirtualMotorCenterAndGap(Device):
    "Center and gap with virtual motors"
    hc = Cpt(VirtualCenter, '-Ax:X}')
    vc = Cpt(VirtualCenter, '-Ax:Y}')
    hg = Cpt(VirtualGap, '-Ax:X}')
    vg = Cpt(VirtualGap, '-Ax:Y}')
 
    
class ExitSlit(Device):
    hg = Cpt(EpicsMotor, '_HG}Mtr')
    vg = Cpt(EpicsMotor, '_VG}Mtr')
    hc = Cpt(EpicsMotor, '_HT}Mtr')

    
feslt = VirtualMotorCenterAndGap('FE:C02A-OP{Slt:12', name='feslt')

m1slt = BaffleSlit('XF:02IDA-OP{Mir:1-Slt:4_D_1', name='m1slt')

pgmslt_u = BaffleSlit('XF:02IDB-OP{Mono:1-Slt:8_U_1', name='pgmslt_u')
pgmslt_d = BaffleSlit('XF:02IDB-OP{Mono:1-Slt:9_D_1', name='pgmslt_d')

m3slt = BaffleSlit('XF:02IDC-OP{Mir:3-Slt:12_U_1', name='m3slt')
m4slt = BaffleSlit('XF:02IDC-OP{Mir:4-Slt:18_U_1', name='m4slt')

extslt = ExitSlit('XF:02IDC-OP{Slt:1-Ax:15', name='extslt')
