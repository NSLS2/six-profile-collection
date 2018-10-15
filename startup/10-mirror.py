from ophyd import Device, EpicsMotor, EpicsSignalRO, EpicsSignal, PVPositioner
from ophyd import Component as Cpt, FormattedComponent as FCpt

class M1(Device):
    x = Cpt(EpicsMotor, '_Trans}Mtr')
    pit = Cpt(EpicsMotor, '_Pitch}Mtr')
    rol = Cpt(EpicsMotor, '_Roll}Mtr')

class M6(Device):
    z = Cpt(EpicsMotor, 'Z}Mtr')
    pit = Cpt(EpicsMotor, 'Pch}Mtr')

class MHexapod(Device):
    x = Cpt(EpicsMotor, '_X}Mtr')
    y = Cpt(EpicsMotor, '_Y}Mtr')
    z = Cpt(EpicsMotor, '_Z}Mtr')
    yaw = Cpt(EpicsMotor, '_Rx}Mtr')
    pit = Cpt(EpicsMotor, '_Ry}Mtr')
    rol = Cpt(EpicsMotor, '_Rz}Mtr')

class M5_axis(PVPositioner):
    done = FCpt(EpicsSignalRO, '{self._sliced_prefix}Sts:MoveDone-Sts')
    def __init__(self, prefix, *args, **kwargs):
        self._sliced_prefix = ''.join(prefix.partition('}')[:2])
        super().__init__(prefix, *args, **kwargs)
        self.readback.name = self.name

    readback = Cpt(EpicsSignalRO, "-I")
    setpoint = Cpt(EpicsSignal, "-SP")
    done_value=1

class EHexapod(Device):
    x = Cpt(M5_axis, 'X')
    y = Cpt(M5_axis, 'Y')
    z = Cpt(M5_axis, 'Z')
    yaw = Cpt(M5_axis, 'Yaw')
    pit = Cpt(M5_axis, 'Pitch')
    rol = Cpt(M5_axis, 'Roll')


m1 = M1('XF:02IDA-OP{Mir:1-Ax:4', name='m1')
m3 = MHexapod('XF:02IDC-OP{Mir:3-Ax:13', name='m3')
m4 = MHexapod('XF:02IDC-OP{Mir:4-Ax:18', name='m4')
m5 = EHexapod('XF:02IDD-ES{Mir:5}Pos:', name='m5')
m6 = M6('XF:02IDD-ES{Mir:6-Ax:', name='m6')
