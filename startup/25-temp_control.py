from collections import deque

from ophyd import (EpicsMotor, PVPositioner, PVPositionerPC,
                   EpicsSignal, EpicsSignalRO, Device)
from ophyd import Component as Cpt
from ophyd import FormattedComponent as FmtCpt
from ophyd import DynamicDeviceComponent as DDC
from ophyd import DeviceStatus, OrderedDict


class Lakeshore336Setpoint(PVPositioner):
    readback = Cpt(EpicsSignalRO, 'T-RB')
    setpoint = Cpt(EpicsSignal, 'T-SP')
    done = Cpt(EpicsSignalRO, 'Sts:Ramp-Sts')
    ramp_enabled = Cpt(EpicsSignal, 'Enbl:Ramp-Sel')
    done_value = 0


class Lakeshore336Channel(Device):
    T = Cpt(EpicsSignalRO, 'T-I')
    V = Cpt(EpicsSignalRO, 'Val:Sens-I')
    status = Cpt(EpicsSignalRO, 'T-Sts')

#    def __init__(self, *args, read_attrs=None, **kwargs):
#        if read_attrs is None:
#            read_attrs = ['T']
#        super().__init__(*args, read_attrs=read_attrs, **kwargs)


def _temp_fields(chans, **kwargs):
    defn = OrderedDict()
    for c in chans:
        suffix = '-Chan:{}}}'.format(c)
        defn[c] = (Lakeshore336Channel, suffix, kwargs)

    return defn


class Lakeshore336(Device):
    temp = DDC(_temp_fields(['A','B']))#,'C','D']))
    ctrl1 = Cpt(Lakeshore336Setpoint, '-Out:1}')
    ctrl2 = Cpt(Lakeshore336Setpoint, '-Out:2}')


class Lakeshore336Ext(Lakeshore336):
    temp = DDC(_temp_fields(['A','B','C','D','E','F','G', 'H']))


#This part is not used, but can be used to treat the cryostat setpoint/readback as a motor
class Lakeshore336Picky(Device):
    setpoint = Cpt(EpicsSignal, read_pv='-Out:1}T-RB', write_pv='-Out:1}T-SP',
                   add_prefix=('read_pv', 'write_pv'))
    # TODO expose ramp rate
    ramp_done = Cpt(EpicsSignalRO, '-Out:1}Sts:Ramp-Sts')
    ramp_enabled = Cpt(EpicsSignal, '-Out:1}Enbl:Ramp-Sel')
    ramp_rate = Cpt(EpicsSignal, read_pv='-Out:1}Val:Ramp-RB',
                    write_pv='-Out:1}Val:Ramp-SP',
                    add_prefix=('read_pv', 'write_pv'))

    chanA = Cpt(Lakeshore336Channel, '-Chan:A}')
    chanB = Cpt(Lakeshore336Channel, '-Chan:B}')

    def __init__(self, *args, timeout=60*60*30, target='chanA', **kwargs):
        # do the base stuff
        super().__init__(*args, **kwargs)
        # status object for communication
        self._done_sts = None

        # state for deciding if we are done or not
        self._cache = deque()
        self._start_time = 0
        self._setpoint = None
        self._count = -1

        # longest we can wait before giving up
        self._timeout = timeout
        self._lagtime = 120

        # the channel to watch to see if we are done
        self._target_channel = target

        # parameters for done testing
        self.mean_thresh = .01
        self.ptp_thresh = .1

    def _value_cb(self, value, timestamp, **kwargs):
        self._cache.append((value, timestamp))

        if (timestamp - self._cache[0][1]) < self._lagtime / 2:
            return

        while (timestamp - self._cache[0][1]) > self._lagtime:
            self._cache.popleft()

        buff = np.array([v[0] for v in self._cache])
        if self._done_test(self._setpoint, buff):
            self._done_sts._finished()
            self._reset()

    def _setpoint_cb(value, **kwargs):
        print('in cb', value)
        if value == self._setpoint:
            self._done_sts._finished()
            self.setpoint.clear_sub(self._setpoint_cb, 'value')

    def _reset(self):
        if self._target_channel == 'setpoint':
            target = self.setpoint
            target.clear_sub(self._setpoint_cb, 'value')
        else:
            target = getattr(self, self._target_channel).T
            target.clear_sub(self._value_cb, 'value')
        self._done_sts = None
        self._setpoint = None
        self._cache.clear()

    def _done_test(self, target, buff):
        mn = np.mean(np.abs(buff - target))

        if mn > self.mean_thresh:
            return False

        if np.ptp(buff) > self.ptp_thresh:
            return False

        return True


    def set(self, new_position, *, timeout=None):
        # to be subscribed to 'value' cb on readback
        sts = self._done_sts = DeviceStatus(self, timeout=timeout)
        if self.setpoint.get() == new_position:
            self._done_sts._finished()
            self._done_sts = None
            return sts

        self._setpoint = new_position

        self.setpoint.set(self._setpoint)

        # todo, set up subscription forwarding
        if self._target_channel == 'setpoint':
            self.setpoint.subscribe(local_cb, 'value')
        else:
            target = getattr(self, self._target_channel).T
            target.subscribe(self._value_cb, 'value')

        return self._done_sts


stemp = Lakeshore336('XF:02IDD-ES{TCtrl:1', name='stemp')
#stemp.hints = {'fields': ['stemp_temp_A', 'stemp_temp_B']}  #TODO this doesn't work at 2ID and it DID at 23ID (is it kind vs hints)


