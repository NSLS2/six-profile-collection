#sd.baseline = [ring_curr, gcpress,
#epu1.gap, epu1.phase, 
#feslt.hc, feslt.vc, feslt.hg, feslt.vg, 
#m1.x, m1.pit, m1.rol, 
#pgm.cff, pgm.en, pgm.grx, pgm.m2pit, pgm.grpit, pgm.grlines, 
#m3slt.hs, m3slt.ha, m3slt.vs, m3slt.va,
#m3diag,
#m3.x, m3.y, m3.z, m3.yaw, m3.pit, m3.rol,
#extslt.hg, extslt.vg, extslt.hc, 
#gcdiag, 
#m4_diag1,
#m4slt.inb, m4slt.out, m4slt.bot, m4slt.top, 
#m4.x, m4.y, m4.z, m4.yaw, m4.pit, m4.rol,
#cryo.x, cryo.y, cryo.z, cryo.t, 
#ow,
#m5.x, m5.y, m5.z, m5.yaw, m5.pit, m5.rol,
#m5mask, m6_msk,
#m6.pit, m6.z,
#espgm.cff, espgm.en, espgm.m7pit, espgm.grpit, espgm.grxrb, espgmmask, #espgm.grx,
#oc.y, oc.z, oc.roll, oc.twoth,
#dcslt.inb,dcslt.out,dcslt.bot,dcslt.top,
#dc.z, dc.twoth]


sd.baseline = [ring_curr, gcpress,
epu1, 
feslt, 
m1, 
pgm,
m3slt,
m3diag,
m3,
extslt,
gcdiag, 
m4_diag1,
m4slt, 
m4,
cryo,
stemp, #this just puts in the setpoint readback
ow,
m5,
m5mask, m6_msk,
m6,
espgm.cff, espgm.en, espgm.m7pit, espgm.grpit, espgm.grxrb, espgmmask, #espgm.grx
oc,
dcslt,
dc]


# To avoid baseline are printed on screen:
# bec.disable_baseline()%

def get_threshold(Ei = pgm.en.user_readback.value):
    '''Calculate the minimum and maximum threshold for RIXSCAM single photon counting (LS mode) 
    Ei\t:\t float -  incident energy (defualt is beamline current energy)
    '''
    t_min = 0.7987 * Ei - 97.964
    t_max = 1.4907 * Ei + 38.249
    print('\n\n\tMinimum value for RIXSCAM threshold (LS mode):\t{}'.format(t_min))
    print('\tMaximum value for RIXSCAM threshold (LS mode):\t{}'.format(t_max))
    
    return t_min, t_max
