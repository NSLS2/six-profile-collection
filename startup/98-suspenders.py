from bluesky.suspenders import SuspendFloor, SuspendBoolHigh         


ring_suspender = SuspendFloor(ring_curr, 340, resume_thresh=348, sleep=600)#,
                              #post_plan=beamline_align_v3_for_suspenders)

shutterb_suspender = SuspendBoolHigh(EpicsSignalRO(shutterb.status.pvname), sleep=600)#,
									 #post_plan=beamline_align_v3_for_suspenders)

# Is this the right PV???
fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:02ID-PPS{Sh:FE}Pos-Sts'), sleep=600)
#fe_shut_suspender = SuspendBoolHigh(EpicsSignal('XF:02ID-PPS{Sh:FE}Pos-Sts'), sleep=10*60)

def install_suspenders():
    """
    This function has to be called outside RE
    just use install_suspenders() !!
    Install suspenders.

    Note that this clears any existing suspenders, so that if it is
    called twice in a row it does not register duplicates.
    """
    RE.clear_suspenders()
    RE.install_suspender(ring_suspender)
    RE.install_suspender(fe_shut_suspender)
    RE.install_suspender(shutterb_suspender)


def clear_suspenders():
    """
    Alias for RE.clear_suspenders()

    For convenience and symmetry with install_suspenders() above.
    """
    RE.clear_suspenders()


install_suspenders()

