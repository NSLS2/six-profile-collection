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
    initial_scan_id='current scan_id'
    initial_posO=motorO.position

    #initialization of time to finish variables.
    start_scan_id=None
    total_num_scans=num0
    
    if num is None:
        num=numO
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)
        
        md=md or {}
        md.update({'plan_name':'multi_scan','multi_initial_scan_id':initial_scan_id,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})

        uid=yield from scan(detectors,*args,num, per_step=per_step, md=md)

        if initial_scan_id is 'current scan_id' and uid is not None:
            initial_scan_id = db[uid].start['scan_id']
        
        if initial_scan_id is not 'current scan_id': current_plan_time(initial_scan_id,total_num_scans)

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
    initial_scan_id='current scan_id'
    initial_posO=motorO.position

    #initialization of time to finish variables.
    start_scan_id=None
    total_num_scans=num0
    
    if num is None:
        num=numO

    startO+=motorO.position
    stopO+=motorO.position
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)        
        
        md=md or {}
        md.update({'plan_name':'multi_rel_scan','multi_initial_scan_id':initial_scan_id,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})    
        
        uid=yield from rel_scan(detectors,*args,num, per_step=per_step, md=md)

        if initial_scan_id is 'current scan_id' and uid is not None:
            initial_scan_id = db[uid].start['scan_id']

        if initial_scan_id is not 'current scan_id': current_plan_time(initial_scan_id,total_num_scans)
                
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
    initial_scan_id='current scan_id'
    initial_posO=motorO.position

    #initialization of time to finish variables.
    start_scan_id=None
    total_num_scans=num0
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)

        md=md or {}
        md.update({'plan_name':'multi_grid_scan','multi_initial_scan_id':initial_scan_id,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})


        uid=yield from grid_scan(detectors,*args, per_step=per_step, md=md)

        if initial_scan_id is 'current scan_id' and uid is not None:
            initial_scan_id = db[uid].start['scan_id']

        if initial_scan_id is not 'current scan_id': current_plan_time(initial_scan_id,total_num_scans)

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
    initial_scan_id='current scan_id'
    initial_posO=motorO.position

    #initialization of time to finish variables.
    start_scan_id=None
    total_num_scans=num0

    num=numO

    startO+=motorO.position
    stopO+=motorO.position
        
        
    for i in range(numO):
            
        O=startO+i*(stopO-startO)/(numO-1)
        yield from mv(motorO,O)
        multi_position=str(i)+':'+str(numO)
        
        md=md or {}
        md.update({'plan_name':'multi_rel_grid_scan','multi_initial_scan_id':initial_scan_id,'multi_num':numO,'multi_start':startO,'multi_stop':stopO,
                   'multi_motor':motorO.name,'multi_position': multi_position,'multi_axis_value':O})


        uid=yield from rel_grid_scan(detectors,*args, per_step=per_step, md=md)

        if initial_scan_id is 'current scan_id' and uid is not None:
            initial_scan_id = db[uid].start['scan_id']

        if initial_scan_id is not 'current scan_id': current_plan_time(initial_scan_id,total_num_scans)
                
    yield from mv(motorO,initial_posO)

