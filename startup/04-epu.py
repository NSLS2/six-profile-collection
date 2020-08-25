from ophyd import (PVPositioner, Component as Cpt, EpicsSignal, EpicsSignalRO,
                   Device, FormattedComponent as FmCpt)
from ophyd.status import MoveStatus
from ophyd.positioner import PositionerBase
from ophyd.utils import ReadOnlyError
import time as ttime


# path for the new standby mode
epu_sb = EpicsSignal('SR:C02-ID:G1A{EPU:1}Cmd:SBy-Cmd', name = 'epu_standby')

epu_sb_ao = EpicsSignal('XF:02ID-ID{Ping}Enbl-SP', name = 'epu_standby_auto')
# 

class DeadBandPositioner(PVPositioner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_status = None
        
    def set(self, new_position, **kwargs):
        sts = self._last_status = super().set(new_position, **kwargs)
        rbv = self.readback
        
        def rbv_callback(value, **kwargs):
            # TUNE THIS DEADBAND!!!!
            if np.abs(value - new_position) < 0.0005:
                sts._finished()
                rbv.clear_sub(rbv_callback)
                
        rbv.subscribe(rbv_callback, run=True)
        
        return self._last_status

    def stop(self, *, success=False):
        # super hacky fix to skip pvpostioner stop method
        # which always hits the stop signal which flashes the brakes and takes
        # the
        if self._last_status is not None and self._last_status.done:
            return PositionerBase.stop(self, success=success)
        else:
            self.setpoint.put(self.position)
            return super().stop(success=success)
        
    def _setup_move(self, position):
        # this is because this apprently blocks until the move finishes!
        self.setpoint.put(position, wait=False)

class UgapPositioner(DeadBandPositioner):
    readback = Cpt(EpicsSignalRO, '-Ax:Gap}Mtr.RBV')
    setpoint = Cpt(EpicsSignal, '-Ax:Gap}Mtr')

    stop_signal = Cpt(EpicsSignal, '}Cmd:Stop-Cmd')
    stop_value = 0

    done = Cpt(EpicsSignal, '}Sts:Moving-Sts' )
    done_value = 0

    kill_switch_pressed = Cpt(EpicsSignalRO, '}Sts:Kill-Sts')
    safety_device_fail = Cpt(EpicsSignalRO, '}Sts:Safety-Sts', string=True)
    emergency_open_gap = Cpt(EpicsSignalRO, '}Sts:OpenGapCmd-Sts', string=True)
    # TODO subscribe kill switch prressed and stop motion
    
class UphasePositioner(DeadBandPositioner):
    readback = Cpt(EpicsSignalRO, '-Ax:Phase}Mtr.RBV')
    setpoint = Cpt(EpicsSignal, '-Ax:Phase}Mtr')

    stop_signal = Cpt(EpicsSignal, '}Cmd:Stop-Cmd')
    stop_value = 0

    done = Cpt(EpicsSignal, '}Sts:Moving-Sts')
    done_value = 0

    kill_switch_pressed = Cpt(EpicsSignalRO, '}Sts:Kill-Sts')
    safety_device_fail = Cpt(EpicsSignalRO, '}Sts:Safety-Sts', string=True)
    emergency_open_gap = Cpt(EpicsSignalRO, '}Sts:OpenGapCmd-Sts', string=True)
    # TODO subscribe kill switch prressed and stop motion
    


class EPU(Device):
    gap = Cpt(UgapPositioner, 'SR:C02-ID:G1A{EPU:1', settle_time=0)   #works without added table and offset & def below
    phase = Cpt(UphasePositioner, 'SR:C02-ID:G1A{EPU:1', settle_time=0) #works without added table and offset
    #gap = Cpt(UgapPositioner,'{self._epu_prefix}', settle_time=0)
    #phase = Cpt(UphasePositioner,'self._epu_prefix', settle_time=0)
    table = FmCpt(EpicsSignal,'{self._ai_prefix}Val:Table-Sel') # TODO add reference to PV string for meaning
    offset = FmCpt(EpicsSignal,'{self._ai2_prefix}Val:InpOff1-SP', name = 'epu1_offset') #calibration offset 
    def __init__(self, *args, ai_prefix=None,  ai2_prefix='None', **kwargs): #,epu_prefix=None
        #self._epu_prefix = epu_prefix
        self._ai_prefix = ai_prefix
        self._ai2_prefix = ai2_prefix
        
        super().__init__(*args, **kwargs)


epu1 = EPU(ai_prefix='XF:02ID-ID{EPU:1}', ai2_prefix ='XF:02ID-ID{EPU:1-FLT}', name='epu1') #epu_prefix='SR:C02-ID:G1A{EPU:1', 
#epu1 = EPU('SR:C02-ID:G1A{EPU:1', ai_prefix='XF:02ID-ID{EPU:1}', ai2_prefix ='XF:02ID-ID{EPU:1-FLT}', name='epu1')

#epu1 = EPU('SR:C02-ID:G1A{EPU:1', name='epu1')

#epu1.gap.read_attrs = ['setpoint', 'readback']
#epu1.gap.readback.name = 'epu1_gap'

#epu1.phase.read_attrs = ['setpoint', 'readback']
#epu1.phase.readback.name = 'epu1_phase'




