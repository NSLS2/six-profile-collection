import uuid
from ophyd import Device, EpicsMotor, EpicsSignal

epu_table_mode = EpicsSignal('XF:02ID-ID{EPU:1}Enbl:Mode-Sel', name='epu_table_mode')

def pol_V(offset=None):
    yield from mv(m1_simple_fbk,0)
    yield from mv(m1_pid_fbk,'OFF')
    yield from mv(m3_pid_fbk,'OFF')
    cur_mono_e = (yield from bps.rd(pgm.en.user_readback))
    yield from mv(epu1.table,6) # 4 = 3rd harmonic; 6 = "testing V" 1st harmonic
    yield from mv(epu_table_mode,'Enable')
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,28.5)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    yield from mv(m1_pid_fbk,'ON')
    yield from mv(m3_pid_fbk,'ON')
    print('\nFinished moving the polarization to vertical.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))

def pol_H(offset=None):
    yield from mv(m1_simple_fbk,0)
    yield from mv(m1_pid_fbk,'OFF')
    yield from mv(m3_pid_fbk,'OFF')
    cur_mono_e = (yield from bps.rd(pgm.en.user_readback))
    yield from mv(epu1.table,5) # 2 = 3rd harmonic; 5 = "testing H" 1st harmonic
    yield from mv(epu_table_mode,'Enable')
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,0)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    yield from mv(m1_pid_fbk,'ON')
    yield from mv(m3_pid_fbk,'ON')
    print('\nFinished moving the polarization to horizontal.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))

###########################################
epu_forw_int_mode_input = EpicsSignal('XF:02ID-ID{EPU:1-FLT}Enbl:Inp1-Sel', name = 'epu_forw_int_mode_input')
epu_forw_int_mode_output = EpicsSignal('XF:02ID-ID{EPU:1-FLT}Enbl:Out1-Sel', name = 'epu_forw_int_mode_output')
epu_rev_int_mode_input = EpicsSignal('XF:02ID-ID{EPU:1-RLT}Enbl:Inp1-Sel', name = 'epu_rev_int_mode_input')

def epu_control_disable():
    '''The function disables the EPU control so that the PGM and the EPU can be operated fully independetly. This function doesn't require any parameter.'''
    yield from mv(m1_pid_fbk,'OFF')
    yield from mv(m3_pid_fbk,'OFF')
    print(' The EPU table and control with the PGM energy are going to be disabled....')
    yield from mv(epu_table_mode,'Disable')
    yield from mv(epu_forw_int_mode_input, 0)
    yield from mv(epu_forw_int_mode_output, 0)
    yield from mv(epu_rev_int_mode_input, 0)
    yield from sleep(2)
    print(' The EPU table and control is now disabled.')
    print(' The M1 and M3 PID Feedback systems are switched OFF ' )

def epu_control_enable(pol):
    '''The function can enable the EPU control either for Linear Horizontal or Linear Vertical polarization. The function accepts the polarization as input parameter: use 0 for Linear Horizontal or 28.5 for Linear Vertical.'''
    print(' The EPU control with the PGM energy is going to be enabled....')

    yield from mv(m1_pid_fbk,'OFF')
    yield from mv(m3_pid_fbk,'OFF')

    yield from mv(epu_forw_int_mode_input, 1)
    yield from mv(epu_forw_int_mode_output, 1)
    yield from mv(epu_rev_int_mode_input, 1)
    yield from sleep(2)
    cur_mono_e = pgm.en.user_readback.get()
    if pol == 'H':
       yield from mv(epu1.table,5) # 2 = 3rd harmonic; 5 = "testing H" 1st harmonic
       yield from mv(epu_table_mode,'Enable')
       yield from mv(epu1.phase,0)
       yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
       yield from mv(pgm.en,cur_mono_e)

    if pol == 'V':
       yield from mv(epu1.table,6) # 2 = 3rd harmonic; 5 = "testing H" 1st harmonic
       yield from mv(epu_table_mode,'Enable')
       yield from mv(epu1.phase,28.5)
       yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
       yield from mv(pgm.en,cur_mono_e)

    else:
       print('ERROR: Polarization not correctly selected. Please define the desired polarization as a function argument, either V or H within quotes')

    print(' The EPU Table and the control with the PGM energy is now enabled for E=:\t{}'.format(cur_mono_e))
    print(' ATTENTION 1: You need to run a beamline alignment routine now.')
    print(' ATTENTION 2: Please, make sure the offset for your EPU table is correct. The current one is: \t{}'.format(epu1.offset.get()))


def m3_check():
    yield from mv(m3_simple_fbk,0)
    yield from mv(m3_pid_fbk,'OFF')
    sclr_enable()
    if (yield from bps.rd(pzshutter)) == 0:
       print('Piezo Shutter is disabled')
       flag = 0
    if (yield from bps.rd(pzshutter)) == 2:
       print('Piezo Shutter is enabled: going to be disabled')
       yield from pzshutter_disable()
       flag = 1

    temp_extslt_vg = (yield from bps.rd(extslt.vg.user_readback))
    temp_extslt_hg = (yield from bps.rd(extslt.hg.user_readback))
    temp_gcdiag = (yield from bps.rd(gcdiag.y.user_readback))
    #yield from mv(qem07.averaging_time, 1)
    yield from mv(sclr.preset_time, 1)
    yield from mv(extslt.hg,10)
    yield from mv(extslt.vg,30)
    #yield from gcdiag.grid # RE-COMMENT THIS LINE 5/7/2019
    #yield from rel_scan([qem07],m3.pit,-0.0005,0.0005,31, md = {'reason':'checking m3 before cff'})
    peaks = bluesky.callbacks.fitting.PeakStats(m3.pit.name, 'sclr_channels_chan8') # Good for Normal Operation
    # peaks = bluesky.callbacks.fitting.PeakStats(m3.pit.name, 'sclr_channels_chan2')  #Goof for Gas Cell
    yield from bpp.subs_wrapper(rel_scan([sclr],m3.pit,-0.0005,0.0005,31, md = {'reason':'checking m3'}), peaks)
    print(f'!!! m3_check: peaks["cen"]: {peaks["cen"]}')
    if peaks['cen'] is not None:
        yield from mv(m3.pit, peaks['cen'])
    else:
        yield from mv(extslt.hg,temp_extslt_hg)
        yield from mv(extslt.vg,temp_extslt_vg)
        peaks_not_found()  # raises an exception!

    yield from mv(extslt.hg,temp_extslt_hg)
    yield from mv(extslt.vg,temp_extslt_vg)
    yield from mv(gcdiag.y,temp_gcdiag)
    yield from sleep(60)
    #yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.get())
    #yield from mv(m3_pid_target,extslt_cam.stats1.centroid.x.get())#m3_simple_fbk_cen.get())
    yield from mv(m3_pid_target, m3_pid_cen.get())
    yield from mv(m3_pid_fbk,'ON')
    if flag == 0:
       print('Piezo Shutter remains disabled')   
    if flag == 1:
       print('Piezo Shutter is going to renabled')
       yield from pzshutter_enable()


def m1_align_fine2():

    m1x_init = (yield from bps.rd(m1.x.user_readback))
    m1pit_init = (yield from bps.rd(m1.pit.user_readback))
    m1pit_step=50
    m1pit_start=m1pit_init-1*m1pit_step
    
    for i in range(0,5):
        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
        yield from scan([qem05],m1.x,-3,3.8,35)
    yield from mv(m1.pit,m1pit_init)
    yield from mv(m1.x,m1x_init)

def alignM3x():
    # get the exit slit positions to return to at the end
    vg_init = (yield from bps.rd(extslt.vg.user_setpoint))
    hg_init = (yield from bps.rd(extslt.hg.user_setpoint))
    hc_init = (yield from bps.rd(extslt.hc.user_setpoint))
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
    yield from mv(m1_fbk_sp,extslt_cam.stats1.centroid.x.get())
    yield from mv(m1_fbk,1)


def beamline_align_v2():
    yield from mv(m1_simple_fbk,0)
    yield from mv(m3_simple_fbk,0)
    yield from mv(m1_fbk,0)

    # Comes from 43-alignment_scans.py:
    # @property
    # def m1pit(self):
    #     .........``...
    yield from align.m1pit
    yield from sleep(5)
    yield from mv(m1_simple_fbk_target_ratio,m1_simple_fbk_ratio.get())
    yield from mv(m1_simple_fbk,1)

    yield from sleep(5)
    yield from m3_check()


def beamline_align_v2_for_suspenders():
    # We create a unique run name in case
    # multiple suspenders are tripped at the same time.
    run_name = f'alignment-{str(uuid.uuid4())[:8]}'
    yield from bpp.set_run_key_wrapper(beamline_align_v2(), run=run_name)

def beamline_align_v3_for_suspenders():
    # We create a unique run name in case
    # multiple suspenders are tripped at the same time.
    run_name = f'alignment-{str(uuid.uuid4())[:8]}'
    yield from bpp.set_run_key_wrapper(beamline_align_v3(), run=run_name)

#@bpp.set_run_key_decorator('alignment')
def beamline_align_v3():
    yield from mv(m1_simple_fbk,0)
    yield from mv(m3_simple_fbk,0)
    yield from mv(m1_pid_fbk,'OFF')
    yield from mv(m3_pid_fbk,'OFF')
    yield from mv(m1_fbk,0)

    # Comes from 43-alignment_scans.py:
    # @property
    # def m1pit(self):
    #     ............
    yield from align.m1pit
    yield from sleep(5)
    #yield from mv(m1_pid_target_ratio,m1_pid_ratio.get())
    yield from mv(m1_pid_target_ratio,1) #Changed on 1/25/21: if m3slits are centered on the ROI, this should work better.
    yield from sleep(5)
    yield from count([m3diag.cam])
    yield from m3diag.out

    yield from mv(m1_pid_fbk,'ON')

    yield from sleep(5)
    yield from m3_check()


def xas_old(dets,motor,start_en,stop_en,num_points,sec_per_point):

    sclr_enable()
    sclr_set_time = (yield from bps.rd(sclr.preset_time))

    if (yield from bps.rd(pzshutter)) == 0:
       print('Piezo Shutter is disabled')
       flag = 0
    if (yield from bps.rd(pzshutter)) == 2:
       print('Piezo Shutter is enabled: going to be disabled')
       yield from pzshutter_disable()
       flag = 1
    yield from mv(sclr.preset_time,sec_per_point)
    if dets[0].name == 'rixscam':
        det_field = 'rixscam_xip_count_possible_event'
    else:
        det_field = 'sclr_channels_chan2'

    peaks = bluesky.callbacks.fitting.PeakStats(pgm.en.name, det_field)
    yield from bpp.subs_wrapper(scan(dets,pgm.en,start_en,stop_en,num_points), peaks)
    print(f"!!! xas: peaks['max']: {peaks['max']}")
    E_max = peaks['max'][0]
    E_com = peaks['com']

    if flag == 0:
       print('Piezo Shutter remains disabled')   
    if flag == 1:
       print('Piezo Shutter is going to renabled')
       yield from pzshutter_enable()
    yield from mv(sclr.preset_time,sclr_set_time)
    return E_com, E_max

def xas(dets,motor,start_en,stop_en,num_points,sec_per_point):

    sclr_enable()
    sclr_set_time_original = (yield from bps.rd(sclr.preset_time))

    if (yield from bps.rd(pzshutter)) == 0:
       print('Piezo Shutter is disabled')
       flag = 0
    if (yield from bps.rd(pzshutter)) == 2:
       print('Piezo Shutter is enabled: going to be disabled')
       yield from pzshutter_disable()
       flag = 1
    yield from mv(sclr.preset_time,sec_per_point)
    if dets[0].name == 'rixscam':
        det_field = 'rixscam_xip_count_possible_event'
    else:
        det_field = 'sclr_channels_chan2'

    ####################################################################
    dets_name = list([])
    for i in dets:
        dets_name.append(i.name)
    if 'rixscam' in dets_name:
        rixscam_set_time_original = rixscam.cam.acquire_time.get()
        yield from mv(rixscam.cam.acquire_time, sec_per_point)
    ####################################################################
    peaks = bluesky.callbacks.fitting.PeakStats(pgm.en.name, det_field)
    yield from bpp.subs_wrapper(scan(dets,pgm.en,start_en,stop_en,num_points), peaks)
    print(f"!!! xas: peaks['max']: {peaks['max']}")
    E_max = peaks['max'][0]
    E_com = peaks['com']

    if flag == 0:
       print('Piezo Shutter remains disabled')   
    if flag == 1:
       print('Piezo Shutter is going to renabled')
       yield from pzshutter_enable()
    yield from sleep(5)
    yield from mv(sclr.preset_time,sclr_set_time_original)
    if 'rixscam' in dets_name:
        yield from mv(rixscam.cam.acquire_time,rixscam_set_time_original)
	
    return E_com, E_max


#TODO put this inside of rixscam
def rixscam_get_threshold(Ei = None):
    '''Calculate the minimum and maximum threshold for RIXSCAM single photon counting (LS mode) 
    Ei\t:\t float -  incident energy (default is beamline current energy)
    '''
    if Ei is None:
        Ei = (yield from bps.rd(pgm.en.user_readback))
    t_min = 0.7987 * Ei - 97.964
    t_max = 1.4907 * Ei + 38.249
    print('\n\n\tMinimum value for RIXSCAM threshold (LS mode):\t{}'.format(t_min))
    print('\tMaximum value for RIXSCAM threshold (LS mode):\t{}'.format(t_max))
    print('\tFor Beamline Energy:\t\t\t\t{}'.format(Ei))
    
    return t_min, t_max

#TODO put this insdie of rixscam
def rixscam_set_threshold(Ei=None):
    '''Setup the RIXSCAM.XIP plugin values for a specific energy for single photon counting and
     centroiding in LS mode.  
     Ei\t:\t float -  incident energy (default is beamline current energy)
    '''
    if Ei is None:
        Ei = pgm.en.user_readback.get()
    thold_min, thold_max = yield from rixscam_get_threshold(Ei)
    yield from mv(rixscam.xip.beamline_energy, Ei, 
                  rixscam.xip.sum_3x3_threshold_min, thold_min, 
                  rixscam.xip.sum_3x3_threshold_max, thold_max)

	


#TODO make official so that there is a m1_fbk device like m1fbk.setpoint
m1_fbk = EpicsSignal('XF:02IDA-OP{FBck}Sts:FB-Sel', name = 'm1_fbk')
m1_fbk_sp = EpicsSignal('XF:02IDA-OP{FBck}PID-SP', name = 'm1_fbk_sp')
m1_fbk_th = extslt_cam.stats1.centroid_threshold
#m1_fbk_pix_x = extslt_cam.stats1.centroid.x.get()
m1_fbk_cam_time = extslt_cam.cam.acquire_time

#(mv(m1_fbk_th,1500)
m1_simple_fbk = EpicsSignal('XF:02IDA-OP{M1_simp_feed}FB-Ena', name = 'm1_simple_fbk')
m1_simple_fbk_target_ratio = EpicsSignal('XF:02IDA-OP{M1_simp_feed}FB-TarRat', name = 'm1_simple_fbk_target_ratio')
m1_simple_fbk_ratio = EpicsSignal('XF:02IDA-OP{M1_simp_feed}FB-Ratio', name = 'm1_simple_fbk_ratio')

m3_simple_fbk = EpicsSignal('XF:02IDA-OP{M3_simp_feed}FB-Ena', name = 'm3_simple_fbk')
m3_simple_fbk_target = EpicsSignal('XF:02IDA-OP{M3_simp_feed}FB-Targ', name = 'm3_simple_fbk_target')
m3_simple_fbk_cen = EpicsSignal('XF:02IDA-OP{M3_simp_feed}FB_inpbuf', name = 'm3_simple_fbk_cen')


# Definition signals PID feedback system 02/25/2020
m1_pid_fbk = EpicsSignal('XF:02ID-OP{FBTEST2}Sts:FB-Sel', name = 'm1_pid_fbk')
m1_pid_target_ratio = EpicsSignal('XF:02ID-OP{FBTEST2}PID-SP', name = 'm1_pid_target_ratio')
m1_pid_ratio = EpicsSignal('XF:02ID-OP{FBTEST2}Inp-Sts.A', name = 'm1_pid_ratio')

m3_pid_fbk = EpicsSignal('XF:02ID-OP{FBTEST3}Sts:FB-Sel', name = 'm3_pid_fbk')
m3_pid_target = EpicsSignal('XF:02ID-OP{FBTEST3}PID-SP', name = 'm3_pid_fbk_target')
m3_pid_cen = EpicsSignal('XF:02ID-OP{FBTEST3}Inp-Sts.A', name = 'm3_pid_cen')

