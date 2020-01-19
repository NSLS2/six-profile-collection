#2018/02/24 Gas Cell @ N-edge  

def test_extra_staging(exp_time=10):
     
     yield from rixscam_extra_stage(exp_time)
     yield from mv(rixscam.cam.acquire_time,exp_time)
     yield from count([rixscam], md = {'reason':'fake data'})
     yield from rixscam_extra_unstage()
                                               
     print(rixscam.cam.acquire_time.value,'\n')             
     print('now i should be moving and collecting/cleaning')
     for i in range(exp_time*2):     
         print('moving and cleaning')
         yield from sleep(1)                   
     print(rixscam.cam.acquire_time.value,'\n')
                                              
     yield from rixscam_extra_stage(exp_time)        
     yield from mv(rixscam.cam.acquire_time,exp_time)        
     yield from count([rixscam], md = {'reason':'fake data'})
     yield from rixscam_extra_unstage()
     print(rixscam.cam.acquire_time.value,'\n')  
     print('now i should be moving & cleaning')        
                                                                
     for i in range(int(exp_time*0.5)):                            
         print('moving and cleaning')                         
         yield from sleep(1)                             
                                                
     print('DONE now i should be cleaning, for real now, but lets check with one last scan')
     
     yield from rixscam_extra_stage(exp_time)        
     yield from mv(rixscam.cam.acquire_time,exp_time)        
     yield from count([rixscam], md = {'reason':'fake data'})
     yield from rixscam_extra_unstage()
     print(rixscam.cam.acquire_time.value,'\n')  
     print('now i should be  cleaning')


def rixscam_extra_stage(exp_time):  #this is hear for now so that we know we have a good first image. need more testing.
    yield from mv(rixscam.cam.acquire, 0)
    yield from mv(rixscam.cam.image_mode,'Multiple')
    yield from sleep(1.03+3.5) #for readout
    yield from mv(rixscam.cam.acquire_time, exp_time) #because the camera is always behind by 1
    yield from mv(rixscam.cam.acquire,1) # This takes the place of the dummy image
    yield from sleep(1.03 + 3.5)
    print('\n\tDetector ready to take data.  If you RE.abort, then RE(rixscam_extra_unstage())\n\n')


def rixscam_extra_unstage():  #exp_time not needed if we can monitor the image mode
    print('\tPreparing rixscam for "constant charge cleaning". If this takes a long time, then we know that there is a need for an extra image')
    yield from mv(rixscam.cam.acquire_time,  1)
    yield from sleep(1.03) # if above is put_complete, then we don't need this.
    yield from mv(rixscam.cam.acquire,1)  # because camera is always behind by 1 so we fake a dummy image
    #yield from sleep(3.3+exp_time) # if above is put_complete, then we don't need this.
    while(rixscam.cam.image_mode.value != 2): # maybe this is better than waiting exp_time+3.3 s. (readout time is just under 3 for full image)
    #while(rixscam.cam.acquire.value = 1): # maybe this is better than waiting exp_time+3.3 s. (readout time is just under 3 for full image)
        yield from mv(rixscam.cam.image_mode,'Continuous')
    #    # add overwite statement to tell user what is happening
        yield from sleep(1.03) # should not be needed, but it seems that the rememants of the last exposure time are present, and put_complete is not working appropriately
    yield from mv(rixscam.cam.acquire, 1)
    print('\n\tDetector is "Collecting" in exposure mode {} (2 is continuous) for {} s\n\n'.format(rixscam.cam.image_mode.value,rixscam.cam.acquire_time.value))

def rixscam_multi_image(num_images,extra_md =' ', take_dark = False):
    f_string = ''
    yield from mv(gvbt1,'open')
    yield from count([rixscam],md={'reason':'dummy'})
    
    for i in range(0,num_images):
        uid = yield from count([rixscam],md={'reason':'multi image scan,{} of {}. {}'.format(i+1,num_images,extra_md) })
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  image ' + str(i+1) + ' of ' + str(num_images) + '\n'
    if take_dark is True:
        yield from mv(gvsc1,'close')
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
        yield from mv(gvsc1,'open')
        
    yield from mv(gvbt1,'close')
    print(f_string)

def rixscam_multi_image_best(exp_time, num_images,extra_md =' '):
    yield from mv(gvbt1,'open')
    yield from rixscam_extra_stage(exp_time)

    uid = yield from count([rixscam],md={'reason':'multi image scan, 1 of {}. {}'.format(num_images, extra_md) })
    if uid is not None:
        scan_id = db[uid].start['scan_id']
    else:
         scan_id='not yet run'
    
    for i in range(0,num_images):

        yield from count([rixscam],md={'reason':'multi image scan,{} of {}. {}'.format(i+1,num_images,extra_md) })
    
    yield from mv(gvbt1,'close') 
    yield from rixscam_extra_unstage()  
    

def some_image(dets=[rixscam],exp_time=600,num_ims = 6, sample = 'Multilayer'):
    f_string = ''
    #yield from rixscam_extra_stage(exp_time)
    yield from mv(rixscam.cam.acquire_time, exp_time)
    yield from mv(gvbt1,'open')
    for i in range(num_ims):	
        uid = yield from count(dets,  md = {'reason':'{} {} of {}  100um vg'.format(sample, i, num_ims)})
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + ' 100um vg\n'
    yield from mv(extslt.vg, 50)
    for i in range(num_ims*2):	
        uid = yield from count(dets,  md = {'reason':'{} {} of {}  50um vg'.format(sample, i, num_ims)})
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + ' 50um vg\n'
    #yield from rixscam_extra_unstage()
    yield from mv(gvbt1,'close')
    print(f_string)


def multi_image(dets=[rixscam], num_ims=1, exp_time=1): #qem12#
    try:
        f_string='\n---------Scan Summary---------\n'
    

        sample = 'ndnio3'
        yield from rixscam_extra_stage(exp_time)
        yield from mv(rixscam.cam.acquire_time, exp_time)
        for i in range(num_ims):	
            uid = yield from count(dets,  md = {'reason':'{} {} of {} 100um vg'.format(sample, i, num_ims)})
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + ' 100um vg \n'
    
        yield from rixscam_extra_unstage()
    
        yield from mv(cryo.x, 34, cryo.y, 74,  cryo.z, 42)    
        sample = 'carbon'
    
        yield from rixscam_extra_stage(exp_time)
        yield from mv(rixscam.cam.acquire_time, exp_time)
        for i in range(num_ims):	
            uid = yield from count(dets,  md = {'reason':'{} {} of {}  100um vg'.format(sample, i, num_ims)})
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + ' 100um vg\n'

        yield from rixscam_extra_unstage()    
    
        yield from mv(extslt.vg, 30)
        sample = 'carbon'
    
        yield from rixscam_extra_stage(exp_time)
        yield from mv(rixscam.cam.acquire_time, exp_time)
        for i in range(num_ims):	
            uid = yield from count(dets,  md = {'reason':'{} {} of {}  30um vg'.format(sample, i, num_ims)})
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + '30um vg\n'
        
        yield from rixscam_extra_unstage()
        yield from mv(gvsc1,'close')
        sample = 'SCgv Dark'
        num_ims = 3
        yield from rixscam_extra_stage(exp_time)
        yield from mv(rixscam.cam.acquire_time, exp_time)
        for i in range(num_ims):	
            uid = yield from count(dets,  md = {'reason':'{} {} of {}  '.format(sample, i, num_ims)})
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': sample = ' + str(sample) + '\n'

        yield from rixscam_extra_unstage()
        yield from mv(gvbt1,'close')
        
    
        print(f_string)
        print('\t SAMPLE IS CARBON TAPE \n')
        print('\t check esit slit gap \n')

    except Exception:
        # Catch the exception long enough to clean up.
        yield from mv(gvbt1,'close')
        print('\n\tSomething bad happened.\n')
        print(f_string)
        print('\n\tSomething bad happened.\n')
        yield from rixscam_extra_unstage()
        raise


	
def rixscam_m6_1_axis(  extra_md = ' '):
#according to joe's calcs, 0.5mrad makes a signf change.  this is 0.028 deg in m6
# beyond  +/- 0.25deg it could be very difficult to see something...especially if focusing well.
    x_motor=  m6.pit
    x_ideal=1.42
    x_start= x_ideal + 0.02
    x_stop=  x_ideal - 0.02
    num= 5 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)#,y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_val) + '\n'#\
                   # ' , m7_pit = ' + str(y_val) + '\n'
    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_ideal) + '\n'#\
                    #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')

    print (f_string)

def rixscam_m6_2_axis_zero_order(  extra_md = ' '):
#according to joe's calcs, 0.5mrad makes a signf change.  this is 0.028 deg in m6
# beyond  +/- 0.25deg it could be very difficult to see something...especially if focusing well.
    x_motor=  m6.pit
    x_ideal=1.41
    x_start= x_ideal + 0.02
    x_stop=  x_ideal - 0.02
    num= 5 #12
    
    y_motor= espgm.m7pit
    y_ideal= 5.3615
    y_start = y_ideal + 0.02
    y_stop = y_ideal - 0.02

    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)   
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , 3)      
        yield from mv (x_motor,x_val,y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_val) + '\n'\
                    ' , m7_pit = ' + str(y_val) + '\n'
    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    yield from mv(x_motor,x_ideal,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_ideal) + '\n'\
                    ' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')

    print (f_string)

def rixscam_ow_1_axis(  extra_md = ' '):
# to scan optics wheel to find position for parabolic mirrors
# detector subtends and angle of ~0.1 deg
    x_motor= ow.th
    x_ideal=-30.2918
    x_start= x_ideal + 1.0
    x_stop=  x_ideal - 1.0
    num = 41
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)#,y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': ow_th = ' + str(x_val) + '\n'#\
                   # ' , m7_pit = ' + str(y_val) + '\n'
    yield from mv(gvsc1,'close')
	
    if 0: # dark image
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    if 0: # extra measurement at 'ideal' position
        yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
        yield from mv(gvsc1,'open')
        uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_ideal) + '\n'#\
                    #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')

    print (f_string)


def rixscam_m6_pit_optimization2():
#according to joe's calcs, 0.5mrad makes a signf change.  this is 0.028 deg in m6
# beyond  +/- 0.25deg it could be very difficult to see something...especially if focusing well.
    precison_digit = 4
    gr_pit=round(espgm.grpit.user_readback.value,precison_digit)
    
    extra_md = 'gr = {}'.format(gr_pit)

    #2500 l/mm grating values (wide range)
    #m7_dict={6.17:4.81,6.27:5.075,6.37:5.290,6.47:5.476,6.57:5.652,6.67:5.819}
    #x_motor=m6.pit
    #x_ideal= 1.35  
    #x_start= 1.55
    #x_stop=  1.2 

    #y_motor=espgm.m7pit
    #y_ideal = m7_dict[gr_pit]
    #y_start= y_ideal+8*.025
    #y_stop= y_ideal-6*.025
    #num = 15

    #1250 l/mm grating values (wide range)
    #NOTE : grating:m7
    #m7_dict={4.85:4.256,4.95:4.452,5.05:4.623,5.09:4.683, 5.12:4.806,5.15:4.778, 5.18:4.8205, 5.25: 4.928, 5.35:5.072,5.45:5.207}
    m7_dict={4.9281:4.8445}#6.1385:5.3433,6.3385:5.7303,6.4385:5.9003}
    x_motor=m6.pit
    x_ideal= 1.3777
    x_start= x_ideal+5*.001
    x_stop= x_ideal-5*.001  

    y_motor=espgm.m7pit
    y_ideal = m7_dict[gr_pit]
    y_start= y_ideal+5*.001
    y_stop= y_ideal-5*.001
    num = 11

    yield from mv(gvbt1,'close')
    f_string=''

    yield from count([rixscam])

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)        
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit) 
        yield from mv (x_motor,x_val,y_motor,y_val)
        yield from sleep(10)
        yield from mv(gvbt1,'open')
        uid = yield from count([rixscam],num=1, md = {'reason':'{} m6 first order focus - 20um vg'.format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_val) + \
                    ' , m7_pit = ' + str(y_val) + '\n'
        yield from mv(gvbt1,'close')     


    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    yield from mv(x_motor,x_ideal,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    #uid = yield from count([rixscam],num=1, md = {'reason':'{} ideal position'.format(extra_md)})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_ideal) + \
    #               ' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')

    print (f_string)

def rixscam_m6_pit_optimization2_centroid(num_scan):
#according to joe's calcs, 0.5mrad makes a signf change.  this is 0.028 deg in m6
# beyond  +/- 0.25deg it could be very difficult to see something...especially if focusing well.
    precison_digit = 4
    gr_pit=round(espgm.grpit.user_readback.value,precison_digit)
    
    extra_md = 'gr = {}'.format(gr_pit)

    #NOTE : grating:m7
    m7_dict={6.2476:5.7229}
    x_motor=m6.pit
    x_ideal= 1.3777
    x_start= x_ideal+5*.001
    x_stop= x_ideal-5*.001  

    y_motor=espgm.m7pit
    y_ideal = m7_dict[gr_pit]
    y_start= y_ideal+5*.001
    y_stop= y_ideal-5*.001
    num = 11

    
    f_string=''

    yield from count([rixscam], num=1)
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)        
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit) 
        yield from mv (x_motor,x_val,y_motor,y_val)
        yield from sleep(10)

        for i in range(num_scan):
            uid = yield from count([rixscam],num=1, md = {'reason':'{} m6 first order focus - 20um vg'.format(extra_md)})        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m6_pit = ' + str(x_val) + \
                        ' , m7_pit = ' + str(y_val) + '\n'
    
    yield from mv(gvbt1,'close')

    print (f_string)


def rixscam_gr_m6_pit_optimization2():

    yield from align.m1pit
    yield from m3_check()
    
    gr_list = [5.4945, 5.5945, 5.6945, 5.7945, 5.8945]
    
    for gr in gr_list:
        yield from mv(espgm.grpit, gr)
        yield from rixscam_m6_pit_optimization2()


def rixscam_m7_gr_2_axis(  extra_md = ' '):
    precison_digit = 4
    y_motor= espgm.m7pit
    #y_ideal= 4.8445#5.5349 
    #y_start = 4.7971#4.7813#5.4959
    #y_stop = 4.8919#5.5734
    y_ideal = 5.086414 
    y_start = 5.036414
    y_stop = 5.136414


    x_motor=  espgm.grpit
    #x_ideal= 4.9281#6.2368
    #x_start= 4.8981#4.8881#6.2168
    #x_stop=  4.9581#6.2568
    x_ideal= 5.2939
    x_start= 5.2639
    x_stop = 5.3229
    num= 14 #12
    
    f_string=''

    yield from count([rixscam,sclr], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)   
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit)      
        yield from mv (x_motor,x_val,y_motor,y_val)
        #yield from mv(gvbt1,'open')
        uid = yield from count([rixscam,sclr],num=1, md = {'reason':' m7-gr scan {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_val) + \
                    ' , m7_pit = ' + str(y_val) + '\n'
        #yield from mv(gvbt1,'close')
    #yield from mv(gvbt1,'open')
    #yield from mv(gvsc1,'close')
    #uid = yield from count([rixscam,sclr],num=1, md = {'reason':'gv:sc1 dark'})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    #yield from mv(x_motor,x_ideal,y_motor, y_ideal)
    #yield from mv(gvsc1,'open')
    #uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    #if uid == None:
        #uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_ideal) + \
#                    ' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')
    
    print (f_string) 

def rixscam_m7_gr_2_axis_centroid_temp(cts, num_scans=1, extra_md = ' '):
    precison_digit = 4
    y_motor= espgm.m7pit
    #y_ideal= 4.8445#5.5349 
    #y_start = 4.7971#4.7813#5.4959
    #y_stop = 4.8919#5.5734
    y_ideal = 5.3915
    y_start = 5.3915-0.004*6
    y_stop = 5.3915+0.004*6


    x_motor=  espgm.grpit
    #x_ideal= 4.9281#6.2368
    #x_start= 4.8981#4.8881#6.2168
    #x_stop=  4.9581#6.2568
    x_ideal= 6.0139
    x_start= 6.0139-0.002*6
    x_stop = 6.0139+0.002*6
    num= 13
    
    f_string=''

    #yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , precison_digit)   
        y_val = round (y_start + i * (y_stop - y_start) / (num - 1) , precison_digit)      
        yield from mv (x_motor,x_val,y_motor,y_val)
        for s in range(num_scans):
            uid = yield from count([rixscam],num=cts, md = {'reason':' m7-gr scan {}'. format(extra_md)})        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_val) + \
                        ' , m7_pit = ' + str(y_val) + '\n'

    yield from mv(gvbt1,'close')
    
    print (f_string) 


def rixscam_m7_gr_2_axis_v1(  extra_md = ' '):
    precison_digit = 4
    y_motor= espgm.m7pit
    y_ideal= 5.543500 
    y_list = [5.3433,5.5433,5.7303,5.9003]

    x_motor=  espgm.grpit
    x_ideal= 6.238500 
    x_list=[6.1385,6.2385,6.3385,6.4385]
    num= 4 #12
    
    f_string=''
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from count([rixscam,sclr], md = {'reason':'dummy'})

    for i in range(num):
        x_val = x_list[i]  
        y_val = y_list[i]   
        yield from mv (x_motor,x_val,y_motor,y_val)
        yield from mv(gvbt1,'open')
        uid = yield from count([rixscam,sclr],num=1, md = {'reason':' m7-gr scan {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_val) + \
                    ' , m7_pit = ' + str(y_val) + '\n'
        yield from mv(gvbt1,'close')
    yield from mv(gvbt1,'open')
    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam,sclr],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    #yield from mv(x_motor,x_ideal,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    #uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    #if uid == None:
        #uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': gr_pit = ' + str(x_ideal) + \
#                    ' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')
    
    print (f_string) 

def rixscam_cff_m7_gr():
    #cffs = [2.22,2.24,2.25,2.26,2.27,2.28,2.29,2.30,2.32,2.34]  # for mbg
    cffs = [2.10,2.12,2.14,2.16,2.18,2.20,2.22,2.24,2.26]  # for mbg
    
    #yield from mv(sclr.preset_time, 180)
    #yield from mv(extslt.vg, 10)
    #extslt_vg = np.round(extslt.vg.user_readback.value,1)
    #yield from mv(rixscam.cam.acquire_time, 180)
    for cff in cffs:
        yield from mv(pgm.cff,  cff)#Fcryo_z
        yield from sleep(10)
        yield from mv(pgm.en, 1085)
        #yield from rixscam_m7_gr_2_axis(extra_md = np.str(cff)+np.str(extslt_vg))
    #yield from mv(sclr.preset_time, 1)
    yield from mv(rixscam.cam.acquire_time, 5)
    #yield from count([rixscam,sclr])
    yield from count([rixscam])

def rixscam_pgm_en(extra_md = '' ):
    """
    Looks like 50um extslt_vg is typical.
    """

    x_motor=pgm.en
    x_ideal = 1095 #462 #852.4 #1250lmm   
    x_start = 1060 #451 #821.4 #1250lmm   
    x_stop = 1130 #465
    num = 6 #8
    cts=60

    #yield from m1m3_max()
    extslt_vg_value = np.round(extslt.vg.user_readback.value,0)	
    
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md={'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 2)        
        yield from mv (x_motor,x_val)
        uid = yield from count([rixscam, ring_curr], num=cts, md = {'reason':'{} energy calibration - {}um vg'.format(extra_md, extslt_vg_value)})            
        #uid = yield from count([rixscam],num=1, md = {'reason':'{} energy calibration - {}um vg'.format(extra_md, extslt_vg_value)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm_en = ' + str(x_val) + '\n'
   

    yield from mv(gvbt1,'close')

    print (f_string)
    yield from mv(x_motor,x_ideal)  




def rixscam_m4slt(extra_md = '1800 + 2500 set' ):

    vgs = [1]
    hgs = [1.5]
    eslt = [10]
    num=4

    extslt_vg_value = np.round(extslt.vg.user_readback.value,0)	
    
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md={'reason':'dummy'})

    for i in range(num):
        #x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 2)        
        #yield from mv (x_motor,x_val)
        uid = yield from count([rixscam],num=1, md = {'reason':'{} energy calibration - {}um vg'.format(extra_md, extslt_vg_value)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm_en = '# + str(x_val) + '\n'
   

    yield from mv(gvbt1,'close')
    yield from mv(rixscam.cam.acquire_time, 5)
    yield from count([rixscam],num=1, md = {'reason':'dummy'})
    print (f_string)
    #yield from mv(x_motor,x_ideal)  


def rixscam_energies(extra_md = '' ):
    yield from mv(extslt.vg,30)
    yield from pol_H()
       
    f_string=''
    
    yield from mv(espgm.m7pit,5.4210)
    i = 576.5
    yield from mv(pgm.en, i)
    yield from align.m1pit
    yield from m3_check() 
    yield from mv(gvbt1,'open')
    for j in range (0, 12):
        yield from mvr(cryo.y,-0.01)
        uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    yield from mv(gvbt1,'close')
     
    #yield from align.m1pit
    #yield from m3_check()

    #for j in range (0, 12):
    #    yield from mvr(cryo.y,-0.01)
    #    uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
    #    if uid == None:
    #       uid = -1
    #    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    #yield from mv(gvbt1,'close')

    yield from mv(espgm.m7pit,5.4305)
    i = 579.3
    yield from mv(pgm.en, i)
    yield from align.m1pit
    yield from m3_check() 
    yield from mv(gvbt1,'open')
    for j in range (0, 12):
        yield from mvr(cryo.y,-0.01)
        uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    yield from mv(gvbt1,'close')
     
    #yield from align.m1pit
    #yield from m3_check()

    #for j in range (0, 12):
    #    yield from mvr(cryo.y,-0.01)
    #    uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
    #    if uid == None:
    #       uid = -1
    #    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    #yield from mv(gvbt1,'close')
    
    yield from mv(espgm.m7pit,5.4385)
    i = 580.5
    yield from mv(pgm.en, i)
    yield from align.m1pit
    yield from m3_check() 
    yield from mv(gvbt1,'open')
    for j in range (0, 12):
        yield from mvr(cryo.y,-0.01)
        uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    yield from mv(gvbt1,'close')
     
    #yield from align.m1pit
    #yield from m3_check()

    #for j in range (0, 12):
    #    yield from mvr(cryo.y,-0.01)
    #    uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
    #    if uid == None:
    #       uid = -1
    #    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
    #yield from mv(gvbt1,'close')


    yield from mv(gvbt1,'open')
    yield from mv(gvsc1,'close')
    for i in range(0,3):
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'open')
    
    print (f_string) 

def rixscam_acquire(detectors
, Ei_vals, m7_pit_vals, num_rixs_im, pol_type=None, extra_md = ' ' ):
    """
    Parameters
    ----------
    detectors:  list 
        detectors to be used with rixs spectra
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

    if pol_type == 'H':
        yield from pol_H(0) #TODO fix this - find a better way in profile to manage this
    elif pol_type == 'V':
        yield from pol_V(3) #TODO fix this - find a better way in profile to manage this
    elif pol_type == None:
        if np.round(epu1.phase.position,1) == 0.0:
            pol_type = 'H'
        if np.round(epu1.phase.position,1) == 28.5:
            pol_type = 'V'
    else:
        print('You forgot to specify the polarization type (pol_type) or the epu1.phase is not as expected.')
    print('Checking m7 now')
    if m7_pit_vals != None:
        print('\tm7 is okay')
        if len(Ei_vals) == len(m7_pit_vals):
            pass
        else:
            print('\n\nInvalid  parameters for incident energy and m7 pitch: \n\tEnergy and pitch list lengths are: {} and {}, repectively.\n'.format(len(Ei_vals), len(m7_pit_vals)))
            raise

      
    print('\n\nStarting plan for {} polarized light with {} rixs images for each Ei = {}\n\n'.format(pol_type,num_rixs_im,Ei_vals))
    
    f_string=''
    md_string = 'no md string yet'
    yield from count(detectors, md = {'reason':'dummy'})
    print('Ya dumnmy')
    for i in range(len(Ei_vals)):
        yield from mv(pgm.en, Ei_vals[i])
        if m7_pit_vals  != None:
            yield from mv(espgm.m7pit, m7_pit_vals[i])
        yield from mv(gvbt1,'open')
        #scan_num_cor = 2+2*i
        print('\t\tTaking Lights for RIXS Now')
        #LIGHTS
        for j in range(0, num_rixs_im):
            yield from mvr(cryo.y,-0.005)
            print('\t\tTaking Lights for RIXS REALLY')
            md_string = str(extra_md) + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV - Pol ' + str(pol_type)
            uid = yield from count(detectors,num=1, md = {'reason':'{}'. format(md_string)}) 
            #uid = yield from count([rixscam],num=1, md = {'reason':'{} - E = {:3.3f}eV - Pol {}'. format(extra_md, Ei_vals[i], pol_type)}) 
            if uid == None:
                uid = db[-1].start['scan_id']#+1+j+scan_num_cor
                f_string += 'scan no ' + str(uid) + ' ' + str(md_string) + '\n'
                #print(md_string)
                #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            else:
                f_string += 'scan no ' + str(db[uid].start['scan_id']) + ' ' + str(md_string) + '\n'
                #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
        yield from mv(gvbt1,'close')
         
        #DARKS
    #yield from mv(gvbt1,'open')
    #yield from mv(gvsc1,'close')
    #for i in range(0,2):
        #uid = yield from count(detectors,num=1, md = {'reason':'gv:sc1 dark'})        
        #if uid == None:
        #  uid = -1
        #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    #yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'open')
    
    #print(f_string) 
    #print('\n\n EXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))



def rixscam_acquire_sample_c_tape(Ei_vals, m7_pit_vals, sample, c_tape, num_rixs_im, pol_type=None, extra_md = ' ' ):
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

    print('\n\n\tEnsuring beamline exit slit vertical gap is at 20 um\n\n')
    yield from mv(extslt.vg,20, extslt.hg, 150)

    if pol_type == 'H':
        yield from pol_H(0) #TODO fix this - find a better way in profile to manage this
    elif pol_type == 'V':
        yield from pol_V(3) #TODO fix this - find a better way in profile to manage this
    elif pol_type == None:
        if np.round(epu1.phase.position,1) == 0.0:
            pol_type = 'H'
        if np.round(epu1.phase.position,1) == 28.5:
            pol_type = 'V'
    else:
        print('You forgot to specify the polarization type (pol_type) or the epu1.phase is not as expected.')
    print('Checking m7 now')
    if m7_pit_vals != None:
        print('\tm7 is okay')
        if len(Ei_vals) == len(m7_pit_vals):
            pass
        else:
            print('\n\nInvalid  parameters for incident energy and m7 pitch: \n\tEnergy and pitch list lengths are: {} and {}, repectively.\n'.format(len(Ei_vals), len(m7_pit_vals)))
            raise

      
    print('\n\nStarting plan for {} polarized light with {} rixs images for each Ei = {}\n\n'.format(pol_type,num_rixs_im,Ei_vals))
    
    f_string=''
    md_string = 'no md string yet'
    yield from count([rixscam], md = {'reason':'dummy'})
    print('Ya dumnmy')
    for i in range(len(Ei_vals)):
        yield from mv(pgm.en, Ei_vals[i])
        if m7_pit_vals  != None:
            yield from mv(espgm.m7pit, m7_pit_vals[i])
        yield from mv(gvbt1,'open')
        #scan_num_cor = 2+2*i
        print('\t\tTaking Lights for RIXS Now')
        #LIGHTS
        for j in range(0, num_rixs_im):
            #SAMPLE POSITION 
            yield from mv(cryo.x,sample[0])
            yield from mv(cryo.y,sample[1]-0.002*i)
            yield from mv(cryo.z,sample[2])
            print('\t\tTaking RIXS from the SAMPLE')
            md_string = str(extra_md) + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV - Pol ' + str(pol_type)
            uid = yield from count([rixscam,qem11,qem12],num=1, md = {'reason':'{}'. format(md_string)}) 
            if uid == None:
                uid = db[-1].start['scan_id']
                f_string += 'scan no ' + str(uid) + ' ' + str(md_string) + '\n'
                #print(md_string)
                #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            else:
                f_string += 'scan no ' + str(uid) + ' ' + str(md_string) + '\n'
                #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'

            #C-tape POSITION 
            yield from mv(cryo.x,c_tape[0])
            yield from mv(cryo.y,c_tape[1])
            yield from mv(cryo.z,c_tape[2])
            print('\t\tTaking RIXS from the C-tape')
            md_string_2 = 'C - tape' + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV - Pol ' + str(pol_type)
            uid = yield from count([rixscam,qem11,qem12],num=1)
            if uid == None:
                uid = db[-1].start['scan_id']
                f_string += 'scan no ' + str(uid) + ' ' + str(md_string_2) + '\n'
                #print(md_string_2)
                #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            else:
                #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'   
                f_string += 'scan no ' + str(db[uid].start['scan_id']) + ' ' + str(md_string_2) + '\n'        

        yield from mv(gvbt1,'close')
         
        #DARKS
    yield from mv(gvbt1,'open')
    yield from mv(gvsc1,'close')
    for i in range(0,2):
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'open')
    
    print(f_string) 
    print('\n\n EXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))


def rixscam_acquire_V2(Ei_vals, m7_pit_vals, num_rixs_im, pol_type=None, extra_md = ' ' ):
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

    print('\n\n\tEnsuring beamline exit slit vertical gap is at 20 um\n\n')
    yield from mv(extslt.vg,20, extslt.hg, 150)
    try:
        if pol_type == 'H':
            yield from pol_H(0) #TODO fix this - find a better way in profile to manage this
        elif pol_type == 'V':
            yield from pol_V(3) #TODO fix this - find a better way in profile to manage this
        elif pol_type == None:
            if np.round(epu1.phase.position,1) == 0.0:
                pol_type = 'H'
            if np.round(epu1.phase.position,1) == 28.5:
                pol_type = 'V'
        else:
            print('You forgot to specify the polarization type (pol_type) or the epu1.phase is not as expected.')
            raise
        print('Checking m7 now')
        if m7_pit_vals != None:
            print('\tm7 is okay')
            if len(Ei_vals) == len(m7_pit_vals):
                pass
            else:
                print('\n\nInvalid  parameters for incident energy and m7 pitch: \n\tEnergy and pitch list lengths are: {} and {}, repectively.\n'.format(len(Ei_vals), len(m7_pit_vals)))
                raise

      
        print('\n\nStarting plan for {} polarized light with {} rixs images for each Ei = {}\n\n'.format(pol_type,num_rixs_im,Ei_vals))
        
        f_string=''
        md_string = 'no md string yet'
        yield from count([rixscam], md = {'reason':'dummy'})
        print('Ya dumnmy')

        for i in range(len(Ei_vals)):
            yield from mv(pgm.en, Ei_vals[i])
            if m7_pit_vals  != None:
                yield from mv(espgm.m7pit, m7_pit_vals[i])
            yield from mv(gvbt1,'open')
            #scan_num_cor = 2+2*i
            print('\t\tTaking Lights for RIXS Now')
            #LIGHTS
            for j in range(0, num_rixs_im):
                yield from mvr(cryo.y,-0.002)
                print('\t\tTaking Lights for RIXS REALLY')
                md_string = str(extra_md) + ' - E = ' + str(np.round(Ei_vals[i],3)) + 'eV - Pol ' + str(pol_type)
                uid = yield from count([rixscam],num=1, md = {'reason':'{}'. format(md_string)}) 
                #uid = yield from count([rixscam],num=1, md = {'reason':'{} - E = {:3.3f}eV - Pol {}'. format(extra_md, Ei_vals[i], pol_type)}) 
                if uid == None:
                    uid = db[-1].start['scan_id']#+1+j+scan_num_cor
                    f_string += 'scan no ' + str(uid) + str(md_string) + '\n'
                    print(md_string)
                    #f_string += 'scan no ' + str(uid) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
                else:
                    f_string += 'scan no ' + str(uid) + str(md_string) + '\n'
                    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(np.round(Ei_vals[i],3)) + '\n'
            yield from mv(gvbt1,'close')
         
        #DARKS
        yield from mv(gvbt1,'open')
        yield from mv(gvsc1,'close')
        for i in range(0,2):
            uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
        yield from mv(gvbt1,'close')
        yield from mv(gvsc1,'open')
    
        print(f_string) 
        print('/n/n EXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))

    except Exception:
        yield from mv(gvbt1,'close')
        yield from mv(gvsc1,'open')	
        print('OOPS!  The plan stopped.  The completed scans are:\n')
        print(f_string)
        print('\n\nEXAMPLE METADATA FOR SCAN:\n\t {}\n\n'.format(md_string))




def rixscam_test_LV_LH(extra_md = '' ):
    yield from mvr(cryo.y, -0.01)
    x_motor=pgm.en
    x_val=579.5
    yield from mv(x_motor,x_val)

    yield from pol_H(4)
#    yield from align.m1pit
#    yield from m3_check()  
    yield from mv(gvbt1,'open')

    yield from count([rixscam])
    f_string=''
    for i in range(0,3):
        uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = 579.5 eV - Pol H'. format(i)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm_en = ' + str(x_val) + 'Pol H' '\n'
    yield from mv(gvbt1,'close')

    yield from pol_V(6)
 #   yield from align.m1pit
 #   yield from m3_check()  
    yield from mv(gvbt1,'open')

    yield from count([rixscam])

    for i in range(0,3):
        uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = 579.5 eV - Pol V'. format(i)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm_en = ' + str(x_val) + 'Pol V' '\n'
    yield from mv(gvbt1,'close')

    print (f_string)
    
    yield from pol_H(4)

def rixscam_Ei_dep(extra_md = '' ):
    yield from mv(extslt.vg,30)
    yield from pol_H()
    yield from align.m1pit
    yield from m3_check()    
    f_string=''
    
    yield from mv(espgm.m7pit,5.4210)
    for i in np.arange(575,578,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
        yield from mv(gvbt1,'close')

    yield from mv(espgm.m7pit,5.4305)
    for i in np.arange(578,580,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
        yield from mv(gvbt1,'close')
    
    yield from mv(espgm.m7pit,5.4385)
    for i in np.arange(580,582.5,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol H'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
            #print(f_string)
        yield from mv(gvbt1,'close')


    yield from mv(gvbt1,'open')
    yield from mv(gvsc1,'close')
    for i in range(0,3):
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'open')
    
    print (f_string) 
 
    yield from mv(pgm.en, 575)
    yield from pol_V()
    yield from sleep(300)
    yield from align.m1pit
    yield from m3_check()    
    f_string=''

    yield from mv(espgm.m7pit,5.4210)
    for i in np.arange(575,578,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol V'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
        yield from mv(gvbt1,'close')

    yield from mv(espgm.m7pit,5.4305)
    for i in np.arange(578,580,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol V'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
        yield from mv(gvbt1,'close')
    
    yield from mv(espgm.m7pit,5.4385)
    for i in np.arange(580,582.5,0.5):
        yield from mv(pgm.en, i)
        yield from mv(gvbt1,'open')
        for j in range (0, 6):
            yield from mvr(cryo.y,-0.01)
            uid = yield from count([rixscam],num=1, md = {'reason':' Sr2CrO4 - E = {} eV - Pol V'. format(i)})        
            if uid == None:
               uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': E = ' + str(i) + '\n'
        yield from mv(gvbt1,'close')


    yield from mv(gvbt1,'open')
    yield from mv(gvsc1,'close')
    for i in range(0,3):
        uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    yield from mv(gvbt1,'close')
    yield from mv(gvsc1,'open')
    
    print (f_string) 


def rixscam_dc_z_optimization(extra_md = '' ):
    x_motor=  dc.z
    x_ideal= 260
    x_start= x_ideal + 12
    x_stop=  x_ideal - 12
    num=  9 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)#,y_motor,y_val)
        #yield from mv(gvbt1,'open') 
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
           uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc_z = ' + str(x_val) + '\n'#\
                   # ' , m7_pit = ' + str(y_val) + '\n'
        #yield from mv(gvbt1,'close')

    yield from mv(gvsc1,'close')
    #uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    #yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    #uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    #if uid == None:
        # uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc_z = ' + str(x_ideal) + '\n'#\
                    #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_dc_z_optimization_centroid(num_scan):
    x_motor=  dc.z
    x_ideal= 260
    x_start= x_ideal + 12
    x_stop=  x_ideal - 12
    num=  9 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)#,y_motor,y_val)
        
        for i in range(num_scan):
            uid = yield from count([rixscam],num=1)        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc.z = ' + str(x_val) + '\n'
        
    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_cff_optimization(extra_md = '' ):
    x_motor= pgm.cff
    y_motor= pgm.en
    y_val= 1085
    x_ideal= 2.26
    x_start= x_ideal -0.16 #0.04#
    x_stop=  x_ideal +0.08 #0.04#
    num= 13 #5 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(5)
        yield from mv (y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm.cff = ' + str(x_val) + '\n'#\
                   # ' , m7_pit = ' + str(y_val) + '\n'
    #yield from mv(gvsc1,'close')
    #uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    #yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
    #yield from mv(gvsc1,'open')
   # uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm.cff = ' + str(x_ideal) + '\n'#\
    #                #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)




def rixscam_cff_optimization_centroid(num_scan):
    x_motor= pgm.cff
    y_motor= pgm.en
    y_val= 1085
    x_ideal= 2.20
    x_start= x_ideal -0.1 #0.04#
    x_stop=  x_ideal +0.1 #0.04#
    num= 11 #5 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})
    yield from mv(gvbt1,'open')
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(5)
        yield from mv (y_motor,y_val)
        for i in range(num_scan):
            uid = yield from count([rixscam],num=1)        
            if uid == None:
                uid = -1
            f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': pgm.cff = ' + str(x_val) + '\n'
  
    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_exit_slit_optimization(extra_md = '' ):
    x_motor= extslt.vg
    y_motor= pgm.en
    y_val= 850.7
    x_ideal= 10
    x_start= x_ideal +70
    x_stop=  x_ideal
    num= 8 #12
    yield from mv(gvbt1,'open')
    f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 4)        
        yield from mv (x_motor,x_val)
        yield from sleep(5)
        yield from mv (y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' {}'. format(extra_md)})        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': extslt.vg = ' + str(x_val) + '\n'#\
                   # ' , m7_pit = ' + str(y_val) + '\n'
    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
   # uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    #if uid == None:
    #    uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': extslt.vg = ' + str(x_ideal) + '\n'#\
    #                #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')
    yield from mv (x_motor,x_ideal)
    print (f_string)


def rixscam_motor1_rel_scan(motor1, ideal, plus, minus, pts, extra_md = '' ):
    x_motor=  motor1
    x_ideal= ideal
    x_start= x_ideal + plus
    x_stop=  x_ideal - minus
    num= pts #12
    yield from mv(gvbt1,'open')
    #f_string=''

    yield from count([rixscam], md = {'reason':'dummy'})

    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)#,y_motor,y_val)
        uid = yield from count([rixscam],num=1, md = {'reason':' scan {} {}'. format(motor1.name, extra_md)})        
        if uid == None:
            uid = -1
        #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc_z = ' + str(x_val) + '\n'#\
        #           # ' , m7_pit = ' + str(y_val) + '\n'
    yield from mv(gvsc1,'close')
    uid = yield from count([rixscam],num=1, md = {'reason':'gv:sc1 dark'})        
    if uid == None:
        uid = -1
    f_string += 'scan no ' + str(db[uid].start['scan_id']) + ':  dark \n'
    
    yield from mv(x_motor,x_ideal)#,y_motor, y_ideal)
    yield from mv(gvsc1,'open')
    uid = yield from count([rixscam],num=1, md = {'reason':'returned to center'})        
    if uid == None:
        uid = -1
    #f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': dc_z = ' + str(x_ideal) + '\n'#\
    #                #' , m7_pit = ' + str(y_ideal) + '\n'

    yield from mv(gvbt1,'close')

    print (f_string)


def rixscam_m7_pit():
    x_motor=espgm.m7_pit
    x_start=5.6
    x_stop=4.6
    num=50


    #yield from count([rixscam],num=1)  #refresh CCD
    for i in range(num):
        x_val = round (x_start + i * (x_stop - x_start) / (num - 1) , 3)        
        yield from mv (x_motor,x_val)
        uid = yield from count([rixscam],num=1)        
        if uid == None:
            uid = -1
        f_string += 'scan no ' + str(db[uid].start['scan_id']) + ': m7_pit = ' + str(x_val) 

    print (f_string)
    yield from mv(gvbt1,'close')



def m1_check():
    yield from mv(extslt.hg,20)
    yield from rel_scan([qem07],m1.pit,-30,30,31, md = {'reason':'checking m1 before each cff'})
    yield from mv(m1.pit,peaks.cen['gc_diag_grid'])
    yield from mv(extslt.hg,150)


def post_3AAyag_align():
    det=[sc_4]    

    x_axis=espgm.gr_pit
    x_start=1
    x_stop=5
    x_num=21
    
    y_axis=cryo.t
    #y_start=64.33
    y_start=65.09
    y_stop=66.33
    #y_num=51
    y_num=32


    for i in range(y_num):
        y=y_start+i*(y_stop-y_start)/(y_num-1)
        yield from mv(y_axis,y)
        yield from scan(det,x_axis,x_start,x_stop,x_num)
        #yield from mvr(x_axis, (x_start-x_stop)/(x_num-1)) # 2 lines added because scan is timing out
        #yield from sleep(2.5) # 


def lunch():
    for i in range(1,5):
        yield from mv(cryo.z,29+i)
        yield from scan([qem11],pgm.en,850,860,51)
    
    yield from mv(cryo.z,31)

    for i in range(0,7):
        yield from mv(cryo.y,34.5+i*0.5)
        yield from scan([qem11],pgm.en,850,860,51)
    yield from mv(cryo.y,36)
   
def m1_align():

    m1x_init=1.05040
    m1pit_init=1802
    m1pit_start=1000
    m1pit_step=250

    for i in range(0,9):
        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
        yield from scan([qem01,qem05],m1.x,-4,2,31)
    yield from mv(m1.pit,m1pit_start)

def m1_align_fine():

    m1x_init=0.28945     #0.46 #this is what I found, but this looks unused 
    m1pit_init=1934
    m1pit_start=1800
    m1pit_step=50

    for i in range(0,7):
        yield from mv(m1.x,0)
        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
        yield from rel_scan([qem05],m1.x,-3.5,3.5,36)
    yield from mv(m1.pit,m1pit_start)
    
#def m1_align_fine2():  ## MOVED to STANDAR-PLANS in STartup

#    m1x_init=m1.x.user_readback.value
#    m1pit_init=m1.pit.user_readback.value
#    m1pit_step=50
#    m1pit_start=m1pit_init-3*m1pit_step
    
#    for i in range(0,7):
#        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
#        yield from rel_scan([qem05],m1.x,-3.5,3.5,36)
#    yield from mv(m1.pit,m1pit_start)


def find_energy():
    pgm_m2_start=88.344903
    pgm_gr_start=87.678349
    
    yield from mv(pgm.m2_pit,pgm_m2_start)
    yield from mv(pgm.gr_pit,pgm_gr_start)
    yield from relative_inner_product_scan([qem07],451,pgm.m2_pit,-2,1.0,pgm.gr_pit,-2,1.0)

    yield from sleep(60)    
    yield from mv(pgm.m2_pit,pgm_m2_start)
    yield from mv(pgm.gr_pit,pgm_gr_start)
    yield from scan([qem07],epu1.gap,20,55,141)

    

def m1m3_max():
    temp_extslt_vg=extslt.vg.user_readback.value
    temp_extslt_hg=extslt.hg.user_readback.value
    yield from gcdiag.grid
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,20)  
        
    yield from relative_scan([qem07],m1.pit,-30,30,31)
    yield from mv(m1.pit,peaks['cen']['gc_diag_grid'])
    yield from sleep(10)
    yield from relative_scan([qem07],m3.pit,-0.0005,0.0005,31)
    yield from mv(m3.pit,peaks['cen']['gc_diag_grid']) 
    
    yield from mv(extslt.hg,temp_extslt_hg)
    yield from mv(extslt.vg,temp_extslt_vg)  
    yield from gcdiag.out
       

def m3_tune():
    #extslt_hg=0.12
    #extslt_vg=0.1
    m3_pit_start=-0.754240
    m3_x_start=3.4
    m3_pit_step=1
    m3_x_step=1

    for i in range(0,10):
    	yield from mv(m3.pit,m3_pit_start-m3_pit_step)
    	yield from sleep(10)
    	yield from mv(m3.pit,m3_pit_start)
    	yield from sleep(10)
    	yield from relative_scan([qem07],extslt.hc,-1,1,201)
	
    for i in range(0,10):
    	yield from mv(m3.x,m3_x_start-m3_x_step)
    	yield from sleep(10)
    	yield from mv(m3.x,m3_x_start)
    	yield from sleep(10)
    	yield from relative_scan([qem07],extslt.hc,-1,1,201)

    for i in range(0,10):
    	yield from mv(m3.pit,m3_pit_start+m3_pit_step)
    	yield from sleep(10)
    	yield from mv(m3.pit,m3_pit_start)
    	yield from sleep(10)
    	yield from relative_scan([qem07],extslt.hc,-1,1,201)
	
    for i in range(0,10):
    	yield from mv(m3.x,m3_x_start+m3_x_step)
    	yield from sleep(10)
    	yield from mv(m3.x,m3_x_start)
    	yield from sleep(10)
    	yield from relative_scan([qem07],extslt.hc,-1,1,201)

    for i in range(0,50):
    	yield from sleep(600)
    	yield from relative_scan([qem07],extslt.hc,-1,1,201)

def m3_focus():
    m3_pit_start=-0.754240
    extslt_hc_start=-3.68615

    for i in range(0,30):
        yield from mv(m3.pit,m3_pit_start-0.00072*i)
        yield from mv(extslt.hg,40)
        yield from relative_scan([qem07],extslt.hc,-0.4,0.4,21)
        yield from mv(extslt.hc,peaks['max']['gc_diag_diode'][0])
        yield from sleep(5)
        yield from mv(extslt.hg,6)
        yield from relative_scan([qem07],extslt.hc,-0.12,0.12,41)
        yield from mv(extslt.hc,peaks['cen']['gc_diag_diode']-0.2)

def m3_stability_focus():
    m3_pit_start=-0.754240
    extslt_hc_start=-3.71405
    yield from mv(extslt.hg,10)
    for i in range(0,30):
        yield from relative_scan([qem07],extslt.hc,-0.4,0.4,81)
        yield from mv(extslt.hc,peaks['cen']['gc_diag_diode'])
        yield from sleep(900)

    for i in range(0,30):
        yield from mv(m3.pit,m3_pit_start-0.00072*i)
        yield from mv(extslt.hg,40)
        yield from relative_scan([qem07],extslt.hc,-0.4,0.4,21)
        yield from mv(extslt.hc,peaks['max']['gc_diag_diode'][0])
        yield from sleep(5)
        yield from mv(extslt.hg,6)
        yield from relative_scan([qem07],extslt.hc,-0.12,0.12,41)
        yield from mv(extslt.hc,peaks['cen']['gc_diag_diode']-0.2)


def find_center_of_rot():
    ow_start = 39.45
    ow_step = 0.01
    m4pit_start = -4.0435
    m4pit_step = 0.005
    
    for i in range(0,30):
        yield from mv(m4.pit,m4pit_start-i*m4pit_step)
        yield from sleep(10)
        print('Current cycle number: {}' .format(i))
        yield from scan([qem11],ow,ow_start-25*ow_step,ow_start+25*ow_step,51)    
        yield from sleep(10)


def center_of_rot():
    yield from mv(epu1.gap,41.2)
    yield from mv(pgm.en,930)
    
    #yield from mv(cryo.y,100)
    #yield from mv(cryo.x,50)
    #yield from mv(ow,39.75)

    for i in range(0,25):
        yield from mv(m4.x,3.6+0.1*(i-12))
        yield from sleep(10)
        yield from scan([qem10,qem11],m4.pit,-4.21,-4.15,121)    
        #yield from scan([qem10,qem11],m4.pit,-4.145,-4.115,61)
        yield from sleep(30)

    yield from mv(m4.x,3.6)


def center_of_rot_coordinated():
    yield from mv(epu1.gap,41.2)
    yield from mv(pgm.en,930)
    
    #yield from mv(cryo.y,100)
    #yield from mv(cryo.x,50)
    #yield from mv(ow,39.5)

    for i in range(0,6):
        yield from mv(m4.x,3.6+0.1*(i+5))
        yield from mv(extslt.hc,-5.03560+0.057*(i+5))
        yield from mv(m3.pit,-0.753135+0.000204*(i+5))
        yield from sleep(10)
        yield from scan([qem10,qem11],m4.pit,-4.220,-4.20,41)    
        #yield from scan([qem10,qem11],m4.pit,-4.145,-4.115,61)
        yield from sleep(30)

    yield from mv(m4.x,3.6)
    yield from mv(m3.pit,-0.753135)
    yield from mv(extslt.hc,-5.03560)


def center_of_rot_yaw():
    yield from mv(epu1.gap,41.00)
    yield from mv(pgm.en,930)
    
    #yield from mv(cryo.y,100)
    #yield from mv(cryo.x,50)
    #yield from mv(ow,39.75)
    yield from mv(m4.x,1.2)

    for i in range(0,10):
        yield from mv(m4.yaw,-1.48-0.01*i)
        yield from sleep(10)
        yield from scan([qem10,qem11],m4.pit,-4.21,-4.15,121)    
        #yield from scan([qem10,qem11],m4.pit,-4.145,-4.115,61)
        yield from sleep(30)

    yield from mv(m4.yaw,-1.1850)
    

def epu_calib_left():
    yield from mv(epu1.phase, 28.5)
    d = [qem07]
    #FE slit H and V gap to 1.2 mm
    yield from mv(feslt.hg,1.5)
    yield from mv(feslt.vg,1.5)
    yield from mv(pgm.cff,2.330)

    yield from sleep(100)
    #3rd Harmonic
    for i in range(1400,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-0.5)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,1.0,75)


def m4_yaw_roll():  
    #cryo.x.settle_time=0.2
    #cryo.y.settle_time=0.2
    
    #r_md = 'V beam with yaw roll'
    
    #yield from mv(extslt.vg,30)
    #yield from mv(extslt.hg,150)
    #yield from mv(epu1.gap,40.8) #detunedyield from mv(cryo.x,33.50)
#    mir4_rol_init = 1.421
#    mir4_rol_step= 0.002
    mir4_yaw_init = -0.70585
    mir4_yaw_step = 0.0003 #0.002

    for i in range(-10,-3):
        yield from mv(m4.yaw, mir4_yaw_init + mir4_yaw_step * (1 * i))
        #yield from mv(m4.rol,mir4_rol_init+mir4_rol_step*(1*i))
        #yield from mv(cryo.x,39.0)
        yield from mv(cryo.y,11.938) # to be adjusted
        yield from sleep(5)
        yield from rel_scan([sclr],cryo.y,0,0.02,61)
        #yield from rel_scan([sclr],cryo.y,0,0.04,121, md={'reason':r_md})


def pitch_and_yaw():
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    
    
    #yield from mv(extslt.hg,150)
    mir4_pit_init = -4.1027
    mir4_pit_step = -0.0003

    for i in range(0,6):
        yield from mv(m4.pit, mir4_pit_init + mir4_pit_step * (1 * i))
        yield from m4_yaw_roll()


def m4_y():  
    
    yield from mv(extslt.vg,20)
    yield from mv(extslt.hg,300)
    yield from mv(epu1.gap,40.8) #detunedyield from mv(cryo.x,33.50)
    mir4_y_init = 96.875
    mir4_y_step= 0.05
    
    for i in range(1, 7):
        yield from mv(m4.y,mir4_y_init+mir4_y_step*(1*i-3))
        yield from mv(cryo.x,39.3)
        yield from mv(cryo.y,94.47)
        yield from sleep(10)
        yield from relative_scan([sclr],cryo.y,0,0.15,31)
        
def m4_pit():
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    #yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    #yield from mv(epu1.gap,40.8) #detuned EPU @930 eV
    mir4_pit_init = -4.1024
    mir4_pit_step= 0.0003 #0.001

    for i in range(-7, 8):
        yield from mv(m4.pit,mir4_pit_init+1*mir4_pit_step*(1*i))
        #yield from mv(cryo.x,37.8)
        yield from mv(cryo.y,90.152) # to be adjusted
        yield from sleep(10)
        yield from relative_scan([sclr],cryo.y,0,0.02,41)
        #yield from relative_scan([sclr],cryo.y,0,0.10,31)
        #yield from mv(cryo.y,97.5)
        #yield from mv(cryo.x,43.350+0.08*(1*i))
        #yield from mv(cryo.x,42.7) # to be adjusted
        #yield from sleep(30)
        #yield from relative_scan(d11,cryo.x,0,0.4,121)


def m4_z():  
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    #yield from mv(epu1.gap,40.8) #detuned EPU @930 eV 
    mir4_z_init = -5.4
    mir4_z_step= 0.1
    
    for i in range(0, 15):
        yield from mv(m4.z,mir4_z_init+mir4_z_step*(1*i-7))
        yield from mv(cryo.x,40)
        yield from mv(cryo.y,94.44-0.01*(i-7))
        yield from sleep(10)
        yield from relative_scan([sclr],cryo.y,0,0.1,31)
        #yield from mv(cryo.y,98.0)
        #yield from mv(cryo.x,42.7-(1*i-5)*0.028)
        #yield from mv(cryo.x,42.7)
        #yield from sleep(30)
        #yield from relative_scan(d11,cryo.x,0,0.4,121) 


def m4_z_pit(): 

    start_scan_id=None
    total_num_scans=110
    
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    d11 = [qem11]
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,300)
    #yield from mv(epu1.gap,38) #detuned EPU @852 eV 
    mir4_z_init = -1.4
    mir4_z_step= 0.5
    mir4_pit_init = -4.085
    mir4_pit_step= 0.003

    for i in range(0, 5): 
        yield from mv(m4.z,mir4_z_init+mir4_z_step*(1*i-2)) 
        yield from sleep(30)
        for i in range(0, 11):
            yield from mv(m4.pit,mir4_pit_init+mir4_pit_step*(1*i-5))
            yield from sleep(30)
            
            yield from mv(cryo.y,97)
            yield from mv(cryo.x,43.05+0.1*(1*i-5)) # to be adjusted
            yield from sleep(30)
            uid = yield from relative_scan(d11,cryo.x,0,0.5,101)  
            if uid is not None and start_scan_id is None:
                start_scan_id = db[uid].start['scan_id']
            
            if start_scan_id is not None: current_plan_time(start_scan_id,total_num_scans)

            yield from mv(cryo.x,42)
            yield from mv(cryo.y,97.6) # to be adjusted
            yield from sleep(30)
            yield from relative_scan(d11,cryo.y,0,0.4,121)
            if start_scan_id is not None: current_plan_time(start_scan_id,total_num_scans)


def m4_z_pit_2(): 

    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    d11 = [qem11]
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,300)
    #yield from mv(epu1.gap,38) #detuned EPU @852 eV 
    mir4_z_init = -5.4
    mir4_z_step= 0.5
    mir4_pit_init = -4.061
    mir4_pit_step= 0.003

    #for i in range(0, 5): 
        #yield from mv(m4.z,mir4_z_init+mir4_z_step*(1*i-2))
        #yield from sleep(30)
    for i in range(0, 7):
        yield from mv(m4.pit,mir4_pit_init+mir4_pit_step*(1*i-3))
        yield from sleep(5)
        yield from mv(cryo.y,96.28) # to be adjusted
        yield from sleep(10)
        yield from relative_scan(d11,cryo.y,0,0.2,61)


def m4_x():  
    d11 = [qem11]
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,3000)
    yield from mv(epu1.gap,40.7) #detunedyield from mv(cryo.x,33.50)
    mir4_x_init = 3.2
    extslt_hc_init = -4.106
    mir3_pit_init = -0.751240
    mir4_x_step= 0.1
    mir3_pit_step=0.0002164 # +5.55% correction with respect to theoretical 0.00205
    extslt_hc_step=0.05715
    
    for i in range(0, 11):
        yield from mv(m4.x,mir4_x_init+mir4_x_step*(1*i-5))
        yield from mv(extslt.hc,extslt_hc_init+extslt_hc_step*(1*i-5))
        yield from mv(m3.pit,mir3_pit_init+mir3_pit_step*(1*i-5))
        yield from sleep(30)
        yield from mv(cryo.x,36)
        yield from mv(cryo.y,98.6)
        yield from sleep(30)
        yield from scan(d11,cryo.y,98.5,98.8,91)
        yield from mv(cryo.y,98.0)
        yield from mv(cryo.x,+(1*i-5)*0.1)
        yield from sleep(30)
        yield from scan(d11,cryo.x,37.5+(1*i-5)*0.1,37.8+(1*i-5)*0.1,91)

def m4_vexitslt_focus():
    #d11=[qem11]
    d11=[sclr]
    extslt_ini=5
    extslt_final=42.5
    extslt_step=2.5
    
    for i in range(0, 1+round(abs(extslt_ini-extslt_final)/extslt_step)):
        yield from mv(extslt.vg,extslt_ini+i*extslt_step)
        #yield from sleep(5)
        #yield from mv(cryo.x,40.6)
        yield from mv(cryo.y,67.065) # to be adjusted
        yield from sleep(1)
        yield from relative_scan([sclr],cryo.y,0,0.015,46)
        #yield from mv(cryo.y,98)
        #yield from mv(cryo.x,43.2) # to be adjusted
        #yield from sleep(30)
        #yield from relative_scan(d11,cryo.x,0,0.4,151)  

def m4_depth_of_focus():
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,150)
    cryo_z_init = 0.1#-0.8
    cryo_z_step= 0.15
    v_focus_x = 37.65
    v_focus_y = 89.950

    for i in range(-6, 21): #-15, 16
        yield from mv(cryo.z,cryo_z_init + cryo_z_step * (1 * i))
        yield from mv(cryo.x, v_focus_x)
        yield from mv(cryo.y, v_focus_y) 
        yield from sleep(5)
        print('\n\n\t\tMoved cryo.z for i = {}\n\n'.format(i))
        yield from rel_scan([sclr],cryo.y,0,0.035,106)

    yield from mv(cryo.z,cryo_z_init)
    cryo_x_init = 38.45

    yield from mv(cryo.y,88.9550)
    x_offset = -0.014
    c = 0
    #yield from mv(cryo.x,38.42)
    for i in range(-6, 21): #-15, 16
        c = c + 1
        yield from mv(cryo.z, cryo_z_init + cryo_z_step * (1 * i))
        yield from mv(cryo.x, cryo_x_init + c * x_offset)
        #yield from mv(cryo.x,cryo_x_init)
        yield from sleep(5)
        print('\n\n\t\tMoved cryo.z for i = {}\n\n'.format(i))
        yield from rel_scan([sclr],cryo.x,0,0.2,201)
  
def m4_cryo_x_vfocus():
    d11=[qem11]
    cryo_x_ini=34
    cryo_x_final=38
    cryo_x_step=0.25
    
    for i in range(0, 1+round(abs(cryo_x_ini-cryo_x_final)/cryo_x_step)):
        yield from mv(cryo.x,cryo_x_ini+i*cryo_x_step)
        yield from sleep(10)
        yield from mv(cryo.y,95.91) # to be adjusted
        yield from rel_scan([qem11],cryo.y,-2,0.2,23)
        yield from mv(cryo.y,peaks['cen']['sc_diode_1'])
        yield from sleep(10)
        yield from relative_scan(d11,cryo.y,-0.15,0.15,91)
        

def m4_m3_x():  
    d11 = [qem11]
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,3000)
    yield from mv(epu1.gap,38) #detunedyield from mv(cryo.x,33.50)
    mir4_x_init = 3.2
    extslt_hc_init = -4.106
    mir3_pit_init = -0.747875
    mir1_pit_init = 1932.537
    mir3_x_init=1.2
    mir3_x_step= 0.5
    mir3_pit_step=-0.00108 # +5.55% correction with respect to theoretical 0.00101
    extslt_hc_step=0.2857
    mir1_pit_step=4.52
    
    for i in range(0, 11):
        yield from mv(m1.pit,mir1_pit_init+mir1_pit_step*(1*i-5))
        yield from sleep(30)     
        yield from mv(m3.x,mir3_x_init+mir3_x_step*(1*i-5))
        yield from mv(extslt.hc,extslt_hc_init+extslt_hc_step*(1*i-5))
        yield from mv(m3.pit,mir3_pit_init+mir3_pit_step*(1*i-5))
        
        mir4_pit_init = -4.069
        mir4_pit_step= 0.003
        for j in range(0, 5):
            yield from mv(m4.pit,mir4_pit_init+mir4_pit_step*(1*j-2))
    
            yield from sleep(30)
            yield from mv(cryo.x,42)
            yield from mv(cryo.y,97.55)
            yield from sleep(30)
            yield from rel_scan(d11,cryo.y,0,0.4,121)
            yield from mv(cryo.y,97.0)
            yield from mv(cryo.x,37.4+0.1*(1*j-2)+0.038*(1*i-6))
            yield from sleep(30)
            yield from rel_scan(d11,cryo.x,0,0.5,121)
     

def m4_extslt_scan():
    d11 = [qem11]
    yield from mv(cryo.x,32.7)
    yield from mv(cryo.z,5.5)

    for i in range(0, 9):
        yield from mv(cryo.y,98)
        yield from mv(epu1.gap,40.9-i*0.0055*5)
        yield from sleep(10)
        yield from mv(extslt.vg,5+i*5)
        yield from sleep(10)
        yield from scan(d11,cryo.y,98,98.5,150)


    for i in range(0, 6):
        yield from mv(cryo.y,98)
        yield from mv(epu1.gap,40.64-i*0.00535*10)
        yield from sleep(10)
        yield from mv(extslt.vg,50+i*10)
        yield from sleep(10)
        yield from scan(d11,cryo.y,98,98.5,150)



def beam_profile():
    d11 = [qem11]

    yield from mv(cryo.y,97.2)

    for i in range(0, 21):
        yield from mv(cryo.x,36.7-0.07*i)
        yield from sleep(10)
        yield from mv(cryo.z,0.5+i)
        yield from sleep(10)
        yield from scan(d11,cryo.x,36.7-0.07*i,37.7-0.07*i,300)


    #yield from mv(cryo.y,97.6)

    #for i in range(0, 21):
        #yield from mv(cryo.x,36.7-0.07*i)
        #yield from sleep(10)
        #yield from mv(cryo.z,0.5+i)
        #yield from sleep(10)
        #yield from scan(d11,cryo.x,36.7-0.07*i,37.7-0.07*i,300)


    #yield from mv(cryo.x,33.5)
    
    #for i in range(0, 21):
        #yield from mv(cryo.y,97.85)
        #yield from sleep(10)
        #yield from mv(cryo.z,0.5+i)
        #yield from sleep(10)
        #yield from scan(d11,cryo.y,97.85,98.65,267)


    #yield from mv(cryo.y,98)

    #for i in range(0, 21):
        #yield from mv(cryo.x,36.7-0.07*i)
        #yield from sleep(10)
        #yield from mv(cryo.z,0.5+i)
        #yield from sleep(10)
        #yield from scan(d11,cryo.x,36.7-0.07*i,37.7-0.07*i,300)

def beam_profile_vs_cryox():
    d11 = [qem11]
    yield from mv(cryo.x,30)
    yield from mv(cryo.z,5.5)
    yield from mv(epu1.gap,40.9)

    for i in range(0, 61):
        yield from mv(cryo.y,98)
        yield from sleep(10)
        yield from mv(cryo.x,30+i*0.1)
        yield from sleep(30)
        yield from scan(d11,cryo.y,98,98.5,200)

    yield from mv(extslt.vg,30)
    yield from mv(epu1.gap,40.75)

    for i in range(0, 61):
        yield from mv(cryo.y,98)
        yield from sleep(10)
        yield from mv(cryo.x,30+i*0.1)
        yield from sleep(30)
        yield from scan(d11,cryo.y,98,98.5,200) 

def beam_profile_at_cor():
#Beam Profile with Si-blade aligned at the center of rotation of SC
    # Optics Wheel should be at 50.9 deg to have the photodiode located behind the cryostat
    yield from gcd_out()
    d11 = [qem11]
    mir4_pit_init = -4.1709
    mir4_x_init = 2.675
    mir4_y_init = 98.44
    mir3_pit_init=-0.743510
    extslt_hc_init=-5.22910
    mir4_x_step= 1
    mir4_pit_step=-0.0266 #-0.0307/4
    mir3_pit_step=0.002164 # +5.55% correction with respect to theoretical 0.00205
    extslt_hc_step=0.57
    
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,200)
    yield from mv(epu1.gap,40.7) #detuned

    for i in range(0, 25):
        yield from mv(m4.pit,mir4_pit_init+mir4_pit_step*(1*i-12))
        yield from mv(m4.x,mir4_x_init+mir4_x_step*(1*i-12))
        yield from mv(extslt.hc,extslt_hc_init+extslt_hc_step*(1*i-12))
        yield from mv(m3.pit,mir3_pit_init+mir3_pit_step*(1*i-12))

        yield from sleep(30)
        yield from mv(cryo.x,29.2)
        yield from mv(cryo.y,99.3)
        yield from sleep(30)
        yield from scan(d11,cryo.y,99.3,100.1,161)
        yield from mv(cryo.y,98.4)
        yield from mv(cryo.x,32.4)
        yield from sleep(30)
        yield from scan(d11,cryo.x,32.4,33.4,201)


def beam_profile_vs_m3x():
#Beam Profile with Si-blade aligned at the center of rotation of SC
    # Optics Wheel should be at 50.9 deg to have the photodiode located behind the cryostat
    from epics import caget, caput 
    yield from gcd_out()
    d11 = [qem11]
    mir1_pit_init=1857.5
    mir3_pit_init= -0.75975
    mir3_x_init = 1.8
    mir4_pit_init = -4.11070
    mir4_x_init = 0.3
    mir4_y_init = 98.95
    extslt_hc_init= -6.8892
    step_m3x= 1.4/4
    step_m3pit= -0.00155/4 #-0.0028647/8   
    step_m4pit= -0.0028647/4
    step_extslt_hc= 0.5998/4
    step_m1pit= 25.33/4 

    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,200)
    yield from mv(epu1.gap,40.7) #detuned

    for i in range(1, 7):
        caput('XF:02IDA-OP{Mir:1-Ax:4_Pitch}Cmd:Kill-Cmd',1 ) 
        yield from abs_set(m1.pit,mir1_pit_init+step_m1pit*(1*i+8),wait=False)
        yield from sleep(30)
        caput('XF:02IDA-OP{Mir:1-Ax:4_Pitch}Cmd:Kill-Cmd',1 )        
        yield from mv(m4.pit,mir4_pit_init+step_m4pit*(1*i+8))
        yield from mv(m3.x,mir3_x_init+step_m3x*(1*i+8))
        yield from mv(m3.pit,mir3_pit_init+step_m3pit*(1*i+8))
        yield from mv(extslt.hc,extslt_hc_init+step_extslt_hc*(1*i+8))
        
        
        yield from mv(cryo.x,29.2)
        yield from mv(cryo.y,100.00)
        yield from sleep(30)
        yield from scan(d11,cryo.y,100.00,100.70,141)
        yield from mv(cryo.y,99.0)
        yield from mv(cryo.x,32.35)
        yield from sleep(30)
        yield from scan(d11,cryo.x,32.35,33.35,201)


def beam_profile_vs_m4_surface():
#Beam Profile with Si-blade aligned at the center of rotation of SC
    # Optics Wheel should be at 50.9 deg to have the photodiode located behind the cryostat
    d11 = [qem10,qem11]
    m4slt_inb_init=10.5
    m4slt_out_init=-1.95
    step_x=0.1
        
    yield from mv(extslt.vg,10)
    yield from mv(epu1.gap,41.1) #tuned

    for i in range(1, 24):
        yield from mv(m4slt.inb,m4slt_inb_init+step_x*i)
        yield from mv(m4slt.out,m4slt_out_init+step_x*i)
        yield from sleep(10)
        yield from mv(cryo.x,18.65)
        yield from mv(cryo.y,99.0)
        yield from sleep(30)
        yield from scan(d11,cryo.y,99.0,99.5,151)
        yield from mv(cryo.y,97.0)
        yield from mv(cryo.x,21.3)
        yield from sleep(30)
        yield from scan(d11,cryo.x,21.3,23.3,401)

    yield from mv(m4slt.inb,-18)
    yield from mv(m4slt.out,18)
    yield from sleep(30)
    yield from mv(epu1.gap,40.7) #detuned
    mir4_rol_init=2.093140  #m4_rol initial value 2.59314
    step_r=0.1
    
    for i in range(0, 11):
        yield from mv(m4.rol,mir4_rol_init+step_r*i)
        yield from sleep(10)
        yield from mv(cryo.x,18.65)
        yield from mv(cryo.y,97.9)
        yield from sleep(10)
        yield from scan(d11,cryo.y,97.9,99.9,401)
        yield from mv(cryo.y,97.0)
        yield from mv(cryo.x,21.3)
        yield from sleep(10)
        yield from scan(d11,cryo.x,21.3,23.3,401)

def beam_position_vs_m4_height_v():
#Beam Profile with Si-blade aligned at the center of rotation of SC
    # Optics Wheel should be at 50.9 deg to have the photodiode located behind the cryostat
    dets = [sclr]
    m4slt_bot_init= -2.0
    step_x = 0.2

    yield from mv(m4slt.vg,0.25)
    for i in range(0, 19):
        yield from mv(m4slt.vc,m4slt_bot_init+step_x*i)
        yield from sleep(10)
        yield from scan(dets,cryo.y,90,90.1,301)

def beam_profile_vs_m4_surface_v():
#Beam Profile with Si-blade aligned at the center of rotation of SC
    # Optics Wheel should be at 50.9 deg to have the photodiode located behind the cryostat
    d11 = [qem10,qem11]
    m4slt_bot_init= 4.7250
    m4slt_top_init=-8.9750
    step_x=0.08
        
    yield from mv(extslt.vg,10)
    yield from mv(epu1.gap,41.1) #tuned

    for i in range(5, 11):
        yield from mv(m4slt.bot,m4slt_bot_init+step_x*i)
        yield from mv(m4slt.top,m4slt_top_init+step_x*i)
        yield from sleep(10)
        yield from mv(cryo.x,18.65)
        yield from mv(cryo.y,97.90)
        yield from sleep(30)
        yield from scan(d11,cryo.y,97.9,99.9,401)


def FEscan_gap_new():
    d = [qem07]
    yield from mv(feslt.hc,0)
    yield from mv(feslt.vc,0)
    yield from mv(epu1.gap,41.3)
    
 # Check Vertical Gap   
    yield from mv(feslt.hg,1.5) 
    yield from mv(feslt.vg,1.5)

    for i in range(0, 14):
        yield from mv(feslt.vg,1.5-0.1*i)
        yield from mv(pgm.en,870)
        yield from sleep(10)
        yield from scan(d,pgm.en,870,970,100)     

 # Check Horizontal Gap   
    yield from mv(feslt.hg,1.5) 
    yield from mv(feslt.vg,1.5) 

    for i in range(0, 14):
        yield from mv(feslt.hg,1.5-0.1*i)
        yield from mv(pgm.en,870)
        yield from sleep(10)
        yield from scan(d,pgm.en,870,970,100)     

# Repeat FE Slit Center Search
    yield from mv(feslt.hg,0.8) 
    yield from mv(feslt.vg,0.8) 
    yield from mv(epu1.gap,41.3)

    for i in range(0, 9):
        yield from mv(feslt.vc,0.8-0.2*i)
        for j in range(0, 9):
            yield from mv(feslt.hc,0.8-0.2*j)
            yield from mv(pgm.en,870)
            yield from sleep(10)
            yield from scan(d,pgm.en,870,970,100) 


    yield from mv(feslt.hc,0.5)
    yield from mv(feslt.vc,0.738)
    yield from mv(epu1.gap,41.3)
    
 # Check Vertical Gap   
    yield from mv(feslt.hg,1.5) 
    yield from mv(feslt.vg,1.5)

    for i in range(0, 14):
        yield from mv(feslt.vg,1.5-0.1*i)
        yield from mv(pgm.en,870)
        yield from sleep(10)
        yield from scan(d,pgm.en,870,970,100)     

 # Check Horizontal Gap   
    yield from mv(feslt.hg,1.5) 
    yield from mv(feslt.vg,1.5) 

    for i in range(0, 14):
        yield from mv(feslt.hg,1.5-0.1*i)
        yield from mv(pgm.en,870)
        yield from sleep(10)
        yield from scan(d,pgm.en,870,970,100)    



def epu_calib_gs_phase_pm28p5_0mm_new():

    d=[qem07]
    #Using Gas Cell Grid as detector

    yield from mv(gc_diag,-95.4)
    
    #################
    # Phase -28.5mm #
    #################
    yield from mv(epu1.phase, -28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from mv(feslt.hg,1.5)
    yield from mv(feslt.vg,1.5)
    yield from mv(pgm.cff,2.330)

    #1st Harmonic at 320 eV
    yield from mv(pgm.en,320,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,30)
    yield from mv(epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,50)

    #1st Harmonic
    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,3,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)

    for i in range(450,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,6,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)
    
    yield from sleep(100)
    #3rd Harmonic
    for i in range(1000,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-0.5)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,1.0,75)


    #################
    # Phase 0.0 mm  #
    #################

    yield from mv(epu1.phase, 0)

    #FE slit H and V gap to 1.2 mm
    yield from mv(feslt.hg,1.5)
    yield from mv(feslt.vg,1.5)
    yield from mv(pgm.cff,2.330)

    #160 eV
    yield from mv(pgm.en,160,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,75)
    yield from mv(pgm.en,160,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,75)

    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,6,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)

    yield from sleep(100)
    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,4,40)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-0.5)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,1.0,75)


    #################
    # Phase 28.5mm  #
    #################
    yield from mv(epu1.phase, 28.5)
    
    #FE slit H and V gap to 1.2 mm
    yield from mv(feslt.hg,1.5)
    yield from mv(feslt.vg,1.5)
    yield from mv(pgm.cff,2.330)

    #1st Harmonic at 320 eV
    yield from mv(pgm.en,320,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,30)
    yield from mv(epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,50)

    #1st Harmonic
    for i in range(350,401,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-1.4-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,3,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)

    for i in range(450,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-3-7.8 -(i-350)*0.0067)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,6,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)
    
    yield from sleep(100)
    #3rd Harmonic
    for i in range(1000,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-0.5-8-(i-1000)*0.0027)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-0.5)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,1.0,75)

def epu_calib_gs_phase_0mm_Mar2018():

    d=[qem07]
    #Using Gas Cell Grid as detector

    yield from mv(gc_diag,-95.4)
    
    #################
    # Phase 0.0 mm  #
    #################

    yield from mv(epu1.phase, 0)

    #FE slit H and V gap to 1.2 mm
    yield from mv(feslt.hg,1.5)
    yield from mv(feslt.vg,1.5)
    yield from mv(pgm.cff,2.330)

    #160 eV
    yield from mv(pgm.en,160,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,75)
    yield from mv(pgm.en,160,epu1.gap,17.05)
    yield from sleep(10)
    yield from relative_scan(d,epu1.gap,0,1,75)

    for i in range(200,1351,50):
        calc_gap=e2g(i)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-3)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,6,30)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-1)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,2,100)

    yield from sleep(100)
    #600-1550 eV, 3rd harmonic
    for i in range(600,1601,50):
        calc_gap=e2g(i/3)
        yield from mv(pgm.en,i,epu1.gap,calc_gap-2)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,4,40)
        yield from mv(epu1.gap,peaks['max']['gc_diag_grid'][0]-0.5)
        yield from sleep(10)
        yield from relative_scan(d,epu1.gap,0,1.0,75)

#def alignM3x():
#    # get the exit slit positions to return to at the end
#    vg_init = extslt.vg.user_setpoint.value
#    hg_init = extslt.hg.user_setpoint.value
#    hc_init = extslt.hc.user_setpoint.value
#    print('Saving exit slit positions for later')
    
#    # get things out of the way
#    yield from m3diag.out
#    # read gas cell diode
#    yield from gcdiag.grid

#    # set detector e.g. gas cell diagnostics qem
#    detList=[qem07]
#    # set V exit slit value to get enough signal
#    yield from mv(extslt.vg, 30)
#    # open H slit full open
#    yield from mv(extslt.hg, 9000)

#    #move extslt.hs appropriately and scan m3.x
#    yield from mv(extslt.hc,-9)
#    yield from relative_scan(detList,m3.x,-6,6,61)

#    yield from mv(extslt.hc,-3)
#    yield from relative_scan(detList,m3.x,-6,6,61)

#    yield from mv(extslt.hc,3)
#    yield from relative_scan(detList,m3.x,-6,6,61)
    
#    print('Returning exit slit positions to the inital values')
#    yield from mv(extslt.hc,hc_init)
#   yield from mv(extslt.vg, vg_init, extslt.hg, hg_init)

def detectorz():
    yield from mv(rixscam.cam.acquire_time,480)
    yield from count([rixscam])
    f_string = ''
    for i in range (0,75,1):
        yield from mvr(dc.z,-5)
        yield from count([rixscam],md = {'reason':'carbon-tape dc_z scans'})
        x_val = db[-1].table('baseli5.24235')['dc_z'][1]
        f_string = 'scan no ' + str(db[-1].start['scan_id']) + ': dc_z = ' + str(x_val) + \
                    ' , i = ' + str(i) + '\n'
        print(f_string)
    yield from mv(shutter_B,'Close')
    yield from count([rixscam])
    yield from count([rixscam],md = {'reason':'carbon-tape dc_z scans DARK'})
    yield from mv(dc.z, 260) # return to nominal value
	
def detectorvexit():
    yield from mv(rixscam.cam.acquire_time,600)
    yield from count([rixscam])
    f_string = ''
    for i in range (0,4,1):
        yield from mvr(extslt.vg,-10)
        yield from count([rixscam],md = {'reason':'carbon-tape extslt.vg scans'})
        x_val = db[-1].table('baseline')['extslt_vg'][1]
        f_string = 'scan no ' + str(db[-1].start['scan_id']) + ': extslt_vg = ' + str(x_val) + \
                    ' , i = ' + str(i) + '\n'
        print(f_string)
    yield from mv(shutter_B,'Close')
    yield from count([rixscam])
    yield from count([rixscam],md = {'reason':'carbon-tape extslt_vg scans DARK'})
    yield from mv(extslt.vg, 50) # return to nominal value



def temp_eq(templimit=1,checktime=5):
    deltaT = stemp.temp.B.T.value - stemp.ctrl2.setpoint.value # for control. sample is temp.b.value
    i=0
    print('Temperature of cryostat equilibrating...\n')
    while (abs(deltaT)>templimit):
        sys.stdout.write('\r')
        sys.stdout.write("\tDeviation of %3.2f K to be within +/- %3.2f K after %d s." % (deltaT,templimit,checktime*i))
        sys.stdout.flush()
        i=i+1
        deltaT = stemp.temp.B.T.value - stemp.ctrl2.setpoint.value
        yield from sleep(checktime)
        



def beam_profile_vs_cryoz():
    for i in range(0, 31):
        yield from mv(cryo.z,0.1+i*0.1)
        yield from sleep(10)
        yield from rel_scan([sclr],cryo.y,0,0.08,51)



    
