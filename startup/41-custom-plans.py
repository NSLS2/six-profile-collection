from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
import datetime


### CUSTOM PLANS FOR 2-ID BEAMLINE

def multi_scan(detectors,numO,motorO,startO,stopO,*args,num=None, per_step=None, md=None):
    ''' 
    Combines an 'outer_product_scan' scan with a 'scan' scan such that each  multi-motor trajectory 
    defined by '*args' is saved as a seperate experiment in databroker for point defined by numO,motorO,
    startO,stopO.
            
    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    numX : integer
        The number of points to step through for the axis not contained within each seperate experiment. 
    motorO, startO, stopO : object, float, float
        The motor axis, start and stop values for the axis not contained within each seperate experiment. 

    *args :
        For one dimension, ``motor, start, stop``.
        In general:
        .. code-block:: python
            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN
        Motors can be any 'settable' object (motor, temp controller, etc.)
    num : integer, optional
        number of points for the axes contained within each experiment, if not defiend it defaults to numX.
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        See docstring of bluesky.plan_stubs.one_nd_step (the default) for
        details.
    md : dict, optional
        metadata
    '''
    initial_uid='current_uid'
    initial_posO=motorO.position
    
    if num is None:
        num=numO
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)
        
        md=md or {}
        md.update({'plan_name':'multi_scan','multi_initial_uid':initial_uid,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})

        uid=yield from scan(detectors,*args,num, per_step=per_step, md=md)

        if initial_uid is 'current uid':
            initial_uid = uid

    yield from mv(motorO,initial_posO)
    
  
def multi_rel_scan(detectors,numO,motorO,startO,stopO,*args,num=None, per_step=None, md=None):
    ''' 
    Combines an 'outer_product_scan' scan with a 'relative_scan' scan such that each  multi-motor trajectory 
    defined by '*args' is saved as a seperate experiment in databroker for point defined by numO,motorO,
    startO,stopO.
            
    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    numX : integer
        The number of points to step through for the axis not contained within each seperate experiment. 
    motorO, startO, stopO : object, float, float
        The motor axis, start and stop values for the axis not contained within each seperate experiment, relative to the current position. 

    *args :
        For one dimension, ``motor, start, stop`` relative to the current position of motor.
        In general:
        .. code-block:: python
            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN
        Motors can be any 'settable' object (motor, temp controller, etc.)
    num : integer, optional
        number of points for the axes contained within each experiment, if not defiend it defaults to numX.
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        See docstring of bluesky.plan_stubs.one_nd_step (the default) for
        details.
    md : dict, optional
        metadata
    '''
    initial_uid='current_uid'
    initial_posO=motorO.position
    
    if num is None:
        num=numO

    startO+=motorO.position
    stopO+=motorO.position
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)        
        
        md=md or {}
        md.update({'plan_name':'multi_rel_scan','multi_initial_uid':initial_uid,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})    
        
        uid=yield from rel_scan(detectors,*args,num, per_step=per_step, md=md)

        if initial_uid is 'current uid':
            initial_uid = uid
                
    yield from mv(motorO,initial_posO)


def multi_grid_scan(detectors,motorO,startO,stopO,numO,*args,per_step=None, md=None):
    ''' 
    Combines an 'outer_product_scan' scan with a 'scan' scan such that each  multi-motor trajectory 
    defined by '*args' is saved as a seperate experiment in databroker for point defined by numO,motorO,
    startO,stopO.
            
    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    numX : integer



        The number of points to step through for the axis not contained within each seperate experiment. 
    motorO, startO, stopO : object, float, float
        The motor axis, start and stop values for the axis not contained within each seperate experiment. 

    *args
        patterned like (``motor1, start1, stop1, num1,``
                        ``motor2, start2, stop2, num2, snake2,``
                        ``motor3, start3, stop3, num3, snake3,`` ...
                        ``motorN, startN, stopN, numN, snakeN``)
        The first motor is the "slowest", the outer loop. For all motors
        except the first motor, there is a "snake" argument: a boolean
        indicating whether to following snake-like, winding trajectory or a
        simple left-to-right trajectory.
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        See docstring of bluesky.plan_stubs.one_nd_step (the default) for
        details.
    md : dict, optional
        metadata
    '''
    initial_uid='current_uid'
    initial_posO=motorO.position

        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)

        md=md or {}
        md.update({'plan_name':'multi_grid_scan','multi_initial_uid':initial_uid,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})


        uid=yield from grid_scan(detectors,*args, per_step=per_step, md=md)

        if initial_uid is 'current uid':
            initial_uid = uid

    yield from mv(motorO,initial_posO)
    
  
def multi_rel_grid_scan(detectors,motorO,startO,stopO,numO,*args,num=None, per_step=None, md=None):
    ''' 
    Combines an 'outer_product_scan' scan with a 'relative_scan' scan such that each  multi-motor trajectory 
    defined by '*args' is saved as a seperate experiment in databroker for point defined by numO,motorO,
    startO,stopO.
            
    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    numX : integer
        The number of points to step through for the axis not contained within each seperate experiment. 
    motorO, startO, stopO : object, float, float
        The motor axis, start and stop values for the axis not contained within each seperate experiment, relative to the current position. 

    *args
        patterned like (``motor1, start1, stop1, num1,``
                        ``motor2, start2, stop2, num2, snake2,``
                        ``motor3, start3, stop3, num3, snake3,`` ...
                        ``motorN, startN, stopN, numN, snakeN``)
        The first motor is the "slowest", the outer loop. For all motors
        except the first motor, there is a "snake" argument: a boolean
        indicating whether to following snake-like, winding trajectory or a
        simple left-to-right trajectory.    *args :
        For one dimension, ``motor, start, stop`` relative to the current position of motor.
        In general:
        .. code-block:: python
            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN
        Motors can be any 'settable' object (motor, temp controller, etc.)
    num : integer, optional
        number of points for the axes contained within each experiment, if not defiend it defaults to numX.
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step)
        See docstring of bluesky.plan_stubs.one_nd_step (the default) for
        details.
    md : dict, optional
        metadata
    '''
    initial_uid='current_uid'
    initial_posO=motorO.position

    num=numO

    startO+=motorO.position
    stopO+=motorO.position
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)
        
        md=md or {}
        md.update({'plan_name':'multi_rel_grid_scan','multi_initial_uid':initial_uid,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})


        uid=yield from rel_grid_scan(detectors,*args, per_step=per_step, md=md)

        if initial_uid is 'current uid':
            initial_uid = uid
                
    yield from mv(motorO,initial_posO)


#CUSTOM UTILITIES FOR 2-ID BEAMLINE

def scan_info(scan_id,source='all'):
    ''' 
    Combines an 'outer_product_scan' scan with a 'relative_scan' scan such that each  multi-motor trajectory 
    defined by '*args' is saved as a seperate experiment in databroker for point defined by numO,motorO,
    startO,stopO.
            
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
