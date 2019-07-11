###### in bashshell for caproto
#after source activte:
#OPHYD_CONTROL_LAYER=caproto bsui

### in bsui started above
#%run ~/caproto_loggers.py  # Defines set_handler, a caproto v0.2.3 feature, and `logger` the caproto logger.
#logger.handlers.clear()  # Remove the default handlers that print to the screen.
#set_handler(file='/tmp/what_is_happening.txt')  # Aims logs to a file
#logger.setLevel('DEBUG')

def plan_lsco_test(): 
    dets = [rixscam, ring_curr]
    yield from mv(extslt.vg,10, extslt.hg, 150)
    #yield from pol_V(0.85)
    rixscam_exp = 5
    cts=120
    repeat = 24
    # Fe 3uc
    #yield from mv(cryo.y,28.65)
    #yield from mv(cryo.x,26.31)
    #yield from mv(cryo.z,15.835)
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(gvbt1, 'open')
    yield from sleep(5)

    
    for i in range(0,repeat):
        print('\n\t\tstarting {} of {} loops\n'.format(i+1,repeat))
        yield from count(dets, num=cts, md = {'reason':'TESTING ccd DATA FAILURE'} )
        print('\n\t\tfinishing {} of 24 loops\n'.format(i+1))

    
    yield from mv(gvbt1,'close')
