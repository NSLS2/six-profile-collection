from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
from ophyd import DeviceStatus

class TwoButtonShutter(Device):
    open_cmd = Cpt(EpicsSignal, 'Cmd:Opn-Cmd', string=True)
    # expected readback on status when open
    open_val = 'Open'

    close_cmd = Cpt(EpicsSignal, 'Cmd:Cls-Cmd', string=True)
    # expected readback on status when closed
    close_val = 'Not Open'

    permit_enabled = Cpt(EpicsSignal, 'Permit:Enbl-Sts', string=True)
    enabled = Cpt(EpicsSignal, 'Enbl-Sts', string=True)

    status = Cpt(EpicsSignalRO, 'Pos-Sts', string=True)
    fail_to_close = Cpt(EpicsSignalRO, 'Sts:FailCls-Sts', string=True)
    fail_to_open = Cpt(EpicsSignalRO, 'Sts:FailOpn-Sts', string=True)

    
    # user facing commands
    open_str = 'open'
    close_str = 'close'
    def set(self, val):
        if self._set_st is not None:
            raise RuntimeError('trying to set while a set is in progress')

        cmd_map = {self.open_str: self.open_cmd,
                   self.close_str: self.close_cmd}
        target_map = {self.open_str: self.open_val,
                      self.close_str: self.close_val}

        cmd_sig = cmd_map[val]
        target_val = target_map[val]

        st = self._set_st = DeviceStatus(self)
        enums = self.status.enum_strs

        def shutter_cb(value, timestamp, **kwargs):
            value = enums[int(value)]
            if value == target_val:
                self._set_st._finished()
                self._set_st = None
                self.status.clear_sub(shutter_cb)

        cmd_enums = cmd_sig.enum_strs
        count = 0
        def cmd_retry_cb(value, timestamp, **kwargs):
            nonlocal count
            

            value = cmd_enums[int(value)]
            if value == 'None':
                if not st.done:
                    shutter_cb(self.status.get(as_string=False), timestamp)
                    if not st.done:
                        time.sleep(.1)

                        cmd_sig.set(1)

                        count += 1
                        if count > 1:
                            cmd_sig.clear_sub(cmd_retry_cb)
                            st._finished(success=False)
                    else:
                        cmd_sig.clear_sub(cmd_retry_cb)                            
                    
                else:
                    cmd_sig.clear_sub(cmd_retry_cb)

                    
        cmd_sig.set(1)
        cmd_sig.subscribe(cmd_retry_cb, run=False)

        self.status.subscribe(shutter_cb)


        return st

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ['status']

#Define the shutters from the above class.
shutterfe = TwoButtonShutter('XF:02ID-PPS{Sh:FE}', name='shutterfe')
shuttera = TwoButtonShutter('XF:02IDA-PPS{PSh}', name='shuttera')
shutterb = TwoButtonShutter('XF:02IDB-PPS{PSh}', name='shutterb')

#Define the gatevalves from the above class.
gvbt1 = TwoButtonShutter('XF:02IDD-VA{BT:1-GV:1}', name='gvbt1')
gvsc1 = TwoButtonShutter('XF:02IDD-VA{SC:1-GV:1}', name='gvsc1')
