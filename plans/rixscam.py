def rixscam_acquire_w_shutter(Ei_vals, m7_pit_vals, num_rixs_im, extra_md = ' ' ):
    """
    Parameters
    ----------
    Ei_vals  :  list
        beamline incident energies
    m7_pit_vals  :  list or None
        espgm.m7pit values for each pgm.en value
        if None, m7 pitch is not adjusted
    num_rixs_im  :  integer
        number of RIXS befove every beamline alignment
    pol_type = None, 'H', or 'V'
        polarization H, or V, offset are already assumed and need to be updated
    extra_md = string
        optional, note to be added to rixs light image data
    """
        
    print('Checking m7 now')
    if m7_pit_vals != None:
        print('\tm7 is okay')
        if len(Ei_vals) == len(m7_pit_vals):
           pass
        else:
            print('\n\nInvalid  parameters for incident energy and m7 pitch: \n\tEnergy and pitch list lengths are: {} and {}, repectively.\n'.format(len(Ei_vals), len(m7_pit_vals)))
            raise

      
    print('\n\nStarting plan with {} rixs images for each Ei = {}\n\n'.format(num_rixs_im,Ei_vals))
        
    f_string=''
    md_string = 'no md string yet'
    yield from count([rixscam, sclr, ring_curr], md = {'reason':'dummy'})
    print('Dumnmy')

    for i in range(len(Ei_vals)):
        yield from mv(pgm.en, Ei_vals[i])
        #yield from mvr(cryo.y,-0.005)
        if m7_pit_vals  != None:
            yield from mv(espgm.m7pit, m7_pit_vals[i])
        yield from mv(gvbt1,'open')
        #LIGHTS
        for j in range(0, num_rixs_im):
            #yield from mvr(cryo.y,-0.002)
            print('\t\tTaking RIXS NOW')
            md_string = str(extra_md) + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV' 
            uid = yield from count([rixscam, sclr, ring_curr],num=1, md = {'reason':'{}'. format(md_string)}) 
                
            if uid == None:
                uid = db[-1].start['scan_id']#+1+j+scan_num_cor
                f_string += 'scan no ' + str(db[uid].start['scan_id'])  + ' ' + str(md_string) + '\n'
                print(md_string)
                #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            else:
                f_string += 'scan no ' + str(db[uid].start['scan_id'])  + ' ' + str(md_string) + '\n'
                #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
         
        #DARKS
        yield from mv(gvsc1,'close')
        for i in range(0,2):
            uid = yield from count([rixscam, sclr, ring_curr],num=1, md = {'reason':'gv:sc1 dark'})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
        yield from mv(gvbt1,'close')
        yield from mv(gvsc1,'open')

    print(f_string) 
    print('/n/n EXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))


def rixscam_acquire_w_shutter_count(Ei_vals, m7_pit_vals, num_rixs_im, extra_md = ' ' ):
    """
    Parameters
    ----------
    Ei_vals  :  list
        beamline incident energies
    m7_pit_vals  :  list or None
        espgm.m7pit values for each pgm.en value
        if None, m7 pitch is not adjusted
    num_rixs_im  :  integer
        number of RIXS befove every beamline alignment
    pol_type = None, 'H', or 'V'
        polarization H, or V, offset are already assumed and need to be updated
    extra_md = string
        optional, note to be added to rixs light image data
    """
        
    print('Checking m7 now')
    if m7_pit_vals != None:
        print('\tm7 is okay')
        if len(Ei_vals) == len(m7_pit_vals):
           pass
        else:
            print('\n\nInvalid  parameters for incident energy and m7 pitch: \n\tEnergy and pitch list lengths are: {} and {}, repectively.\n'.format(len(Ei_vals), len(m7_pit_vals)))
            raise

      
    print('\n\nStarting plan with {} rixs images for each Ei = {}\n\n'.format(num_rixs_im,Ei_vals))
        
    f_string=''
    md_string = 'no md string yet'
    yield from count([rixscam, sclr, ring_curr], md = {'reason':'dummy'})
    print('Dumnmy')

    for i in range(len(Ei_vals)):
        yield from mv(pgm.en, Ei_vals[i])
        yield from mvr(cryo.y,-0.005)
        if m7_pit_vals  != None:
            yield from mv(espgm.m7pit, m7_pit_vals[i])
        yield from mv(gvbt1,'open')
        #LIGHTS
        for j in range(0, num_rixs_im):
            #yield from mvr(cryo.y,-0.002)
            print('\t\tTaking RIXS NOW')
            md_string = str(extra_md) + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV' 
            uid = yield from count([rixscam, sclr, ring_curr],num=1, md = {'reason':'{}'. format(md_string)}) 
                
            if uid == None:
                uid = db[-1].start['scan_id']#+1+j+scan_num_cor
                f_string += 'scan no ' + str(db[uid].start['scan_id'])  + ' ' + str(md_string) + '\n'
                print(md_string)
                #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            else:
                f_string += 'scan no ' + str(db[uid].start['scan_id'])  + ' ' + str(md_string) + '\n'
                #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
         
        #DARKS
        yield from mv(gvsc1,'close')
        for i in range(0,2):
            uid = yield from count([rixscam, sclr, ring_curr],num=1, md = {'reason':'gv:sc1 dark'})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
        yield from mv(gvbt1,'close')
        yield from mv(gvsc1,'open')

    print(f_string) 
    print('/n/n EXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))



def rixscam_cff_optimization_centroid(cts, num_scans=1,extra_md = '' ):
    x_motor= pgm.cff

    y_motor= pgm.en
    #y_val=  529.3
    x_ideal= 3.94
    x_start= x_ideal - 0.02 * 10 #0.04#
    x_stop=  x_ideal - 0.02 * 4 #.04#
    number= 7
    yield from mv(gvbt1,'open')
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(number):
        x_val = round (x_start + i * (x_stop - x_start) / (number - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(5)
        yield from mv (x_motor,x_val)
        yield from sleep(15)
        #yield from mv (y_motor,y_val)
        uid = yield from count([rixscam],num=cts, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm.cff = ' + str(x_val) + '\n'

    yield from mv(gvbt1,'close')
    #yield from mv (x_motor,x_ideal)
    print (f_string)

def rixscam_m7_gr_2_axis_centroid(cts, num_scans=1, extra_md = ' '):
    precison_digit = 4
    dets = [ring_curr, rixscam]
    y_motor= espgm.m7pit
    y_ideal = 6.4386
    y_start = y_ideal - 0.004 * 2
    y_stop = y_ideal + 0.004 * 4
    #fine steps 0.004

    x_motor=  espgm.grpit
    x_ideal= 7.6067
    x_start= x_ideal - 0.002 * 2
    x_stop = x_ideal + 0.002 * 4
    #fine steps 0.002
    num = 7
    
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)   
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit)
        yield from sleep(15)      
        yield from mv (x_motor,x_val,y_motor,y_val)
        for s in range(num_scans):
            uid = yield from count(dets, num=cts, md = {'reason':' m7-gr scan {}'. format(extra_md)})        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_val) + \
                        ' , m7_pit = ' + str(y_val) + '\n'

    yield from mv(gvbt1,'close')
    #yield from mv(x_motor, x_ideal, y_motor, y_ideal)
    
    print (f_string) 


def rixscam_exitSlit(cts, num_scans=1, extra_md = ' '):
    #yield from beamline_align_v2()
    dets = [ ring_curr, rixscam, sclr]
    precison_digit = 4
    y_motor= extslt.vg
    y_ideal = 11
    y_start= y_ideal
    y_stop = y_ideal + 5 * 4
    num = 5
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit)      
        yield from mv(y_motor,y_val)
        yield from sleep(20)
        for s in range(num_scans):
            uid = yield from count(dets, num=cts, md = {'reason':' exit-slit scan {}'. format(extra_md)})        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': exit slit = ' + str(y_val) + '\n'

    yield from mv(gvbt1,'close')

    #yield from mv(x_motor, x_ideal, y_motor, y_ideal)
    
    
    print (f_string)



def rixscam_m6_m7_2_axis_centroid(cts, num_scans=1, extra_md = ' '):
    #yield from beamline_align_v2()
    dets = [ ring_curr, rixscam, sclr]
    precison_digit = 4
    y_motor= m6.pit
    y_ideal = 1.4275
    y_start= y_ideal - 0.00025* 3
    y_stop = y_ideal + 0.00025 *3
    # fine step is 0.0005
	#CHANGED STEP TO 0.001 and 4 on each side

    x_motor=  espgm.m7pit
    x_ideal= 6.4386
    x_start= x_ideal - 0.00025 * 3
    x_stop = x_ideal + 0.00025 * 3
    num = 7
    
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)   
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit)      
        yield from mv(x_motor,x_val,y_motor,y_val)
        yield from sleep(20)
        for s in range(num_scans):
            uid = yield from count(dets, num=cts, md = {'reason':' m7-gr scan {}'. format(extra_md)})        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m7_pit = ' + str(x_val) + \
                        ' , m6_pit = ' + str(y_val) + '\n'

    yield from mv(gvbt1,'close')

    #yield from mv(x_motor, x_ideal, y_motor, y_ideal)
    
    
    print (f_string)

def rixscam_dc_optimization_centroid(cts, num_scans=1, extra_md = '' ):
    dets = [ ring_curr, rixscam, sclr]
    x_motor= dc.z
    x_ideal= 241.5
    step=2.5
    x_start = x_ideal - 11 * step 
    x_stop =  x_ideal - 5 * step 
    number = 7
    yield from mv(gvbt1,'open')
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(number):
        x_val = round (x_start + i * (x_stop - x_start) / (number - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(30)
        uid = yield from count(dets,num=cts, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc_z = ' + str(x_val) + '\n'


    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_pgm_en_centroid(cts, num_scans=1, extra_md = '' ):
    """
    Looks like 20um extslt_vg is typical. 
    """

    x_motor=pgm.en
    x_start = 524
    x_stop =  532
    num = 9

    extslt_vg_value = np.round(extslt.vg.user_readback.value,0)	
    
    yield from mv(gvbt1,'open')
    f_string=''

    for i in range(num):
        yield from sleep(5)
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 2)        
        yield from mv (x_motor,x_val)
        uid = yield from count([rixscam], num=cts, md = {'reason':'{} energy calibration - {}um vg'.format(extra_md, extslt_vg_value)})            
        #uid = yield from count([rixscam],num=1, md = {'reason':'{} energy calibration - {}um vg'.format(extra_md, extslt_vg_value)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm_en = ' + str(x_val) + '\n'
   
    yield from mv(gvbt1,'close')
    print (f_string)

def rixscam_extslit_centroid(cts, num_scans=1, extra_md = '' ):
    """
    Looks like 20um extslt_vg is typical.
    """

    x_motor=extslt.vg
    x_start = 11
    vgs = [11, 15, 20]

    extslt_vg_value = np.round(extslt.vg.user_readback.value,0)	
    
    yield from mv(gvbt1,'open')
    f_string=''

    for i in vgs:
        yield from sleep(5)
                
        yield from mv (x_motor,i)
        uid = yield from count([rixscam], num=cts, md = {'reason':'{} resolution - {}um vg'.format(extra_md, extslt_vg_value)})          
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': extslit_vg = ' + str(i) + '\n'
   
    yield from mv(gvbt1,'close')
    print (f_string)

def rixscam_spectro_angles_dc_centroid(cts, num_scans = 1, extra_md = ' '):
    dets = [ring_curr, rixscam, sclr]

    dc_positions = list(range( 398, 398-50, 50))
    #yield from mv(gvbt1,'open')
    
    for d in dc_positions:
        yield from mv(dc.z, d)
        yield from bps.sleep(5)
        yield from rixscam_m6_m7_2_axis_centroid(cts, extra_md = np.str(extra_md+' at dc '+ np.str(d)))
        yield from rixscam_m7_gr_2_axis_centroid(cts, extra_md =  np.str(extra_md+' at dc '+ np.str(d)))


def rixscam_m5_roll_optimization_centroid(cts, num_scans=1,extra_md = '' ):
    x_motor= m5.rol
    x_ideal=-1000
    x_start= x_ideal -500*2#0.04#
    x_stop=  x_ideal +500*4#.04#
    number= 7  #5 #12
    yield from mv(gvbt1,'open')
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(number):
        x_val = round (x_start + i * (x_stop - x_start) / (number - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(10)
        uid = yield from count([rixscam],num=cts, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm.cff = ' + str(x_val) + '\n'


    yield from mv(gvbt1,'close')
    #yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_m6_mask_study_centroid(cts, num_scans=1,extra_md = '' ):
    x_motor= m6_msk
    x_ideal=60
    x_start= x_ideal
    x_stop=  x_ideal-1*5 #.04#
    number= 6
    yield from mv(gvbt1,'open')
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(number):
        x_val = round (x_start + i * (x_stop - x_start) / (number - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(10)
        uid = yield from count([rixscam],num=cts, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_mask = ' + str(x_val) + '\n'


    yield from mv(gvbt1,'close')
    #yield from mv (x_motor,x_ideal)
    print (f_string)

fails = []
def stubborn_test(num_input):
    import time
    fails.clear()
    for j in range (12):
        print(f"on loop {j}")
        try:
            yield from count([rixscam,sclr],num=num_input, md = {'reason': 'coso 38 K'})
            yield from bps.checkpoint()
        except TimeoutError:
            print('*'*50)
            print(f"HAD AT TIMEOUT on loop {j}")
            print('*'*50)
            yield from bps.checkpoint()
            yield from bps.sleep(300)
            yield from bps.unstage(rixscam)
            fails.append((j, time.ctime()))
            continue
    return fails





from epics import caget 
rixscam_vog_s1 = EpicsSignalRO('XF:02ID1-ES{RIXSCam}:cam1:VOLT_BIAS_OG_1',name='rixscam_vog_s1')
rixscam_vdc_s1 = EpicsSignalRO('XF:02ID1-ES{RIXSCam}:cam1:VOLT_BIAS_HVDC_1',name='rixscam_vdc_s1')
rixscam_vog_s2 = EpicsSignalRO('XF:02ID1-ES{RIXSCam}:cam1:VOLT_BIAS_OG_2',name='rixscam_vog_s2')
rixscam_vdc_s2 = EpicsSignalRO('XF:02ID1-ES{RIXSCam}:cam1:VOLT_BIAS_HVDC_2',name='rixscam_vdc_s2')
rixscam_temp = EpicsSignalRO('XF:02ID1-ES{RIXSCam}:cam1:TemperatureActual',name='rixscam_temp')

tilt_3AA_xz = EpicsSignalRO('XF:02IDD-ES{3AA:1-TiltM:1}Axis:X-I',name='tilt_3AA_xz')
tilt_3AA_yx = EpicsSignalRO('XF:02IDD-ES{3AA:1-TiltM:1}Axis:Y-I',name='tilt_3AA_yx')

tilt_DAA_xz = EpicsSignalRO('XF:02IDD-ES{DAA:1-TiltM:2}Axis:X-I',name='tilt_DAA_xz')
tilt_DAA_yx = EpicsSignalRO('XF:02IDD-ES{DAA:1-TiltM:2}Axis:Y-I',name='tilt_DAA_yx')

def test_rixscam_voltages(cts, num_scans=1):
    yield from mv(gvbt1,'open')
    for i in range(num_scans):
        yield from count([rixscam,rixscam_vdc_s1,rixscam_vog_s1,rixscam_vdc_s2, rixscam_vog_s2, rixscam_temp],num=cts)
    yield from mv(gvbt1,'close')

