from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
import time


#CUSTOM UTILITIES FOR 2-ID BEAMLINE

###scan info utilities###
def scan_info(scan_id,source='all'):
    ''' 
    Prints to the command line, in a human readable way, the header and/or baseline info for the scan defined by scan_id.
            
    Parameters
    ----------
    scan_id : integer
        The scan_id, or the location form latest scan_id using -1,-2......, to print data from
    source : string, optional
        The source to display info from: can be 'all', 'header' (for header info) or 'baseline' (for baseline info). is 'All' by default.
        
    '''

    if source in ['all','baseline','header']:
        hdr=db[scan_id]
        f_string='*************************************************************************\n'
        f_string+='SCAN NUMBER '+str(hdr.start['scan_id'])+' INFORMATION \n'
        f_string+='*************************************************************************\n\n'        


        if source == 'all' or source == 'header':
            f_string+='HEADER INFORMATION\n------------------\n'
            f_string+='    START INFORMATION\n-----------------\n'
            for key in list(hdr.start.keys()): 
                if key == 'time':
                    f_string+='        time'.ljust(20)+' :'.ljust(4)+str(datetime.datetime.fromtimestamp(hdr.start['time']).strftime('%c'))+'\n'
                elif key != 'scan_id' and key != 'plan_args':
                    f_string+='        '+key.ljust(20)+' :'.ljust(4)+str(hdr.start[key])+'\n'

            f_string+='    STOP INFORMATION\n-----------------\n'
            for key in list(hdr.stop.keys()): 
                if key == 'time':
                    f_string+='        time'.ljust(20)+' :'.ljust(4)+str(datetime.datetime.fromtimestamp(hdr.stop['time']).strftime('%c'))+'\n'
                elif key != 'scan_id' and key != 'plan_args':
                    f_string+='        '+key.ljust(20)+' :'.ljust(4)+str(hdr.stop[key])+'\n'
        
        if source == 'all' or source == 'baseline':
            BL = hdr.table(stream_name='baseline')
            f_string+='BASELINE INFORMATION\n------------------\n'
            
            exit_val=0
            
            keys = list(BL.keys())
            while len(keys) > 0 and exit_val <=50:
                exit_val+=1
                if keys[0] == 'time':
                    device = keys[0]
                else:
                    device = keys[0].partition('_')[0]
                f_string+='    '+str(device)+'\n-----------\n'
                device_keys = list(key for key in keys if key.startswith(device))
                for key in device_keys:

                    f_string+='        '+key.ljust(30)+' start val : '+str(BL[key][1]).ljust(30)+' stop val : '+str(BL[key][2])+'\n'

                keys = list(key for key in keys if not key.startswith(device))
                    
        print (f_string)
  
    else:
        print ('source must be "all", "header" or "baseline"')


###plan time utilities###
def current_plan_time(start_scan_id,total_num_scans):
    ''' 
    For plans that involve multiple seperate scans this determines the expected finishing time, based on the time taken so far and the total number of scans.

    It assumes that all scans will take the same amount of time. So it will be less accurate when a plan involves scans of different length and will be more 
    accurate the more scans have already taken place.

    It can be added to scan plans to print out the time taken and the time left after each 'scan', this requires the lines below just before the first scan to 
    define the start scan id:

    #ADD THIS LINE AT START OF PLAN OUTSIDE ANY LOOPS
        start_scan_id=None
        total_num_scans=XXXX

    #THE FIRST SCAN SHOULD HAVE THE FOLLOWING IN FRONT OF THE YIELD FROM.
        uid_id=yield from 'first scan in plan (can be inside a loop)'
    
    #THE FIRST SCAN SHOULD AVE THE FOLLOWING AFTER THE FIRST SCAN YIELD FROM.
        if uid is not None and start_scan_id is None:
            start_scan_id = db[uid].start['scan_id']

    #THE FOLLOWING SHOULD BE PLACED AFTER EACH SCAN IN THE PLAN TO PRINT OUT THE TIME TAKEN AND TIME REMAINING.
        if start_scan_id is not None: current_plan_time(start_scan_id,total_num_scans)


    Parameters
    ----------
    start_scan_id : integer
        The scan_id for the first scan.
    total_num_scans : integer
        The total number of scans in the plan.

        
    '''
    if int(start_scan_id) < db[-2].start['scan_id']:
        time_taken = (db[-2].stop['time'] - db[int(start_scan_id)].start['time'])
        scans_complete = (db[-2].start['scan_id'] - int(start_scan_id))
        scans_remaining = total_num_scans - scans_complete
        time_per_scan = time_taken/scans_complete
        time_remaining = scans_remaining*time_per_scan-(time.time()-db[-2].stop['time'])
        estimated_completion_time = time.time() + time_remaining
    
        print ('Completed scan {} of {}, time taken = {}, average time per scan = {}'.format(scans_complete,total_num_scans, 
                             time.strftime('%H:%M:%S',time.gmtime(time_taken)), time.strftime('%H:%M:%S',time.gmtime(time_per_scan))))
        print ('Remaining time = {}, estimated completion at {}'.format(time.strftime('%H:%M:%S',time.gmtime(time_remaining)), 
                                                                    time.strftime('%d %b %Y %X',time.localtime(estimated_completion_time))))

    else:
        print ('not enough completed scans to estimate time')
    


### detector utilities ##

def scan_dets(*scan_no):
    '''Enter scan id numbers to print settings for primary stream detectors'''
    xtr_str = ''
    for scan in scan_no:
        if 'reason' in db[scan].start:
            xtr_str = '   ' + db[scan].start['reason']
        elif 'purpose' in scan.start:
            xtr_str = '   ' + db[scan].start['purpose']
        print('Scan ID {}:  {}'.format(scan, xtr_str) )
        for detector in db[scan]['start']['detectors']:
            print('  {} (primary stream):  '.format(detector) )
            settings = db[scan].config_data(detector)['primary'][0]
            for p, n in settings.items():
                print('    {:_<30} : {:_>20}'.format(p, n))
            print('{:-<70}'.format('-'))
