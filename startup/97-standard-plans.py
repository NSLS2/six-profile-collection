def pol_V(offset=None):
    cur_mono_e = pgm.en.user_readback.value
    yield from mv(epu1.table,3)
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,28.5)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    print('\nFinished moving the polarization to vertical.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))

def pol_H(offset=None):
    cur_mono_e = pgm.en.user_readback.value
    yield from mv(epu1.table,1)
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,0)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    print('\nFinished moving the polarization to horizontal.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))


def m3_check():
    sclr_enable()
    if pzshutter.value == 0:
       print('Piezo Shutter is disabled')
       flag = 0
    if pzshutter.value == 2:
       print('Piezo Shutter is enabled: going to be disabled')
       yield from pzshutter_disable()
       flag = 1

    temp_extslt_vg=extslt.vg.user_readback.value
    temp_extslt_hg=extslt.hg.user_readback.value
    temp_gcdiag = gcdiag.y.user_readback.value
    yield from mv(qem07.averaging_time, 1)
    yield from mv(extslt.hg,10)
    yield from mv(extslt.vg,30)
    #yield from gcdiag.grid
    #yield from rel_scan([qem07],m3.pit,-0.0005,0.0005,31, md = {'reason':'checking m3 before cff'})
    yield from rel_scan([sclr],m3.pit,-0.0005,0.0005,31, md = {'reason':'checking m3 before cff'})
    #yield from mv(m3.pit,peaks['cen']['gc_diag_grid'])
    yield from mv(m3.pit,peaks['cen']['sclr_channels_chan8'])
    yield from mv(extslt.hg,temp_extslt_hg)
    yield from mv(extslt.vg,temp_extslt_vg)
    yield from mv(gcdiag.y,temp_gcdiag)

    if flag == 0:
       print('Piezo Shutter remains disabled')   
    if flag == 1:
       print('Piezo Shutter is going to renabled')
       yield from pzshutter_enable()  

def m1_align_fine2():

    m1x_init=m1.x.user_readback.value
    m1pit_init=m1.pit.user_readback.value
    m1pit_step=50
    m1pit_start=m1pit_init-1*m1pit_step
    
    for i in range(0,5):
        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
        yield from scan([qem05],m1.x,-3,3.8,35)
    yield from mv(m1.pit,m1pit_init)

def alignM3x():
    # get the exit slit positions to return to at the end
    vg_init = extslt.vg.user_setpoint.value
    hg_init = extslt.hg.user_setpoint.value
    hc_init = extslt.hc.user_setpoint.value
    print('Saving exit slit positions for later')
    
    # get things out of the way
    yield from m3diag.out
    # read gas cell diode
    yield from gcdiag.grid

    # set detector e.g. gas cell diagnostics qem
    detList=[qem07] #[sclr] 
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 30)
    # open H slit full open
    yield from mv(extslt.hg, 9000)

    #move extslt.hs appropriately and scan m3.x
    yield from mv(extslt.hc,-9)
    yield from relative_scan(detList,m3.x,-6,6,61)

    yield from mv(extslt.hc,-3)
    yield from relative_scan(detList,m3.x,-6,6,61)

    yield from mv(extslt.hc,3)
    yield from relative_scan(detList,m3.x,-6,6,61)
    
    print('Returning exit slit positions to the inital values')
    yield from mv(extslt.hc,hc_init)
    yield from mv(extslt.vg, vg_init, extslt.hg, hg_init)

def beamline_align():
    yield from mv(m1_fbk,0)
    
    yield from align.m1pit
    yield from sleep(5)
    yield from m3_check()
    
    #yield from mv(m1_fbk_cam_time,0.002)
    #yield from mv(m1_fbk_th,1500)
    yield from sleep(5)
    yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.value)
    yield from mv(m1_fbk,1)


def xas(dets,motor,start_en,stop_en,num_points):

    sclr_enable()

    if pzshutter.value == 0:
       print('Piezo Shutter is disabled')
       flag = 0
    if pzshutter.value == 2:
       print('Piezo Shutter is enabled: going to be disabled')
       yield from pzshutter_disable()
       flag = 1

    yield from scan(dets,pgm.en,start_en,stop_en,num_points)
    E_max = peaks['max']['sclr_channels_chan2'][0] 

    if flag == 0:
       print('Piezo Shutter remains disabled')   
    if flag == 1:
       print('Piezo Shutter is going to renabled')
       yield from pzshutter_enable()  
    return E_max

def get_threshold(Ei = pgm.en.user_readback.value):
    '''Calculate the minimum and maximum threshold for RIXSCAM single photon counting (LS mode) 
    Ei\t:\t float -  incident energy (defualt is beamline current energy)
    '''
    t_min = 0.7987 * Ei - 97.964
    t_max = 1.4907 * Ei + 38.249
    print('\n\n\tMinimum value for RIXSCAM threshold (LS mode):\t{}'.format(t_min))
    print('\tMaximum value for RIXSCAM threshold (LS mode):\t{}'.format(t_max))
    
    return t_min, t_max
#TODO make official
m1_fbk = EpicsSignal('XF:02IDA-OP{FBck}Sts:FB-Sel', name = 'm1_fbk')
m1_fbk_sp = EpicsSignal('XF:02IDA-OP{FBck}PID-SP', name = 'm1_fbk_sp')
m1_fbk_th = extslt_cam.stats1.centroid_threshold
#m1_fbk_pix_x = extslt_cam.stats1.centroid.x.value
m1_fbk_cam_time = extslt_cam.cam.acquire_time

#(mv(m1_fbk_th,1500)

