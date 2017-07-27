def epu_calib_gs_phase_28p5_1sth():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    gs.DETS.append(epu1.phase)

    gs.MONITORS=[]
    #Using Gas Cell Grid as detector
    yield from bp.mv(gc_diag,-94.4)
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'
    
    yield from bp.mv(epu1.phase, 28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)



    #1st Harmonic at 320 eV
    yield from bp.mv(pgm.en,320,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,30)
    yield from bp.mv(epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,50)


    #1st Harmonic
    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,3,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    for i in range(450,1501,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)  



def epu_calib_gs_phase_28p5_3rd():
    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    gs.DETS.append(epu1.phase)

    gs.MONITORS=[]
    #Using Gas Cell Grid as detector
    yield from bp.mv(gc_diag,-94.4)
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'
    
    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    yield from bp.mv(epu1.phase, 28.5)


    #3rd Harmonic
    for i in range(1000,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)

def epu_calib_gs_phase_0():
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
    
    yield from bp.mv(epu1.phase, 0)

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



def epu_calib_gs_phase_pm28p5_0mm():

    gs.DETS=[]
    gs.DETS.append(qem07)
    gs.DETS.append(pgm.m2_pit)
    gs.DETS.append(pgm.gr_pit)
    gs.DETS.append(pgm.en)
    gs.DETS.append(feslt.hg.setpoint)
    gs.DETS.append(feslt.vg.setpoint)
    gs.DETS.append(epu1.phase)
    gs.DETS.append(extslt.hg)
    gs.DETS.append(extslt.vg)

    gs.MONITORS=[]
    #Using Gas Cell Grid as detector
    yield from bp.mv(gc_diag,-94.4)
    gs.TABLE_COLS=['gc_diag_grid']
    gs.PLOT_Y='gc_diag_grid'
    
    #################
    # Phase -28.5mm #
    #################
    yield from bp.mv(epu1.phase, -28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #1st Harmonic at 320 eV
    yield from bp.mv(pgm.en,320,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,30)
    yield from bp.mv(epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,50)

    #1st Harmonic
    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,3,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    for i in range(450,1501,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)  
    
    yield from bp.sleep(100)
    #3rd Harmonic
    for i in range(1000,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)


    #################
    # Phase 0.0 mm  #
    #################

    yield from bp.mv(epu1.phase, 0)

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


    #################
    # Phase 28.5mm  #
    #################
    yield from bp.mv(epu1.phase, 28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from bp.mv(feslt.hg,1.2)
    yield from bp.mv(feslt.vg,1.2)
    yield from bp.mv(pgm.cff,2.330)

    #1st Harmonic at 320 eV
    yield from bp.mv(pgm.en,320,epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,30)
    yield from bp.mv(epu1.gap,17.05)
    yield from bp.sleep(10)
    yield from dscan(epu1.gap,0,1,50)

    #1st Harmonic
    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,3,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)

    for i in range(450,1501,50):
        calc_gap=e2g(i)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,6,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-1)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,100)  
    
    yield from bp.sleep(100)
    #3rd Harmonic
    for i in range(1000,1601,50):
        calc_gap=e2g(i/3)
        yield from bp.mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,2,30)
        yield from bp.mv(epu1.gap,gs.PS.max[0]-0.5)
        yield from bp.sleep(10)
        yield from dscan(epu1.gap,0,1.0,75)






