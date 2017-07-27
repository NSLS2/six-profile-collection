def epu_calib_gs_phase_28p5_test():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    gs.DETS.append(epu1.phase)

    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'
    
    yield from bp.mv(epu1.phase, 28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)


    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,3,30)
        #yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        #yield from bp.sleep(10)
        #yield from dscan(epu1.gap,0,2,100)

    for i in range(450,1501,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        #yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        #yield from bp.sleep(10)
        #yield from dscan(epu1.gap,0,2,100)  


def epu_calib_gs_5():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)

    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'


    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #160 eV
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)

    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    yield from bp.sleep(100)
    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-2)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,4,40)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)


def epu_calib_gs_4():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)

    gs.MONITORS=[]
    #Using Grid for third harmonic
    yield from bp.mv(gc_diag,-94.4) 
    gs.PLOT_Y='gc_diag_grid' 
    gs.TABLE_COLS=['gc_diag_grid','pgm_en','feslt_hg_setpoint','feslt_vg_setpoint']
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-2)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,4,40)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)

    #FE slit H and V gap to 1.5 mm
    yield from bp.mv(feslt.hg,1.5)
    yield from bp.mv(feslt.vg,1.5)
    yield from bp.mv(pgm.cff,2.330)

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-2)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,4,40)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)

    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)

def joescan2():

    # read gas cell Au grid
    # yield from gcd_grid()
    # yield from bp.sleep(120)
    qem07.read_attrs=['current3.mean_value']
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'

    GRang, PMang = generatePGMscan(400.8, 500, startGR=89.0, stopGR=90.0, 
                    startPM=89.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[0], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)


def joescan1():
    # read gas cell photodiode
    yield from gcd_diode()
    yield from bp.sleep(120)
    qem07.read_attrs=['current1.mean_value']
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_diode']
    gs.PLOT_Y='gc_diag_diode'

    GRang, PMang = generatePGMscan(400.8, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[2], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)

    GRang, PMang = generatePGMscan(400.8, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[1], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)

    GRang, PMang = generatePGMscan(400.8, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[-1], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)

    GRang, PMang = generatePGMscan(400.8, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[-2], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)

    # read gas cell Au grid
    yield from gcd_grid()
    yield from bp.sleep(120)
    qem07.read_attrs=['current3.mean_value']
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'

    GRang, PMang = generatePGMscan(400.8, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[0], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from bp.mv(pgm.m2_pit, i, pgm.gr_pit, j)
        yield from dscan(pgm.gr_pit,-0.015,0.015,61)

def epu_calib_gs():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg)
    gs.DETS.append(feslt.vg)
    
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'

    yield from bp.mv(pgm.cff,2.330)
    
    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)



def epu_calib_gs_2():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg)
    gs.DETS.append(feslt.vg)
    
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_diode']
    gs.PLOT_Y='gc_diag_diode'

    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #160 eV
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    
    #200-1350 eV, 1st harmonic
    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    #FE slit H and V gap to 1.5 mm
    yield from bp.mv(feslt.hg,1.5)
    yield from bp.mv(feslt.vg,1.5)

    #160 eV
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    
    #200-1350 eV, 1st harmonic
    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

def epu_calib_gs_3():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_diode','pgm_en','feslt_hg_setpoint','feslt_vg_setpoint']
    gs.PLOT_Y='gc_diag_diode'

   
    #FE slit H and V gap to 1.5 mm
    yield from bp.mv(feslt.hg,1.5)
    yield from bp.mv(feslt.vg,1.5)

    #160 eV
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    yield from bp.mv(pgm.en,160,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,75)
    
    #200-1350 eV, 1st harmonic
    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    #Using Grid for third harmonic
    yield from bp.mv(gc_diag,-94.4)
    gs.TABLE_COLS=['gc_diag_grid','pgm_en','feslt_hg_setpoint','feslt_vg_setpoint']
    gs.PLOT_Y='gc_diag_grid'    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-2.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,5,50)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)

    #FE slit H and V gap to 1.5 mm
    yield from bp.mv(feslt.hg,1.5)
    yield from bp.mv(feslt.vg,1.5)
    yield from bp.mv(pgm.cff,2.330)
    

    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-2.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,5,50)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)

    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
        

def epu_calib_gs_3_test():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    
    gs.MONITORS=[]
    gs.TABLE_COLS=['gc_diag_diode']
    gs.PLOT_Y='gc_diag_diode'

    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #600-1550 eV, 3rd harmonic
    for i in range(600,650,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,6)


    #FE slit H and V gap to 1.5 mm
    yield from bp.mv(feslt.hg,1.5)
    yield from bp.mv(feslt.vg,1.5)

        
    #200-1350 eV, 1st harmonic
    for i in range(600,650,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,6)

    #600-1550 eV, 3rd harmonic
    for i in range(600,650,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,6)

        
def epu_calib():
    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,ring_curr,pgm.m2_pit,pgm.gr_pit]
    PS =PeakStats('epu1_gap_setpoint','gc_diag_grid')    

    yield from bp.mv(pgm.cff,2.330)
    
    for i in range(250,401,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap)
        yield from bp.sleep(10)
        #yield from relative_scan(d,epu1.gap,-3,3,30), PS
        yield from bp.mv(epu1.gap,PS.max[0])
        yield from bp.sleep(10)
        yield from relative_scan(d,epu1.gap,-1,1,30)


def xassearch():
    for i in range(0, 7):
        yield from bp.mv(m4_diag1,-62-i*0.5)
        print('Moving m4_diag_1 to ',m4_diag1.user_readback.value)
        yield from a2scan(pgm.en,870,990,epu1.gap,39.05,41.8,240)


def gascell2():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
        
    for i in range(0, 8):
        yield from bp.mv(extslt.vg,10+i*5)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)



def gascell_vs_cff_lunch():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,extslt.vg,pgm.cff]
    gs.BASELINE_DEVICES = [qem07.integration_time, qem07.em_range, qem07.averaging_time]

    yield from bp.mv(extslt.vg,40)
    yield from bp.mv(pgm.cff,2.320)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    yield from bp.mv(pgm.cff,2.320)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,20)
    yield from bp.mv(pgm.cff,2.320)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,40)
    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,20)
    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

def gascell_vs_cff8():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,ring_curr, pgm.m2_pit, pgm.gr_pit]
   
    yield from bp.mv(gc_diag,-94.4)
    yield from bp.mv(pgm.cff,2.32533)

    yield from bp.mv(extslt.vg,50)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(extslt.vg,40)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(extslt.vg,30)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(extslt.vg,20)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)
    

def gascell_vs_cff7():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,ring_curr, pgm.m2_pit, pgm.gr_pit]
   
    yield from bp.mv(gc_diag,-94.4)
    yield from bp.mv(extslt.vg,30)

    yield from bp.mv(pgm.cff,2.32533)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)
    
    for i in range(0, 31):
        yield from bp.mv(pgm.cff,2.02533+i*0.02)
        yield from bp.mv(pgm.en,243, epu1.gap,21.88)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(pgm.cff,2.32533)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(pgm.en,242,epu1.gap,21.832)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 600, pgm.en, 242, 252, epu1.gap, 21.832, 22.275)

    yield from bp.mv(gc_diag,-93.7)
    yield from bp.mv(extslt.vg,30)

    yield from bp.mv(pgm.cff,2.32533)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)
    
    for i in range(0, 31):
        yield from bp.mv(pgm.cff,2.02533+i*0.02)
        yield from bp.mv(pgm.en,243, epu1.gap,21.88)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(pgm.cff,2.32533)
    yield from bp.mv(pgm.en,243,epu1.gap,21.88)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 200, pgm.en, 243, 245.5, epu1.gap, 21.88, 21.992)

    yield from bp.mv(pgm.en,242,epu1.gap,21.832)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 600, pgm.en, 242, 252, epu1.gap, 21.832, 22.275)
    
    

    
        
def gascell_vs_cff6():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,ring_curr, pgm.m2_pit, pgm.gr_pit]
   
    yield from bp.mv(gc_diag,-94.4)
    yield from bp.mv(extslt.vg,30)
    
    yield from bp.mv(extslt.vg,30)
    for i in range(0, 5):
        yield from bp.mv(pgm.cff,2.2677+i*0.03)
        yield from bp.mv(pgm.en,864, epu1.gap,39.51)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 320, pgm.en, 864, 872, epu1.gap, 39.51, 39.70)
        
     
def gascell_vs_cff5():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,ring_curr, pgm.m2_pit, pgm.gr_pit]
   
    yield from bp.mv(gc_diag,-94.4)
    yield from bp.mv(extslt.vg,30)
    
    yield from bp.mv(pgm.cff,2.3277)
    yield from bp.mv(pgm.en,864, epu1.gap,39.51)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 320, pgm.en, 864, 872, epu1.gap, 39.51, 39.70)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0277+i*0.03)
        yield from bp.mv(pgm.en,864, epu1.gap,39.51)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 320, pgm.en, 864, 872, epu1.gap, 39.51, 39.70)

    yield from bp.mv(pgm.cff,2.3277)
    yield from bp.mv(pgm.en,864, epu1.gap,39.51)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 320, pgm.en, 864, 872, epu1.gap, 39.51, 39.70)


    yield from bp.mv(gc_diag,-93.7)
    yield from bp.mv(extslt.vg,30)
    
    yield from bp.mv(pgm.cff,2.3277)
    yield from bp.mv(pgm.en,864, epu1.gap,39.51)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 320, pgm.en, 864, 872, epu1.gap, 39.51, 39.70)

def gascell_vs_cff4():
    
    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,extslt.vg,pgm.cff,ring_curr]
   
    yield from bp.mv(gc_diag,-93.7)
    yield from bp.mv(extslt.vg,30)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(gc_diag,-94.4)
    yield from bp.mv(extslt.vg,30)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)


def gascell_vs_cff3():

    qem07.read_attrs = ['current3.mean_value']
    d = [qem07,extslt.vg,pgm.cff]
    gs.BASELINE_DEVICES = [qem07.integration_time, qem07.em_range, qem07.averaging_time]

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)

  
    yield from bp.mv(extslt.vg,20)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)


    yield from bp.mv(extslt.vg,40)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from inner_product_scan(d, 290, pgm.en, 399, 402.5, epu1.gap, 27.601, 27.72)


def gascell_vs_cff2():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,20)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,40)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)
        

def gascell_vs_cff():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.451)
    yield from bp.sleep(10)
    yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)
    
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)

    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)

    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)
        

        

def FEscan2():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)
        
    yield from bp.mv(feslt.hg,0.33)
    yield from bp.mv(feslt.vg,0.33)
    yield from bp.mv(epu1.gap,41.3)
    
    for i in range(0, 5):
        yield from bp.mv(feslt.vc,0.66-0.33*i)
        for j in range(0, 5):
            yield from bp.mv(feslt.hc,0.66-0.33*j)
            yield from bp.mv(pgm.en,900)
            yield from bp.sleep(5)
            yield from ascan(pgm.en,900,970,70)


def FEscan3():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    for i in range(0, 7):
        yield from bp.mv(feslt.vc,0.6-0.2*i)
        for j in range(0, 7):
            yield from bp.mv(feslt.hc,0.6-0.2*j)
            yield from bp.mv(pgm.en,880)
            yield from bp.sleep(5)
            yield from ascan(pgm.en,880,960,80)     
   
def FEscan4():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    yield from bp.mv(feslt.vc,-0.6)
    for j in range(0, 7):
        yield from bp.mv(feslt.hc,0.6-0.2*j)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(5)
        yield from ascan(pgm.en,880,960,80)  

            
            
def FEscan():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)
        
    #yield from bp.mv(feslt.hg,1)
    #yield from bp.mv(feslt.vg,1)
    yield from bp.mv(epu1.gap,41.3)
    
    for i in range(0, 7):
        yield from bp.mv(feslt.vc,-3+i)
        for j in range(0, 7):
            yield from bp.mv(feslt.hc,-3+j)
            yield from bp.mv(pgm.en,900)
            yield from bp.sleep(10)
            yield from ascan(pgm.en,900,970,210)
  


def FEscan_gap():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)


    yield from bp.mv(feslt.hc,0)
    yield from bp.mv(feslt.vc,0)
    yield from bp.mv(epu1.gap,41.3)
    
 # Check Vertical Gap   
    yield from bp.mv(feslt.hg,1.5) 
    yield from bp.mv(feslt.vg,1.5)
    
    for i in range(0, 12):
        yield from bp.mv(feslt.vg,1.5-0.1*i)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(10)
        yield from ascan(pgm.en,880,960,80)     

 # Check Horizontal Gap   
    yield from bp.mv(feslt.hg,1.5) 
    yield from bp.mv(feslt.vg,1.5) 

    for i in range(0, 12):
        yield from bp.mv(feslt.hg,1.5-0.1*i)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(10)
        yield from ascan(pgm.en,880,960,80)     

# Repeat FE Slit Center Search
    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    for i in range(0, 9):
        yield from bp.mv(feslt.vc,0.8-0.2*i)
        for j in range(0, 9):
            yield from bp.mv(feslt.hc,0.8-0.2*j)
            yield from bp.mv(pgm.en,880)
            yield from bp.sleep(10)
            yield from ascan(pgm.en,880,960,80) 



def Jun29lunch():
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    #feslt.vg is 0.2, fesl.hg is 1.5
    yield from ascan(pgm.en,880,960,80)
    yield from bp.mv(feslt.vg,1.5,feslt.hg,0.3)   
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    yield from ascan(pgm.en,880,960,80)
    yield from bp.mv(feslt.vg,1.5,feslt.hg,0.2)
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    yield from ascan(pgm.en,880,960,80)


        
#pitch mirror 1
#change something
#scan again

#def myplan():
   # mir1[0.234,0.236,0.336]
   # for i range(0,4):
    #    yield from bp.mv(m1.pit,mir1[i])
    #   print('Moving M1 to ',m1.pit.user_readback.value)
    #    yield from bp.mv()
    #    yield from dscan(m3.pit,-0.2,0.22,0)
        # this should work below
    #    olog('Scan ID {} m3 pitch scan {}m1 pitch {} m3 trans'.format(db[-1].start.scan_id,m1.pit.user_readback.value,m3.x.user_readback.value))
        

#def myplan2(m1_stp,m3_stp):
   # m1_start = m1.pit.user_readback.value
   # m3_start = m3.x.user_readback.value
   # yield from bp.sleep(0.3)
   # for i range(0,4):
       # yield from bp.mv(m1.pit,m1_start+i*m1_stp,m3.x+i*m3_stp)
       # yield from dscan(m3.pit,-0.2,0.2,20)
        #olog()
    
