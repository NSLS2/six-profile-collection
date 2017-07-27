# this startup file is for misc. detectors and monitors

from ophyd import (EpicsSignal, EpicsSignalRO)

ring_curr = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_curr')



