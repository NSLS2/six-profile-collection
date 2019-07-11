def overnight_blade():
    yield from beamline_align_v2()
    yield from sleep(10)
    yield from beam_position_vs_m4_height_v()
    yield from sleep(10)
    yield from beam_position_vs_m4_height_v()
    yield from sleep(10)

    print('*'*150)
    print('Done with test // Changing grating')
    print('*'*150)

    yield from mv(shuttera,'close')
    yield from pgm.mbg
    yield from sleep(10)
    yield from mv(pgm.m2pit,88.0920691)
    yield from mv(pgm.grpit,87.330043)
    yield from mv(pgm.en,710)
    yield from mv(pgm.cff,2.25)
    yield from mv(pgm.en,710)
    yield from mv(shuttera,'open')
    yield from sleep(600)
    yield from beamline_align_v2()

    print('*'*150)
    print('Grating is ready for beatiful measurements')
    print('*'*150)


def lunch_COSO_O_K():
    dets = [ ring_curr, rixscam, sclr]
    yield from mv(extslt.vg,20)
    num_scan = 10
    for i in range(num_scan):
        yield from count(dets, num = 100)
        yield from sleep(1)
        print(i)


def lunch():
    yield from beamline_align()
    yield from sleep(15)
    yield from rixscam_cff_optimization_centroid(45)


def cena():
    yield from mv(extslt.vg,7)
    yield from rixscam_cff_optimization_centroid(60)
    yield from mv(extslt.vg,20)
    yield from rixscam_pgm_en_centroid(30)
    yield from mv(extslt.vg,7)
    yield from rixscam_m6_m7_2_axis_centroid(60)

def test_ccd(infinite=True):
    while infinite is True:
        yield from count([rixscam,sclr],num=1000)
		#yield from sleep(30)

def dinner_commissioning():
    yield from beamline_align()
    yield from sleep(15)
    yield from mv(m4slt.vg,0.25)
    yield from rel_scan([sclr],m4slt.vc,-3,3,61)
    yield from sleep(15)

    yield from mv(m4slt.vg,3)
    yield from mv(m4slt.hg,0.25)
    yield from rel_scan([sclr],m4slt.hc,-3.5,3.5,71)
    yield from sleep(15)

    yield from mv(m4slt.hg,7)


def night_commissioning():
    yield from beamline_align()
    yield from sleep(15)
    yield from m4_depth_of_focus()
    yield from sleep(15)
    
    yield from stubborn_test(200) 

def plan_first_night(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 240
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(qem11.averaging_time, rixscam_exp)
    yield from mv(qem12.averaging_time, rixscam_exp)  
    yield from mv(sclr.preset_time, rixscam_exp)
    
    yield from pol_V(5.5)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Cu2OSeO3- Cu-L3
    E = list(np.arange(924,932.09,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )  

    ############################################################    
    # TO BE DONE -- 4hours duration ==> check if alignmnet is needed in between

    #yield from pol_H(0.3)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    #yield from mv(extslt.vg,30, extslt.hg, 150)

    #Cu2OSeO3- Cu-L3
    #E = list(np.arange(924,932.09,0.1))
    #yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )

def plan_second_afternoon(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    yield from pol_H(0.3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Cu2OSeO3- Cu-L3
    E = list(np.arange(924,932.09,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )  

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)


def plan_second_night(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    yield from pol_H(0.3)
    yield from align.m1pit
    yield from m3_check()
    #yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = list(np.arange(923.5,932.59,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Te-Cu2OSeO3' )  

    yield from pol_V(5.5)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = list(np.arange(923.5,932.59,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Te-Cu2OSeO3' )  

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_lunch(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 240
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    #yield from RE
    #yield from align.m1pit
    #yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = [925.5,925.5,926,926.4]
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Te-Cu2OSeO3' )  

    yield from pol_H(0.3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = [925.5,925.5,926,926.4]
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Te-Cu2OSeO3' )  


    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_dinner(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    yield from pol_V(5.5)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = list(np.arange(923.9,932.09,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )  

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)


def plan_third_night(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    #yield from pol_V(5.5)
    #yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = list(np.arange(923.3,923.99,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )  

    yield from pol_H(0.3)
    yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Te-Cu2OSeO3- Cu-L3
    E = list(np.arange(923.3,932.09,0.1))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Cu2OSeO3' )  

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)



def plan_fourth_lunch(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    
    #yield from pol_H(2.1)
    yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Fe film - Fe L
    E = list(np.arange(701.8,710.09,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Fe film' )  

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)


def plan_fourth_night(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 300
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
   
    #yield from pol_H(2.1)
    #yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Fe film - Fe L
    E = list(np.arange(703.5,705.39,0.3))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 5, None, 'Fe film' ) 

    yield from pol_V(5.5)
    yield from sleep(120)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Fe film - Fe L
    E = list(np.arange(703.5,705.39,0.3))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 5, None, 'Fe film' )  
 

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_fifth_afternoon(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 300
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
   
    #yield from pol_H(2.1)
    #yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,30, extslt.hg, 150)

    #Fe film - Fe L
    E = list(np.arange(703.8,705.39,0.3))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 6, None, 'Fe film @ 148 deg' ) 

def plan_highres_Fe(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 360
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
   
    #yield from pol_H(2.1)
    #yield from sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    yield from mv(extslt.vg,25, extslt.hg, 150)

    #Fe film - Fe L
    E = list(np.arange(707.75,713,0.5))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 1, None, 'Fe film @ 123 deg' ) 
    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_fifth_night(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 360
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
   
    #yield from pol_V(4)
    #yield from sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from mv(extslt.vg,50, extslt.hg, 150)
    #LSCuO
    E = list(np.arange(525.5,530.59,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 8, None, 'LSCuO deg' ) 

    yield from pol_H(2.1)
    yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,50, extslt.hg, 150)

    #LSCuO
    E = list(np.arange(525.5,530.59,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 8, None, 'LSCuO deg' ) 

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_fifth_night_am_restart(): 
    dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 360
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
   
    #yield from pol_V(4)
    #yield from sleep(60)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from mv(extslt.vg,50, extslt.hg, 150)
    #LSCuO
    E = list(np.arange(526.7,530.59,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 8, None, 'LSCuO deg' ) 

    yield from pol_H(2.1)
    yield from sleep(60)
    yield from align.m1pit
    yield from m3_check()
    yield from mv(extslt.vg,50, extslt.hg, 150)

    #LSCuO
    E = list(np.arange(525.5,530.59,0.2))
    yield from rixscam_acquire(dets, E,m7_pit_vals, 8, None, 'LSCuO deg' ) 

    yield from mv(rixscam.cam.acquire_time, 20)
    yield from mv(sclr.preset_time, 1)

def plan_sixth_night():
    cryo.t.settle_time=0.1
    ow.settle_time=0.1
    yield from align.m1pit
    yield from m3_check()
    EA = 526.25
    EB = 527.75
    Ebg = 524.5
    
    #T=25 K
    #FIX E-SCANS
    yield from mv(pgm.en,EA)
    yield from mvr(cryo.y,-0.01)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,6,23,ow,12,46,86, md = {'reason':'Reflectivity @ 526.3 eV'})
    yield from mv(pgm.en,EB)
    yield from mvr(cryo.y,-0.01)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,23,6,ow,46,12,86, md = {'reason':'Reflectivity @ 527.75 eV'})
    yield from mv(pgm.en,Ebg)
    yield from mvr(cryo.y,-0.01)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,6,23,ow,12,46,86, md = {'reason':'Reflectivity @ 524.5 eV'})
    #FIX Q-SCANS
    yield from mv(cryo.t,14)
    yield from mv(ow,28)
    yield from scan([sclr,qem12],pgm.en,520,540,201,md={'reason':'Fix-q on LSCuO at 20 K'})
    
    #T=50 K
    yield from mv(stemp.ctrl2.setpoint,50)
    yield from temp_eq(0.5,10)
    yield from sleep(120)
    
    yield from mv(cryo.t,6)
    yield from mv(ow,12)
    yield from align.m1pit
    yield from m3_check()
    #FIX E-SCANS
    yield from mv(pgm.en,EA)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,6,23,ow,12,46,86, md = {'reason':'Reflectivity @ 526.3 eV'})
    yield from mv(pgm.en,EB)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,23,6,ow,46,12,86, md = {'reason':'Reflectivity @ 527.75 eV'})
    yield from mv(pgm.en,Ebg)
    yield from sleep(5)
    yield from scan([sclr,qem12],cryo.t,6,23,ow,12,46,86, md = {'reason':'Reflectivity @ 524.5 eV'})
    #FIX Q-SCANS
    yield from mv(cryo.t,14)
    yield from mv(ow,28)
    yield from scan([sclr,qem12],pgm.en,520,540,201,md={'reason':'Fix-q on LSCuO at 20 K'})



def LNO_test_high_res(): 
    #dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 30
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,20, extslt.hg, 150)
    
    yield from pol_H(-2.6)
    E = list(np.arange(853,853.85)) 
    
    yield from sleep(30)
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 240, 'LNO 20um' )
    
    yield from mv(extslt.vg,10, extslt.hg, 150)

    yield from pol_H(-2.6)
    E = list(np.arange(853,853.85))   
    yield from sleep(30)
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 600, 'LNO 10um' )

    yield from mv(rixscam.cam.acquire_time, 5)
    yield from mv(sclr.preset_time, 0.1)
    yield from count([rixscam])


def ene_calib_ctape(): 
    #dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 15
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,10, extslt.hg, 150)
    
    yield from pol_V(3)
    E = [851,851.5,852,852.5,853,853.5,854]
    
    yield from sleep(10)
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 80, 'elastic 10um' )
    
    yield from mv(extslt.vg,20, extslt.hg, 150)
    rixscam_exp = 10
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E = [853]
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 50, 'elastic 20um' )

    yield from mv(extslt.vg,10, extslt.hg, 150)
    rixscam_exp = 8
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(m4slt.vg,2.2)			
    E = [853]
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 50, 'elastic 10um open M4slt' )
    yield from mv(m4slt.vg,1.2)
    yield from mv(rixscam.cam.acquire_time, 60)
    yield from mv(sclr.preset_time, 0.1)
    yield from count([rixscam])

def cff_test_high_res(): 
    #dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 30
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,10, extslt.hg, 150) 
    yield from pol_H(-2.6)
    
    cff_list=[4.6,4.65,4.7,4.75] 
    for cff in cff_list:
        yield from mv(pgm.cff,cff)
        yield from sleep(10)
        yield from rixscam_acquire_w_shutter([851],m7_pit_vals, 20, 'elastic 10 um' )
  
def cff_test_medium_res(): 
    #dets = [rixscam, sclr, ring_curr]
    rixscam_exp = 180
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,20, extslt.hg, 150) 
    
    yield from rixscam_cff_optimization(extra_md = '500 BL 2500 SP' )

    yield from sleep(7200)

    yield from rixscam_cff_optimization(extra_md = '500 BL 2500 SP' )
    yield from mv(shutterb,'close')
    yield from mv(rixscam.cam.acquire_time, 30)
    yield from mv(sclr.preset_time, 0.1)
    yield from count([rixscam])
 

def m7_gr_optim():

    rixscam_exp = 180
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)
    yield from mv(extslt.vg,20, extslt.hg, 150) 
    yield from rixscam_m7_gr_2_axis(extra_md = '500 BL 2500 SP extslt.vg=20' )

    rixscam_exp = 300
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    yield from mv(extslt.vg,10, extslt.hg, 150) 
    yield from rixscam_m7_gr_2_axis(extra_md = '500 BL 2500 SP extslt.vg=10' )    

    yield from mv(shutterb,'close')
    yield from mv(rixscam.cam.acquire_time, 30)
    yield from mv(sclr.preset_time, 0.1)
    yield from count([rixscam])

def LNO_test():
    rixscam_exp = 300
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(sclr.preset_time, rixscam_exp)

    E = [853.5,854.5]
    m7_pit_vals = None
    yield from rixscam_acquire_w_shutter(E,m7_pit_vals, 4, 'LNO 20 um' )



def plan_coso_300(cts): 
    dets = [rixscam, ring_curr]
    rixscam_exp = 2
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(extslt.vg,10, extslt.hg, 150)
    
    yield from pol_H(-8)
    
    #Cu2OSeO3- Cu-L3
    E1 = list(np.arange(927,931.09,0.1))
    E2 = list(np.arange(931.2,935.09,0.2))
    for i in E1+E2:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 300K'} )  
        

def plan_coso_45(cts): 
    dets = [rixscam, ring_curr]
    rixscam_exp = 5
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(extslt.vg,10, extslt.hg, 150)
    
    yield from pol_H(-8)
    
    #Cu2OSeO3- Cu-L3
    E1 = list(np.arange(933.8,935.09,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  



def plan_Te_coso_45(): 
    dets = [rixscam, ring_curr]
    
    yield from mv(extslt.vg,10, extslt.hg, 150)
    
    yield from pol_H(-8)
    
    #Cu2OSeO3- Cu-L3
    rixscam_exp = 4
    cts=60
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E1 = list(np.arange(927,927.89,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  
        
    rixscam_exp = 2
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E1 = list(np.arange(928,928.89,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  

    rixscam_exp = 1
    cts=240
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E1 = list(np.arange(929,930.29,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  

    rixscam_exp = 2
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E1 = list(np.arange(930.4,930.89,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  

    rixscam_exp = 5
    cts=48
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    E1 = list(np.arange(931,935.09,0.2))
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap COSO 45K'} )  


def plan_coso_45_high_res(): 
    dets = [rixscam, ring_curr]
    
    yield from mv(extslt.vg,15, extslt.hg, 150)
    
    yield from pol_H(-8)
    
    #Cu2OSeO3- Cu-L3
    #rixscam_exp = 6
    #cts=100
    #yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    #yield from mv(pgm.en,929.3)
    #for i in range(0,5):
    #    yield from count(dets, num=cts, md = {'reason':'COSO 45K E1'} )  

    #rixscam_exp = 5
    #cts=120
    #yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    #yield from mv(pgm.en,929.9)
    #for i in range(0,5):
    #    yield from count(dets, num=cts, md = {'reason':'COSO 45K E2'} )  

    rixscam_exp = 5
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,930.6)
    for i in range(0,1):
        yield from count(dets, num=cts, md = {'reason':'COSO 45K E3'} )  

    rixscam_exp = 6
    cts=100
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,931.1)
    for i in range(0,5):
        yield from count(dets, num=cts, md = {'reason':'COSO 45K E4'} )  

    rixscam_exp = 5
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,930.2)
    for i in range(0,5):
        yield from count(dets, num=cts, md = {'reason':'COSO 45K E5'} )  

    yield from pol_V(-1.1)
    rixscam_exp = 5
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,930.2)
    for i in range(0,5):
        yield from count(dets, num=cts, md = {'reason':'COSO 45K E6'} )  

    yield from pol_H(-8)
    rixscam_exp = 6
    cts=100
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,929.6)
    for i in range(0,5):
        yield from count(dets, num=cts, md = {'reason':'COSO 45K E6'} ) 
    
    
    yield from mv(gvbt1,'close')


def plan_fe30uc_emap(): 
    dets = [rixscam, ring_curr]

    yield from mv(extslt.vg,20, extslt.hg, 150)
    
    #yield from pol_H(-2)
    
    #Fe_L
    E1 = list(np.arange(705.4,706.49,0.2)) #8s
    E2 = list(np.arange(706.6,707.69,0.2)) #6s
    E3 = list(np.arange(707.8,708.09,0.2)) #8s
    E4 = list(np.arange(708.5,712.09,0.5)) #8s


    rixscam_exp = 8
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    cts=40
    for i in E1:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap Fe 30uc'} )  

    rixscam_exp = 6
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    cts=53
    for i in E2:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap Fe 30uc'} )  

    rixscam_exp = 8
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    cts=40
    for i in E3+E4:
        yield from mv(pgm.en,i)
        yield from sleep(2)
        yield from count(dets, num=cts, md = {'reason':'Emap Fe 30uc'} )  

    yield from mv(gvbt1,'close')


def plan_fe30uc_ecut(): 
    dets = [rixscam, ring_curr]
    yield from mv(extslt.vg,11, extslt.hg, 150)
    #yield from pol_H(-2)
    rixscam_exp = 5
    cts=120
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,706.8)
    for i in range(0,6):
        yield from count(dets, num=cts, md = {'reason':'Fe30uc 706.8eV 130deg'} )


def plan_fe3uc_6uc_ecut(): 
    dets = [rixscam, ring_curr]
    yield from mv(extslt.vg,15, extslt.hg, 150)
    #yield from pol_H(-2)
    rixscam_exp = 5
    cts=120
    # Fe 3uc
    #yield from mv(cryo.y,28.65)
    #yield from mv(cryo.x,26.335)
    #yield from mv(cryo.z,15.295)
    #yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    #yield from mv(pgm.en,706.8)
    #yield from sleep(5)
    #for i in range(0,15):
        #yield from count(dets, num=cts, md = {'reason':'Fe3uc 706.8eV 130deg'} )
    
    # Fe 6uc
    #yield from mv(cryo.y,24.8)
    #yield from mv(cryo.x,26.335)
    #yield from mv(cryo.z,15.365)
    #yield from mv(pgm.en,706.8)
    #yield from sleep(5)
    for i in range(0,18):
        yield from count(dets, num=cts, md = {'reason':'Fe6uc 706.8eV 130deg'} )
    
    yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'close')
    yield from mv(shutterb,'close')

def plan_fe3uc_ecut(): 
    dets = [rixscam, ring_curr]
    yield from mv(extslt.vg,15, extslt.hg, 150)
    #yield from pol_H(-2)
    rixscam_exp = 5
    cts=120
    # Fe 3uc
    #yield from mv(cryo.y,28.65)
    #yield from mv(cryo.x,26.31)
    #yield from mv(cryo.z,15.835)
    yield from mv(rixscam.cam.acquire_time, rixscam_exp)
    yield from mv(pgm.en,706.8)
    yield from sleep(5)
    for i in range(0,24):
        yield from count(dets, num=cts, md = {'reason':'Fe3uc 706.8eV'} )
    
    yield from mv(gvbt1,'close')
    yield from mv(shutterb,'close')
    





