
from bluesky.suspenders import (SuspendBoolHigh,
                                SuspendBoolLow,
                                SuspendFloor,
                                SuspendCeil,
                                SuspendInBand,
                                SuspendOutBand)

ring_suspender = SuspendFloor(EpicsSignal('XF:23ID-SR{}I-I'), 230, sleep=120)

fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:23ID-PPS{Sh:FE}Pos-Sts'), sleep=20*60)

#test_shutsusp = SuspendBoolHigh(EpicsSignal('XF:23IDA-EPS{DP:1-Sh:1}Pos-Sts'), sleep=5)

## It needs:
## RE.install_suspender(test_shutsusp)
## RE.remove_suspender(test_shutsusp)

#RE.install_suspender(ring_suspender)
RE.install_suspender(fe_shut_suspender)
