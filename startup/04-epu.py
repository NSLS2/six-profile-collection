from ophyd import (PVPositioner, Component as Cpt, Signal, EpicsSignal, EpicsSignalRO,
                   Device, FormattedComponent as FmCpt)
from ophyd.positioner import PositionerBase
import ophyd
import warnings


# path for the new standby mode
epu_sb = EpicsSignal('SR:C02-ID:G1A{EPU:1}Cmd:SBy-Cmd', name = 'epu_standby')

epu_sb_ao = EpicsSignal('XF:02ID-ID{Ping}Enbl-SP', name = 'epu_standby_auto')
# 


class DeadbandMixin(Device, PositionerBase):
    """
    Borrowed with gratitude from SST.
    # TODO:  Add to nslsii package after testing and refactor.


    Should be the leftmost class in the inheritance list so that it grabs move first!

    Must be combined with either EpicsMotor or PVPositioner, or some other class
    that has a done_value attribute

    An EpicsMotor subclass that has an absolute tolerance for moves.
    If the readback is within tolerance of the setpoint, the MoveStatus
    is marked as finished, even if the motor is still settling.

    This prevents motors with long, but irrelevant, settling times from
    adding overhead to scans.
    """
    tolerance = Cpt(Signal, value=-1, kind='config')
    move_latch = Cpt(Signal, value=0, kind="omitted")

    def _done_moving(self, success=True, timestamp=None, value=None, **kwargs):
        '''Call when motion has completed.  Runs ``SUB_DONE`` subscription.'''
        if self.move_latch.get():
            if success:
                self._run_subs(sub_type=self.SUB_DONE, timestamp=timestamp,
                               value=value)

            self._run_subs(sub_type=self._SUB_REQ_DONE, success=success,
                           timestamp=timestamp)
            self._reset_sub(self._SUB_REQ_DONE)
            self.move_latch.put(0)

    def move(self, position, wait=True, **kwargs):
        tolerance = self.tolerance.get()

        if tolerance < 0:
            self.move_latch.put(1)
            return super().move(position, wait=wait, **kwargs)
        else:
            status = super().move(position, wait=False, **kwargs)
            setpoint = position
            done_value = getattr(self, "done_value", 1)

            def check_deadband(value, timestamp, **kwargs):
                if abs(value - setpoint) < tolerance:
                    self._done_moving(timestamp=timestamp,
                                      success=True,
                                      value=done_value)

            def clear_deadband(*args, timestamp, **kwargs):
                self.clear_sub(check_deadband, event_type=self.SUB_READBACK)

            self.subscribe(clear_deadband, event_type=self._SUB_REQ_DONE, run=False)
            self.move_latch.put(1)
            self.subscribe(check_deadband, event_type=self.SUB_READBACK, run=True)

            try:
                if wait:
                    ophyd.status.wait(status)
            except KeyboardInterrupt:
                self.stop()
                raise

            return status


class DeadBandPositioner(PVPositioner):
    def __init__(self, *args, **kwargs):
        warnings.warn("DeadBandPositioner is deprecated, use DeadbandMixin instead",
                      DeprecationWarning)
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


class UgapPositioner(DeadbandMixin, PVPositioner):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tolerance.put(0.0005)


class UphasePositioner(DeadbandMixin, PVPositioner):
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

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.tolerance.put(0.0005)


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




