
def mixed_gascell2_vs_cff():
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,150)
    ene_n2=400.3
    yield from gcdiag.grid
    yield from mv(pgm.en,ene_n2)
    yield from pol_H(2.2)
    #yield from sleep(600)
    #yield from align.m1pit
    #yield from m3_check()

    for i in list(np.arange(4.1,5.6,0.1)):
        yield from mv(pgm.cff,i)
        yield from mv(pgm.en,398.8)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,398.8,403.0,421, md = {'reason':'N2-K XAS vs c_ff, vg=10 um'})


 
def mixed_gascell_vs_cff_ubg():
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,150)
    ene_n2=400.4
    ene_neon=867.2 
        
    yield from mv(sclr.preset_time, 1)   

    #yield from gcdiag.grid
    yield from pgm.ubg
 
    #yield from mv(m1_fbk,0) 

    #yield from mv(pgm.cff,4.55)
    #yield from mv(pgm.en,ene_n2)
    #yield from pol_H(3.5)   #  THIS IS BETTER mv(epu1.offset,3.5)  
    #yield from sleep(100)
    #yield from align.m1pit
    #yield from m3_check()

    #yield from mv(m1_fbk_cam_time,1)
    #yield from mv(m1_fbk_th,1500)
    #yield from sleep(2)
    #yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.value)
    
    #yield from mv(m1_fbk,1)
    #yield from sleep(2)
    
    #for i in list(np.arange(4.1,5.21,0.1)):
        #yield from mv(pgm.cff,i)
        #yield from mv(pgm.en,398.8)
        #yield from sleep(10)
        #yield from scan([sclr,ring_curr],pgm.en,398.8,403.0,421, md = {'reason':'ubg N2-K XAS vs c_ff'})

    #yield from mv(m1_fbk,0)
    
    #yield from mv(pgm.cff,4.6)
    #yield from mv(pgm.en,ene_neon)
    #yield from pol_H(2.5)     #  THIS IS BETTER mv(epu1.offset,2.5)
    #yield from sleep(100)
    #yield from align.m1pit
    #yield from m3_check()
    
    #yield from mv(m1_fbk_cam_time,0.2)
    #yield from mv(m1_fbk_th,1500)
    #yield from sleep(2)
    #yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.value)

    #yield from mv(m1_fbk,1)
    #yield from sleep(2)
    for i in list(np.arange(4.0,5.01,0.1)):
        yield from mv(pgm.cff,i)
        yield from mv(pgm.en,864)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,864,872,401, md = {'reason':'ubg Ne-K XAS vs c_ff'})

    yield from mv(pgm.cff,4.4)

def mixed_gascell_vs_cff_mbg():
    
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    ene_n2=400.55
    ene_neon=867.2 
        
    yield from mv(sclr.preset_time, 1)   

    #yield from gcdiag.grid
    #yield from pgm.mbg

    #yield from mv(m1_fbk,0)
    
    #yield from mv(pgm.cff,2.25)
    #yield from mv(pgm.en,ene_neon)
    #yield from mv(epu1.offset,3.5) #checked on 01/30/2019
    #yield from sleep(100)
    #yield from align.m1pit
    #yield from m3_check()
    
    #yield from mv(m1_fbk_cam_time,0.001)
    #yield from mv(m1_fbk_th,2000)
    #yield from sleep(20)
    #yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.value)

    #yield from mv(m1_fbk,1)
    
    #yield from mv(extslt.vg,30)
    #yield from sleep(2)
    for i in list(np.arange(2.18,2.321,0.02)):
        yield from mv(pgm.cff,i)
        yield from mv(pgm.en,864)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,864.0,872.0,401, md = {'reason':'mbg Ne XAS vs c_ff 30um'})

 
    #yield from mv(m1_fbk,0) 

    #yield from mv(pgm.cff,2.15)
    #yield from mv(pgm.en,ene_n2)
    #yield from mv(epu1.offset,2.5)  #checked on 01/30/2019
    #yield from sleep(300)
    #yield from align.m1pit
    #yield from m3_check()

    #yield from mv(m1_fbk_cam_time,0.005)
    #yield from mv(m1_fbk_th,1400)
    #yield from sleep(20)
    #yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.value)
    
    #yield from mv(m1_fbk,1)
    yield from mv(extslt.vg,30)
    yield from mv(sclr.preset_time, 1) 
    #yield from sleep(300)
    
   # for i in list(np.arange(2.16,2.341,0.02)):
        #yield from mv(pgm.cff,i)
        #yield from mv(pgm.en,398.5)
        #yield from sleep(10)
        #yield from scan([sclr,ring_curr],pgm.en,398.5,403.0,451, md = {'reason':'mbg N2 XAS vs c_ff 30um'})

    yield from mv(shutterb,'close')
    #yield from pgm.ubg


def mixed_gascell_vs_extslt():
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    ene_n2=400.3
    ene_neon=866.2 
    best_cff = 2.32
    best_cff_neon = 2.24
    extslt_vgs = [30, 10]
    yield from gcdiag.grid
    #yield from mv(pgm.en,ene_n2)
    #yield from pol_H(2.2)
    #yield from sleep(600)
    #yield from align.m1pit
    #yield from m3_check()

    yield from mv(pgm.cff,best_cff_neon)

    for gap in extslt_vgs:
        yield from mv(extslt.vg,gap)
        yield from mv(pgm.en,863)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,863.0,871.0,401, md = {'reason':'Neon-K XAS vs extslt vg {:.0f}'.format(gap)})

 

    #yield from mv(pgm.en,ene_neon)
    #yield from pol_H(-2.8)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(300)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(900)
    #yield from align.m1pit
    #yield from m3_check()

    #yield from mv(pgm.cff,best_cff_neon)
    #for gap in extslt_vgs:
        #yield from mv(extslt.vg,gap)
        #yield from mv(pgm.en,863)
        #yield from sleep(10)
        #yield from scan([qem07,ring_curr],pgm.en,863.5,870.5,251, md = {'reason':'Ne-K XAS vs extslt vg {:.0f}'.format(gap)})


    #yield from align.m1pit
    #yield from m3_check()
    #for gap in extslt_vgs:
        #yield from mv(extslt.vg,gap)
        #yield from mv(pgm.en,863)
        #yield from sleep(10)
        #yield from scan([qem07,ring_curr],pgm.en,863,871,301, md = {'reason':'Ne-K XAS vs extslt vg {:.0f}'.format(gap)})

def mixed_gascell2_vs_exitslit():
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,150)
    ene_n2=400.3
    yield from gcdiag.grid
    yield from mv(pgm.en,ene_n2)
    yield from pol_H(2.2)
    #yield from sleep(600)
    #yield from align.m1pit
    #yield from m3_check()

    #yield from mv(pgm.en,398.8)
    #yield from sleep(10)
    #yield from scan([sclr,ring_curr],pgm.en,398.8,403.0,421, md = {'reason':'N2-K XAS vs c_ff, c_ff=4.55'})
    for i in list(np.arange(140,221,20)):
        yield from mv(extslt.vg,i)
        yield from mv(pgm.en,398.8)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,398.8,403.0,421, md = {'reason':'N2-K XAS vs c_ff, c_ff=4.55'})


def mixed_gascell_escan_thermalization():
    meta_data = 'ubg N2-K XAS - baseline'
    uid = yield from scan([sclr,ring_curr],pgm.en,400.25, 401.75, 151, md = {'reason':meta_data})     
    #    if uid == None:
    #        uid = -1
    #    f_string += 'scan no ' + str(db[uid].start['scan_id']) + 'reason = ' + str(meta_data) + '\n'#\
    yield from mv(shuttera,'close') 
    yield from sleep(30*60)
    yield from mv(shuttera,'open')
    meta_data = 'ubg N2-K XAS - warmup no m1fb'
    #while True:
    #    #
    #    yield from scan([sclr,ring_curr],pgm.en,400.25, 401.75, 151, md = {'reason':meta_data})
    #    if uid == None:
    #        uid = -1
    #    f_string += 'scan no ' + str(db[uid].start['scan_id']) + 'reason = ' + str(meta_data) + '\n'#\


def n2gascell_vs_cff():
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    ene_n2=400.3
    cff_ideal_500=2.23
    yield from gcdiag.grid
    #yield from pol_H(2.2)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from mv(pgm.en,398.5)
    #yield from sleep(10)
    #yield from scan([qem07,ring_curr],pgm.en,398.5,403.5,401)

    #for i in range(-5, 6):
        #yield from mv(pgm.cff,cff_ideal_500+i*0.02)
        #yield from mv(pgm.en,398.5)
        #yield from sleep(10)
        #yield from scan([qem07,ring_curr],pgm.en,398.5,403.5,401)

    #yield from pol_V(3)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from mv(pgm.en,398.5)

    for i in range(5, 9):
        yield from mv(pgm.cff,cff_ideal_500+i*0.02)
        yield from mv(pgm.en,399.4)
        yield from sleep(10)
        yield from scan([sclr,ring_curr],pgm.en,399.4,403.4,401)

def neon_gascell_vs_cff():
    
    ene_neon=867.2 
    cff_ideal_500=2.24
    #cff_ideal_1800=5.2428
    cff_ideal_1800 = 4.25
    
    det_list=[sclr, ring_curr]
    yield from mv(sclr.preset_time, 1)
    yield from mv(extslt.hg,150)
    
    ###################### grating 1800l/mm  ###############################
    #yield from pgm.ubg    
    #yield from mv(pgm.cff, cff_ideal_1800)
    #yield from mv(pgm.en,ene_neon)
    #yield from sleep(100)
    #yield from beamline_align_v2() ## Remember to check eletrometer for m3_check!!!!!
   
    yield from mv(extslt.vg,11)
    #yield from scan(det_list,pgm.en,864,872,401)
    
    offset=0

    for i in range(-7, 8):
        yield from mv(pgm.cff,cff_ideal_1800+i*0.05) #fine
        yield from sleep(10)
        yield from mv(pgm.en,864-offset)
        yield from sleep(30)
        yield from scan(det_list,pgm.en,864-offset,872-offset,401)

    yield from mv(pgm.cff,cff_ideal_1800)
    yield from mv(pgm.en, 867.16)
    yield from sleep(30)
    yield from count(det_list,num=36000)
    #yield from pgm.ubg
    #yield from mv(pgm.cff, cff_ideal_1800)
    #yield from mv(pgm.en,ene_neon) 
    #yield from mv(extslt.vg,10)

    

    ######################### Grating 500l/mm  ##################################3
    #yield from pgm.mbg 
    #yield from sleep(300)
    #yield from mv(pgm.m2pit,88.28578)
    #yield from mv(pgm.grpit,87.60104)
    #yield from mv(pgm.cff, cff_ideal_500)
    #yield from mv(pgm.en, 867)
    
    #yield from mv(extslt.vg,7)
    #yield from beamline_align_v2()
    #yield from sleep(3600)
    #yield from beamline_align_v2()

    #offset=0
    
    #for i in range(-7, 8):
    #    yield from mv(pgm.cff,cff_ideal_500+i*0.05) #fine
    #    yield from mv(pgm.en,863-offset)
    #    yield from sleep(30)
    #    yield from scan(det_list,pgm.en,863-offset,873-offset,251)
    #yield from mv(pgm.cff,cff_ideal_500)
    

def gas_cell_gr500():
    ######################### Grating 500l/mm  ##################################
    det_list=[sclr, ring_curr]
    yield from mv(sclr.preset_time, 1)
    yield from mv(extslt.hg,150)

    cff_ideal_500 = 2.20
    yield from mv(pgm.cff, cff_ideal_500)
    yield from mv(extslt.vg,11)
    offset=0
    
    for i in range(-4, 5):
        yield from mv(pgm.cff,cff_ideal_500+i*0.02) #fine
        yield from mv(pgm.en,864-offset)
        yield from sleep(30)
        yield from scan(det_list,pgm.en,864-offset,872-offset,201)
    yield from mv(pgm.cff,cff_ideal_500)


def gas_cell_gr1800():
    ######################### Grating 1800l/mm  ##################################
    det_list=[sclr, ring_curr]
    yield from mv(sclr.preset_time, 1)
    yield from mv(extslt.hg,150)
    yield from sleep(3600)
    yield from beamline_align_v2()
    yield from sleep(120)
    cff_ideal_1800 = 4.40
    yield from mv(pgm.cff, cff_ideal_1800)
    yield from mv(extslt.vg,11)
    offset=0

    yield from scan(det_list,pgm.en,864-offset,872-offset,401)
    for i in range(-6, 7):
        yield from mv(pgm.cff,cff_ideal_1800+i*0.025) #fine
        yield from mv(pgm.en,864-offset)
        yield from sleep(30)
        yield from scan(det_list,pgm.en,864-offset,872-offset,401)
    yield from mv(pgm.cff,cff_ideal_1800)



def n2gascell_vs_M1roll():
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,300)
    yield from mv(pgm.cff,2.3277)
    yield from mv(pgm.en,398.8)
    yield from sleep(10)

    yield from multi_scan([qem07],5,m1.rol,1700,2500,pgm.en,398.8,402.3,num=301)

def n2gascell_vs_M3yaw_M3y():
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,300)
    yield from mv(pgm.cff,2.3277)
    yield from mv(pgm.en,400)
    yield from sleep(10)

    yield from multi_scan([qem07],5,m3.yaw,-0.75,-0.25,pgm.en,401.8,405.5,num=351)

    yield from mv(m3.yaw,-0.5)
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    yield from mv(pgm.cff,2.3277)
    yield from mv(pgm.en,400)
    yield from sleep(10)

    yield from multi_scan([qem07],5,m3.y,-0.05,0.05,pgm.en,401.8,405.5,num=351)

    yield from mv(m3.y,0)

