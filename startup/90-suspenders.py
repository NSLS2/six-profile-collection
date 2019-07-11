
from bluesky.suspenders import SuspendFloor
               

ring_suspender = SuspendFloor(ring_curr, 190, resume_thresh=200, sleep=120)
# Is this the right PV???
#fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:02ID-PPS{Sh:FE}Enbl-Sts'), sleep=20*60)

## It needs:
## RE.install_suspender(test_shutsusp)
## RE.remove_suspender(test_shutsusp)

RE.install_suspender(ring_suspender)
#RE.install_suspender(fe_shut_suspender)

print("")
print("You can safely ignore the 'SuspendOutBand' warning - this is a known issue that is fixed in a newer version.")
