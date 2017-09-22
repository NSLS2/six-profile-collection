from ophyd import (PVPositioner, Component as Cpt, EpicsSignal, EpicsSignalRO,
                   Device)
from ophyd.utils import ReadOnlyError
import time as ttime




class UgapPositioner(PVPositioner):
    readback = Cpt(EpicsSignalRO, '-Ax:Gap}Mtr.RBV')
    setpoint = Cpt(EpicsSignal, '-Ax:Gap}Mtr')
    actuate = Cpt(EpicsSignal, '}Cmd:Start-Cmd', string=True)
    actuate_value = 'On'

    stop_signal = Cpt(EpicsSignal, '}Cmd:Stop-Cmd')
    stop_value = 1

    done = Cpt(EpicsSignal, '}Cmd:Start-Cmd')
    done_value = 0

    kill_switch_pressed = Cpt(EpicsSignalRO, '}Sts:Kill-Sts')
    safety_device_fail = Cpt(EpicsSignalRO, '}Sts:Safety-Sts', string=True)
    emergency_open_gap = Cpt(EpicsSignalRO, '}Sts:OpenGapCmd-Sts', string=True)
    # TODO subscribe kill switch prressed and stop motion
    
class UphasePositioner(PVPositioner):
    print('/n/nUphasePosistioner Start/n/n')  #TODO debug intermit problem
    readback = Cpt(EpicsSignalRO, '-Ax:Phase}Mtr.RBV')
    setpoint = Cpt(EpicsSignal, '-Ax:Phase}Mtr')
    actuate = Cpt(EpicsSignal, '}Cmd:Start-Cmd', string=True)
    actuate_value = 'On'

    stop_signal = Cpt(EpicsSignal, '}Cmd:Stop-Cmd')
    stop_value = 1

    done = Cpt(EpicsSignal, '}Cmd:Start-Cmd')
    done_value = 0

    kill_switch_pressed = Cpt(EpicsSignalRO, '}Sts:Kill-Sts')
    safety_device_fail = Cpt(EpicsSignalRO, '}Sts:Safety-Sts', string=True)
    emergency_open_gap = Cpt(EpicsSignalRO, '}Sts:OpenGapCmd-Sts', string=True)
    print('/n/nUphasePosistioner Stop/n/n')  #TODO debug intermit problem
    # TODO subscribe kill switch prressed and stop motion
    


class EPU(Device):
    print('/n/nEPU(Device) Start/n/n')  #TODO debug intermit problem
    gap = Cpt(UgapPositioner, '', settle_time=0)
    print('sleeping 5s before defining the phase')
    ttime.sleep(5)
    phase = Cpt(UphasePositioner, '', settle_time=0)
    print('/n/nEPU(Device) Stop/n/n')  #TODO debug intermit problem

epu1 = EPU('SR:C02-ID:G1A{EPU:1', name='epu1')

epu1.gap.read_attrs = ['setpoint', 'readback']
epu1.gap.readback.name = 'epu1_gap'

print(epu1.gap)

epu1.phase.read_attrs = ['setpoint', 'readback']
epu1.phase.readback.name = 'epu1_phase'

print(epu1.phase)
