from bluesky.suspenders import SuspendFloor, SuspendBoolHigh         


ring_suspender = SuspendFloor(ring_curr, 190, resume_thresh=200, sleep=600)#,
                              #post_plan=beamline_align_v3_for_suspenders)

shutterb_suspender = SuspendBoolHigh(EpicsSignalRO(shutterb.status.pvname), sleep=600)#,
									 #post_plan=beamline_align_v3_for_suspenders)

# Is this the right PV???
fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:02ID-PPS{Sh:FE}Pos-Sts'), sleep=600)
#fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:02ID-PPS{Sh:FE}Pos-Sts'), sleep=10*60)



RE.install_suspender(ring_suspender)
RE.install_suspender(fe_shut_suspender)
RE.install_suspender(shutterb_suspender)

# If you remove suspenders and want to implement them back:

# Before removing them:
#suspenders_saved_for_later = RE.suspenders # DAMA: This return an immutable copy, for the fans at home concerned about mutability.
#RE.clear_suspenders()
# Later, to re-instate them...
#for suspender in suspenders_saved_for_later:
#RE.install_suspender(suspender)
