from ophyd import EpicsMotor
import collections
import time

    

class PreDefinedPositions(Device):
    '''
    A class that is used to create a diagnostic unit and/or a single axis mask units. The
    class has the axis as an attribute as well as a series of pre-defined 'locations'.
    
    Parameters
    ----------
    self : numerous paramters
        All of the parameters associated with the parent class 'Device'
    locations : dictionary
        A keyword:Value dictionary that lists all of the predefined locations (keyword) and a 
        list of axis-value pairs to be set in this location in the form: 
        {location1:['axis1_name',value1,axis2_name',value2,...], 
            location2:['axis1_name',value1,axis2_name',value2,...],.....}.
            NOTE: not all axes need to have a specifed location for each device location, only those with
                  a specifed location are moved/checked for a given location. 
    in_band : float
        A float that gives teh in-band range when deciding if the device is 'in' the correct 
        location or not. THe default value is 0.1.

    '''
    def __init__(self, *args, locations=None, in_band=0.1, cam=None, qem=None , **kwargs):
        super().__init__(*args, **kwargs)

        self.locations = locations
        self.in_band = in_band

        if cam is not None: self.cam=cam
        if qem is not None: self.qem=qem

        def mv_axis(location):
            '''
            A function that moves the diagnostic or single axis slit to the location defined by 'value'
    
            Parameters
            ----------
            location: string
                The name of the location that it is required to move too.
            '''
            axis_value_list=self.get_axis_value_list(location)
        
            yield from mv(*axis_value_list)
            setattr(self,location,mv_axis(location)) 

        for location in self.locations:
            setattr(self,location,mv_axis(location))

        
        
    def read(self):
        '''
        An attribute that returns the current 'location' of the unit as an ordered dictionary. This
        is used identically to the read attribute function for a standard device and therefore can 
        be used in the baseline.
        
        Parameters
        ----------
        read_dict: ordered dictionary, ouput
            The output dictionary that matches the standard output for a Device.

        '''
        loc_value='invalid location'
        for location in self.locations:
            if self.y.position >= self.locations[location][1] - self.in_band and \
                    self.y.position <= self.locations[location][1] + self.in_band:
                loc_value = location

 #       out_dict = collections.OrderedDict()
 #       out_dict[self.name+'_location'] = {'timestamp':time.time(),'value':loc_value }

        read_dict = super().read()
        read_dict.update(out_dict)
        
        return read_dict

    
    
    def describe(self):
        '''
        An attribute that returns the current 'location'description of the output data as an ordered dictionary. 
        This is used identically to the describe attribute function for a standard device and therefore can 
        be used in the baseline.
        
        Parameters
        ----------
        describe_dict: ordered dictionary, ouput
            The output dictionary that matches the standard output for a Device.

        '''

        out_dict = collections.OrderedDict()
 #       out_dict[self.name+'_location'] = {'dtype': 'string',
 #              'lower_ctrl_limit': None,
 #              'precision': None,
 #              'shape': [],
 #              'source': None,
 #              'units': None,
 #              'upper_ctrl_limit': None}
              
        describe_dict = super().describe()
        describe_dict.update(out_dict)
        
        return describe_dict



    def get_axis_value_list(self,location):
        '''returns the axis-value list for a defined location
        
        Returns
        -------
        axis_value_list : list, output
            the axis-value list for the inputted location that is returned

        '''
        axis_value_list=[]
        for item in self.locations[location]:
                if isinstance(item,str):
                    axis_value_list.append(getattr(self,item))
                else:
                    axis_value_list.append(item)
                    
        return axis_value_list
        

    @property
    def current(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''
        loc_value='invalid location'
        for location in self.locations:
            in_position=True
            for i in range(0,len(self.locations[location]),2):
                axis = self.locations[location][i]
                value = self.locations[location][i+1]
                if getattr(self,axis).position <= value - self.in_band or \
                    getattr(self,axis).position >= value + self.in_band:
                    in_position=False
   
            if in_position: loc_value = location
            
        return loc_value




class PreDefinedPositionsGroup():
    '''
    This is a class that can be used to 'combine' a set of PreDefinedPosition devices into a coherant whole. 
    It is used in order to move to, or check a, location for all devices in the group with a single command.

    Parameters
    ----------
    devices : list
        A list of devices that are to be 'combined' into a single group.
    locations : dictionary
        A keyword:Value dictionary that lists all of the predefined locations (keyword) and a 
        list of device-location list to be set in this location in the form: 
        {location1:[[device1_name,device1_location,device2_name,device2_location,...], 
            location2:[device1_name,device1_location,device2_name,device2_location,.....]}.
            NOTE: not all devices need to have a specifed location for each group location, only those with
                  a specifed location are moved/checked for a given location. 

 
    '''
    def __init__(self,devices,locations,name=None):
        self.devices=devices
        self.locations=locations
        self.name=name
        
        for device in devices:
            setattr(self,device.name,device)    
        

        def mv_axis(location):
            '''
            A function that moves the diagnostic or single axis slit to the location defined by 'value'
    
            Parameters
            ----------
            location: string
                The name of the location that it is required to move too.
            '''
    
            axis_value_list=self.get_axis_value_list(location)
                        
            yield from mv(*axis_value_list)
            setattr(self,location,mv_axis(location))

        for location in self.locations:
            setattr(self,location,mv_axis(location))

    
    def read(self):
        '''
        An attribute that returns the current 'location' of the group as an ordered dictionary. This
        is used identically to the read attribute function for a standard device.
        
        Parameters
        ----------
        read_dict: ordered dictionary, ouput
            The output dictionary for the group.

        '''

        out_dict = collections.OrderedDict()
        for dev in self.devices:
            out_dict[self.name+'_'+dev.name+'_location'] = {'timestamp':time.time(),'value':dev.current }

        return out_dict

    
    def get_axis_value_list(self,location):
        '''returns the axis-value list for a defined location
        
        Returns
        -------
        axis_value_list : list, output
           the axis-value list for the inputted location that is returned

        '''
        axis_value_list=[]
        for i in range(0,len(self.locations[location]),2):
            device = getattr(self,self.locations[location][i])
            device_location = self.locations[location][i+1]
            axis_value_list.extend(getattr(device,'get_axis_value_list')(device_location))
                    
        return axis_value_list

    
    @property
    def current(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''
        loc_value='invalid location'
        for location in self.locations:
            in_position=True
            for i in range(0,len(self.locations[location]),2):
                device = getattr(self,self.locations[location][i])
                device_location = self.locations[location][i+1]
                if device_location != getattr(device,'current'):
                    in_position=False
   
            if in_position: loc_value = location
            
        return loc_value


    

class DiagAndSingleAxisMask(PreDefinedPositions):
    '''
    A class that is used to defien diagnostic untis and single axis mask units. It is a child of the 
    PreDefinedPositions class which allows for defining a set of pre-defined positions, in addition 
    these have a single, "y", axis that is used to move to the different locations.
    '''
    
    y = Cpt(EpicsMotor, '')






    
            
m5mask = DiagAndSingleAxisMask('XF:02IDD-ES{Msk:Mir5-Ax:Y}Mtr',
                         locations = {'open':['y',54], 'thin':['y',34], 'wide':['y',21], 'thru':['y',8]},
                         name = 'm5mask')

m3diag = DiagAndSingleAxisMask('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',
                         locations = {'diode':['y',-76.4], 'yag':['y',-49.4], 'grid':['y',-97.5], 'out':['y',-1]},
                         cam = m3_diag_cam, qem = qem05,
                         name = 'm3diag')

gcdiag = DiagAndSingleAxisMask('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',
                         locations = {'diode':['y',-71.4], 'yag':['y',-43.4], 'grid':['y',-95.4], 'out':['y',-1]},
                         cam = gc_diag_cam, qem = qem07,
                         name = 'gcdiag')

espgmmask = DiagAndSingleAxisMask('XF:02IDD-ES{Msk:Mono2-Ax:Y}Mtr',
                         locations= {'yag':['y',-43.4],'out':['y',0]},
                         cam = sc_4,
                         name='espgmmask')


diagnostics = PreDefinedPositionsGroup([m3diag,gcdiag],{'test_location':['m3diag','out','gcdiag','out']},name='diagnostics')



    
m3_diag = EpicsMotor('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',name='m3_diag')

gc_diag = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',name='gc_diag')

m4_diag1 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:1}Mtr',name='m4_diag1')
m4_diag2 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:2}Mtr',name='m4_diag2')
m4_diag3 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:3}Mtr',name='m4_diag3')

m5_RPD = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:RPD}Mtr', name='m5_RPD')

SC_QPD = EpicsMotor('XF:02IDD-ES{SC:1-Ax:QPD}Mtr', name='SC_QPD')
SC_IO = EpicsMotor('XF:02IDD-ES{SC:1-Ax:IO}Mtr', name='m5_RPD')
