def evening_09():

    yield from mv(extslt.vg, 50)
    yield from pol_V(8.4)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    yield from scan([qem11, qem12], pgm.en, 1055, 1125, 351)

    yield from pol_H(-4.2)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    yield from scan([qem11, qem12], pgm.en, 1055, 1125, 351)

def plan_night_10(): 

    #CeCoIn5- Ce-M5
    yield from pol_V(5.5)
    sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 360)
    yield from mv(qem11.averaging_time, 360)
    yield from mv(qem12.averaging_time, 360)  
    E = list(np.arange(878.0,881.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 360)
    yield from mv(qem11.averaging_time, 360)
    yield from mv(qem12.averaging_time, 360)  
    E = list(np.arange(881.0,884.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from pol_H(1)
    sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 360)
    yield from mv(qem11.averaging_time, 360)
    yield from mv(qem12.averaging_time, 360)  
    E = list(np.arange(878.0,881.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 360)
    yield from mv(qem11.averaging_time, 360)
    yield from mv(qem12.averaging_time, 360)  
    E = list(np.arange(881.0,884.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_night_11(): 

    #CeCoIn5- Ce-M5
    #yield from pol_V(5.5)
    #sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(878.0,879.59,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(879.4,881.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(881,882.59,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(882.4,884.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )



    yield from pol_H(1)
    yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(878.0,879.59,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(879.4,881.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(881,882.59,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 420)
    yield from mv(qem11.averaging_time, 420)
    yield from mv(qem12.averaging_time, 420)  
    E = list(np.arange(882.4,884.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_after_12(): 
    dets = [rixscam, sclr, qem11, qem12]
    rixscam_exp = 300
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(qem11.averaging_time, rixscam_exp)
    yield from mv(qem12.averaging_time, rixscam_exp)  
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,30, extslt.hg, 150)

    #CeCoIn5- Ce-M5
    #yield from pol_V(5.5)
    #yield from sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    #E = list(np.arange(878.0,880.09,0.2))
    #yield from rixscam_acquire(dets, E,m7_pit_vals, 3, None, 'CeCoIn5' )
    
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    #E = list(np.arange(880.0,882.09,0.2))
    #yield from rixscam_acquire(dets, E,m7_pit_vals, 3, None, 'CeCoIn5' )

    #yield from pol_H(1)
    #yield from sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    E = list(np.arange(877.5,881.59,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )
    
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    #E = list(np.arange(880.0,882.09,0.2))
    #yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )
    

    yield from mv(sclr.preset_time,1)
    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)


def plan_XAS():
    var = 1
    while var == 1 :
        yield from sleep(5)
        yield from (scan([qem11,qem12],pgm.en,875,885,71))

def plan_after_13(): 
    dets = [rixscam, sclr, qem11, qem12]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(qem11.averaging_time, rixscam_exp)
    yield from mv(qem12.averaging_time, rixscam_exp)  
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #CeCoIn5- Ce-M5
    E = list(np.arange(878.0,882.09,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )
   
    

    yield from mv(sclr.preset_time,1)
    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_anight_13(): 
    dets = [rixscam, sclr, qem11, qem12]
    Estart = 877.7
    Eend = 879.19
    rixscam_exp = 300
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(qem11.averaging_time, rixscam_exp)
    yield from mv(qem12.averaging_time, rixscam_exp)  
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,30, extslt.hg, 150)

    #CeCoIn5- Ce-M5
    #yield from pol_V(5.5)
    #yield from sleep(120)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    E = list(np.arange(Estart,Eend,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from pol_H(1)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    #yield from sleep(30)
    E = list(np.arange(Estart,Eend,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )
  
    yield from mv(sclr.preset_time,1)
    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)
    yield from (scan([qem11,qem12],pgm.en,875,885,71))
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(qem11.averaging_time, rixscam_exp)
    yield from mv(qem12.averaging_time, rixscam_exp)  
    yield from mv(sclr.preset_time, rixscam_exp)
    
    yield from pol_V(5.5)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    #yield from sleep(30)
    E = list(np.arange(Estart,Eend,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )

    yield from pol_H(1)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    #yield from sleep(30)
    E = list(np.arange(Estart,Eend,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'CeCoIn5' )  

    yield from mv(sclr.preset_time,1)
    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)
    yield from (scan([qem11,qem12],pgm.en,875,885,71))

