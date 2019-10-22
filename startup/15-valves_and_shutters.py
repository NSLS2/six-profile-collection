from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
from ophyd import DeviceStatus
# from nslsii.devices import TwoButtonShutter  #TODO why are we not suing the facility TwoButtonShutter?
from nslsii.devices import _time_fmtstr  # TODO(DAMA/MR/20191022): this is a temp workaround for a missing var


class TwoButtonShutter(Device):  #Why custom and not facility?

    open_cmd = Cpt(EpicsSignal, 'Cmd:Opn-Cmd', string=True)
    open_val = 'Open'

    close_cmd = Cpt(EpicsSignal, 'Cmd:Cls-Cmd', string=True)
    close_val = 'Not Open'

    status = Cpt(EpicsSignalRO, 'Pos-Sts', string=True)
    fail_to_close = Cpt(EpicsSignalRO, 'Sts:FailCls-Sts', string=True)
    fail_to_open = Cpt(EpicsSignalRO, 'Sts:FailOpn-Sts', string=True)
    enabled_status = Cpt(EpicsSignalRO, 'Enbl-Sts', string=True)

    # user facing commands
    open_str = 'open'
    close_str = 'close'

    def set(self, val):
        if self._set_st is not None:
            raise RuntimeError(f'trying to set {self.name} while a set is in progress')

        cmd_map = {self.open_str: self.open_cmd,
                   self.close_str: self.close_cmd}
        target_map = {self.open_str: self.open_val,
                      self.close_str: self.close_val}

        cmd_sig = cmd_map[val]
        target_val = target_map[val]

        st = DeviceStatus(self)
        if self.status.get() == target_val:
            st._finished()
            return st

        self._set_st = st
        print(self.name, val, id(st))
        enums = self.status.enum_strs

        def shutter_cb(value, timestamp, **kwargs):
            value = enums[int(value)]
            if value == target_val:
                self._set_st = None
                self.status.clear_sub(shutter_cb)
                st._finished()

        cmd_enums = cmd_sig.enum_strs
        count = 0
        def cmd_retry_cb(value, timestamp, **kwargs):
            nonlocal count
            value = cmd_enums[int(value)]
            # ts = datetime.datetime.fromtimestamp(timestamp).strftime(_time_fmtstr)
            # print('sh', ts, val, st)
            count += 1
            if count > 5:
                cmd_sig.clear_sub(cmd_retry_cb)
                self._set_st = None
                self.status.clear_sub(shutter_cb)
                st._finished(success=False)
            if value == 'None':
                if not st.done:
                    time.sleep(.5)
                    cmd_sig.set(1)
                    ts = datetime.datetime.fromtimestamp(timestamp).strftime(_time_fmtstr)
                    if count > 2:
                        print('** ({}) Had to reactuate shutter while {}ing'.format(ts, val if val is not 'Close' else val[:-1]))
                else:
                    cmd_sig.clear_sub(cmd_retry_cb)

        cmd_sig.subscribe(cmd_retry_cb, run=False)
        self.status.subscribe(shutter_cb)
        cmd_sig.set(1)

        return st

    def stop(self, success):
        import time
        prev_st = self._set_st
        if prev_st is not None:
            while not prev_st.done:
                time.sleep(.1)
        self._was_open = (self.open_val == self.status.get())
        st = self.set('close')
        while not st.done:
            time.sleep(.5)

    def resume(self):
        import time
        prev_st = self._set_st
        if prev_st is not None:
            while not prev_st.done:
                time.sleep(.1)
        if self._was_open:
            st = self.set('open')
            while not st.done:
                time.sleep(.5)

    def unstage(self):
        self._was_open = False
        return super().unstage()

    def __init__(self, *args, **kwargs):
        self._was_open = False
        super().__init__(*args, **kwargs)
        self._set_st = None
        self.read_attrs = ['status']

#Piezoshutter mode signal:
def snap(dets):
    # DAMA/MR (20191022): Try to work-around the issue with half-staged detectors left from previous iteration.
    def _unstage_dets():
        for d in dets:
            yield from bps.unstage(d)

    for i in range(5):
        try:
            yield from _unstage_dets()
        except TimeoutError as e:
            print('*'*50)
            print(f'Unsuccessful attempt #{i+1} to unstage the detectors')
            print(f"Exception: {e}")
            print('*'*50)
            yield from bps.sleep(5)

    for d in dets:
        yield from bps.stage(d)
    for d in dets:
        yield from bps.trigger(d, group='snap')
    yield from bps.wait(group='snap')

    for i in range(5):
        try:
            yield from _unstage_dets()
        except TimeoutError as e:
            print('*'*50)
            print(f'Unsuccessful attempt #{i+1} to unstage the detectors')
            print(f"Exception: {e}")
            print('*'*50)
            yield from bps.sleep(5)


pzshutter = EpicsSignal('XF:02ID1-ES{RIXSCam}:cam1:ShutterMode', name = 'pzshutter')
def pzshutter_enable():
    rixscam_exp_temp = rixscam.cam.acquire_time.value
    rixscam_exp = 1
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pzshutter,'Detector output')
    yield from snap([rixscam])#, num=1, md = {'reason': 'enable pzshutter'})
    yield from mv(rixscam.cam.acquire_time, rixscam_exp_temp)

def pzshutter_disable():
    rixscam_exp_temp = rixscam.cam.acquire_time.value
    rixscam_exp = 1
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pzshutter,'None')
    yield from snap([rixscam])#, num=1, md = {'reason': 'enable pzshutter'})
    yield from mv(rixscam.cam.acquire_time, rixscam_exp_temp)

#Define the shutters from the above class.
shutterfe = TwoButtonShutter('XF:02ID-PPS{Sh:FE}', name='shutterfe')
shuttera = TwoButtonShutter('XF:02IDA-PPS{PSh}', name='shuttera')
shutterb = TwoButtonShutter('XF:02IDB-PPS{PSh}', name='shutterb')

#Define the gatevalves from the above class.
gvbt1 = TwoButtonShutter('XF:02IDD-VA{BT:1-GV:1}', name='gvbt1')
gvsc1 = TwoButtonShutter('XF:02IDD-VA{SC:1-GV:1}', name='gvsc1')
