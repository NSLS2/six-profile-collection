def epu_calib_gr500(dets = [sclr, ring_curr]):

    print('\n\n WARNING WARNING WARNING:\n\t check if there scalar is installed or not!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t this assumes epu interpolation table is DISABLED!!!!')
    yield from gcdiag.diode

    # srs settings for diode =  SRS settings:  5  x10  uA/v , time = 1.0
 
    #yield from mv(feslt.hg,2.0)
    #yield from mv(feslt.vg,2.0)
    #yield from bp.mv(pgm.cff,2.32)
    yield from mv(extslt.hg,300)
    yield from mv(extslt.vg,30)
    #180 eV
    yield from mv(pgm.en,180)
    yield from mv(epu1.gap, 18.01)
    yield from sleep(10)
    yield from rel_scan(dets,epu1.gap,0,1.5,76)
    yield from mv(epu1.gap, 18.01)
    yield from sleep(10)
    yield from rel_scan(dets, epu1.gap,0,1.5,76)

    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,6,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0] -1)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,101)

    yield from sleep(100)
    #800-1600 eV, 3rd harmonic
    for i in range(800,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,4,41)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0]-0.5)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,1.0,76)

    calc_gap=e2g(850)
    yield from mv(pgm.en,850)
    yield from sleep(5)
    yield from mv(epu1.gap,39.387)
    yield from mv(shutterb,'close') 
    print('\n\n WARNING WARNING WARNING:\n\t EPU Table/Interpolation disabled!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t M1 Feedback disabled!!!!')
    


def epu_calib_gr1800(dets = [sclr, ring_curr]):

    print('\n\n WARNING WARNING WARNING:\n\t check if there scalar is installed or not!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t this assumes epu interpolation table is DISABLED!!!!')
    yield from gcdiag.diode

    # srs settings for diode =  SRS settings:  5  x1  uA/v , time = 1.0
 
    yield from mv(epu1.phase, 0)
    #yield from mv(feslt.hg,2.0)
    #yield from mv(feslt.vg,2.0)
    #yield from bp.mv(pgm.cff,5.2707)

    for i in range(250,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,6,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0] -1)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,101)

    yield from sleep(100)
    #800-1550 eV, 3rd harmonic
    for i in range(800,2001,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,4,41)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0]-0.5)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,1.0,76)

    calc_gap=e2g(850)
    yield from mv(pgm.en,850)
    yield from sleep(5)
    yield from mv(epu1.gap,calc_gap)
    

def epu_calib_ph28p5_gr500(dets = [sclr, ring_curr]):

    print('\n\n WARNING WARNING WARNING:\n\t check if there scalar is installed or not!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t this assumes epu interpolation table is DISABLED!!!!')

    yield from gcdiag.diode
    yield from mv(extslt.hg,300)
    yield from mv(extslt.vg,30)

    # srs settings for diode =  SRS settings: 5  x10  uA/v , time = 1.0
    # Current gap limit is 18mm
 
    yield from mv(epu1.phase, 28.5)
    #yield from mv(feslt.hg,2.0)
    #yield from mv(feslt.vg,2.0)
    #yield from bp.mv(pgm.cff,2.24) 

	#1st Harmonic at 320 eV
    #yield from mv(pgm.en,320,epu1.gap,17.05)
    #yield from sleep(10)
    #yield from rel_scan(dets,epu1.gap,0,1,30)
    #yield from mv(epu1.gap,17.05)
    #yield from sleep(10)
    #yield from rel_scan(dets,epu1.gap,0,1,50)

    #1st Harmonic
    for i in range(400,451,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,3,30)
        yield from mv(epu1.gap,peaks['max']['sclr_channels_chan2'][0]-1)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,2,100)

    for i in range(500,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,6,30)
        yield from mv(epu1.gap,peaks['max']['sclr_channels_chan2'][0]-1)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,2,100)

    yield from sleep(100)
    #3rd Harmonic
    for i in range(1100,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,2,30)
        yield from mv(epu1.gap,peaks['max']['sclr_channels_chan2'][0]-0.5)
        yield from sleep(10)
        yield from rel_scan(dets,epu1.gap,0,1.0,75)

    yield from mv(pgm.en,931.6)
    yield from sleep(5)
    yield from mv(epu1.gap,29.56)
    yield from mv(shutterb,'close') 


def epu_calib_ph28p5_gr1800(dets = [sclr, ring_curr]):

    print('\n\n WARNING WARNING WARNING:\n\t check if there scalar is installed or not!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t this assumes epu interpolation table is DISABLED!!!!')
    yield from gcdiag.diode

    # srs settings for diode =  SRS settings:  5  x1  uA/v
    # Current gap limit is 18mm
 
    yield from mv(epu1.phase, 28.5)
    #yield from mv(feslt.hg,2.0)
    #yield from mv(feslt.vg,2.0)
    #yield from bp.mv(pgm.cff,5.2707)

    yield from mv(pgm.en,350)
    yield from sleep(5)
    yield from mv(epu1.gap,18.01)
    yield from sleep(10)
    yield from rel_scan(dets, epu1.gap,0,2,31)
    yield from mv(epu1.gap, 18.01)
    yield from sleep(10)
    yield from rel_scan(dets, epu1.gap,0,1,51)
    
    for i in range(400,451,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,3,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0] -1)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,101)
    for i in range(500,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-2-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,3,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0] -1)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,101)

    yield from sleep(30)
    #800-1550 eV, 3rd harmonic
    for i in range(1100,2001,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-8.5-(i-1000)*0.0027)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0]-0.5)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,1.0,76)

    calc_gap=e2g(850)
    yield from mv(pgm.en,850)
    yield from sleep(5)
    yield from mv(epu1.gap,28.01)
    yield from mv(shutterb,'close') 
    print('\n\n WARNING WARNING WARNING:\n\t EPU Table/Interpolation disabled!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t M1 Feedback disabled!!!!')



def epu_calib_ph28p5_gr1800_v2(dets = [sclr, ring_curr]):

    print('\n\n WARNING WARNING WARNING:\n\t check if there scalar is installed or not!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t this assumes epu interpolation table is DISABLED!!!!')
    yield from gcdiag.diode

    # srs settings for diode =  SRS settings:  5  x1  uA/v
    # Current gap limit is 18mm
 
    yield from mv(epu1.phase, 28.5)
    #yield from mv(feslt.hg,2.0)
    #yield from mv(feslt.vg,2.0)
    #yield from bp.mv(pgm.cff,5.2707)

    yield from sleep(30)
    #800-1550 eV, 3rd harmonic
    for i in range(1100,2001,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i)
        yield from sleep(5)
        yield from mv(epu1.gap,calc_gap-8.5-(i-1000)*0.0027)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,2,31)
        yield from mv(epu1.gap, peaks['max']['sclr_channels_chan2'][0]-0.5)
        yield from sleep(10)
        yield from rel_scan(dets, epu1.gap,0,1.0,76)

    calc_gap=e2g(850)
    yield from mv(pgm.en,850)
    yield from sleep(5)
    yield from mv(epu1.gap,28.01)
    yield from mv(shutterb,'close') 
    print('\n\n WARNING WARNING WARNING:\n\t EPU Table/Interpolation disabled!!!!')
    print('\n\n WARNING WARNING WARNING:\n\t M1 Feedback disabled!!!!')
    

    

