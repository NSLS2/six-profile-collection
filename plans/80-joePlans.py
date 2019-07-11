
def pivotBeamAboutM3_a(M4_deltaX_mm):
    # pivot the beam about M3 while maintaining the same angle of incidence on M4
    # positions are relative to M3, listed are the nominal positions

    # nominal starting positions
    # distances in mm, angles in rad

    # M3 position
    M3_x = 0
    M3_z = 0
    # exit slit
    Xslit_x = 0
    Xslit_z = 8002
    # M4 slits position
    M4slit_x = 0
    M4slit_z = 13602
    # M4 position
    M4_pitch0 = np.radians(1.5) # nominal pitch
    M4_x = 0+M4_deltaX_mm
    M4_z = 14002
    # focus position
    foc_x = -1000*np.sin(2*M4_pitch0)
    foc_z = 14002+1000*np.cos(2*M4_pitch0)

    M3_deltaP = 0.5*M4_deltaX_mm/(M4_z-M3_z)
    Xslit_delX = 2*M3_deltaP*(Xslit_z-M3_z)
    M4slit_delX = 2*M3_deltaP*(M4slit_z-M3_z)
    #
    asq = (M4_x-M3_x)**2 + (M4_z-M3_z)**2
    bsq = (M4_x-foc_x)**2 + (M4_z-foc_z)**2
    csq = (foc_x-M3_x)**2 + (foc_z-M3_z)**2
    cosTheta = (asq+bsq-csq)/(2*np.sqrt(asq)*np.sqrt(bsq))
    M4_deltaP = 2*M3_deltaP    

    string1 = 'M4 delta pitch = {:.7f} deg, {:.1f} urad'.format(np.degrees(M4_deltaP),M4_deltaP*1e6)
    string2 = 'M4 delta X = {:.4} mm'.format(M4_deltaX_mm)
    string3 = 'M4 slit delta X = {:.4} mm'.format(M4slit_delX)
    string4 = 'Exit slit delta X = {:.4} mm'.format(Xslit_delX)
    string5 = 'M3 delta pitch = {:.7f} deg, {:.1f} urad'.format(np.degrees(M3_deltaP),M3_deltaP*1e6)
    print(string1)
    print(string2)
    print(string3)
    print(string4)
    print(string5)



def pivotBeamAboutM3_b(M4_deltaX_mm):
    # pivot the beam about M3 maintaining a fixed position at the sample
    # positions are relative to M3, listed are the nominal positions

    # nominal starting positions
    # distances in mm, angles in rad

    # M3 position
    M3_x = 0
    M3_z = 0
    # exit slit
    Xslit_x = 0
    Xslit_z = 8002
    # M4 slits position
    M4slit_x = 0
    M4slit_z = 13602
    # M4 position
    M4_pitch0 = np.radians(1.5) # nominal pitch
    M4_x = 0+M4_deltaX_mm
    M4_z = 14002
    # focus position
    foc_x = -1000*np.sin(2*M4_pitch0)
    foc_z = 14002+1000*np.cos(2*M4_pitch0)

    M3_deltaP = 0.5*M4_deltaX_mm/(M4_z-M3_z)
    Xslit_delX = 2*M3_deltaP*(Xslit_z-M3_z)
    M4slit_delX = 2*M3_deltaP*(M4slit_z-M3_z)
    #
    asq = (M4_x-M3_x)**2 + (M4_z-M3_z)**2
    bsq = (M4_x-foc_x)**2 + (M4_z-foc_z)**2
    csq = (foc_x-M3_x)**2 + (foc_z-M3_z)**2
    cosTheta = (asq+bsq-csq)/(2*np.sqrt(asq)*np.sqrt(bsq))
    M4_pitch = 0.5*(np.pi-np.arccos(cosTheta))
    M4_deltaP = M4_pitch0-M4_pitch

    string1 = 'M4 delta pitch = {:.7f} deg, {:.1f} urad'.format(np.degrees(M4_deltaP),M4_deltaP*1e6)
    string2 = 'M4 delta X = {:.4} mm'.format(M4_deltaX_mm)
    string3 = 'M4 slit delta X = {:.4} mm'.format(M4slit_delX)
    string4 = 'Exit slit delta X = {:.4} mm'.format(Xslit_delX)
    string5 = 'M3 delta pitch = {:.7f} deg, {:.1f} urad'.format(np.degrees(M3_deltaP),M3_deltaP*1e6)
    print(string1)
    print(string2)
    print(string3)
    print(string4)
    print(string5)


def monoOrdersScan1():
    # read gas cell photodiode
    yield from gcd_diode()
    yield from sleep(120)

    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 50)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[2], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i, pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[1], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i)
        yield from mv(pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[-1], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i)
        yield from mv(pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[-2], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i)
        yield from mv(pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)

    # read gas cell Au grid
    yield from gcd_grid()
    yield from sleep(120)
    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 10)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[0], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i)
        yield from mv(pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)


def monoOrdersScan2():
    # read gas cell photodiode
    yield from gcd_diode()
    yield from sleep(120)

    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 10)

    GRang, PMang = generatePGMscan(930, 500, startGR=85.0, stopGR=90.0, 
                    startPM=84.0, stopPM=90.0, gridDelta=0.2,
                    fineRange=0.02, fineDelta=0.0005,
                    mm=[0], collAng=4, info=False)

    for i, j in zip(PMang, GRang):
        yield from mv(pgmjoe.m2_pit, i)
        yield from mv(pgmjoe.gr_pit, j)
        yield from relative_scan(detList,pgmjoe.gr_pit,-0.020,0.020,81)


def m3Hfocus():
    # read gas cell photodiode
    yield from gcd_diode()
    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 5)
    # set H exit slit value small
    yield from mv(extslt.hg, 10)

    # change m3.pit, track extslt.hc to be centered, and then take
    # a extslt.hc fine scan

    m3_pit_init = -0.729995
    # m3_z_init = 1.0
    extslt_hc_init = -3.064
    # m3_z_step=5
    extslt_hc_step= -0.5
    m3_pit_step= -0.0017095

    yield from mv(m3.z,1)
    for i in range(11,13):
	# move to starting m3.pit
        yield from mv(m3.pit,m3_pit_init+m3_pit_step*i)
	# move to starting extslt.hc
        yield from mv(extslt.hc,extslt_hc_init+extslt_hc_step*i)
        # yield from sleep(30)
        yield from relative_scan(detList, extslt.hc,-1.0,1.0,400)

def alignM3x():
    # get things out of the way
    yield from m3d_out()
    # read gas cell diode
    yield from gcd_diode()

    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 50)
    # open H slit full open
    yield from mv(extslt.hg, 9000)

    #move extslt.hs appropriately and scan m3.x
    yield from mv(extslt.hc,-9)
    yield from relative_scan(detList,m3.x,-6,6,61)

    yield from mv(extslt.hc,-3)
    yield from relative_scan(detList,m3.x,-6,6,61)

    yield from mv(extslt.hc,3)
    yield from relative_scan(detList,m3.x,-6,6,61)

   
