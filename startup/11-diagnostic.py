from ophyd import EpicsMotor
import collections
import time

    

class Diag_SAslit_unit(Device):
    '''
    A class that is used to create a diagnostic unit and/or a single axis slit unit. The
    class has the axis as an attribute as well as a series of pre-defined 'locations'.
    
    Parameters
    ----------
    self : numerous paramters
        All of the parameters associated with the parent class 'Device'
    locations : dictionary
        A keyword:Value dictionary that lists all of the predefined locations and axis values 
        for the instance of the class in the form {location1:value1, location2:value2,.....}.
    in_band : float
        A float that gives teh in-band range when deciding if the device is 'in' the correct 
        location or not. THe default value is 0.1.

    '''
    def __init__(self, *args, locations=None,in_band=0.1 , **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = locations
        self.in_band = in_band

        def mv_axis(axis,value,location):
            '''
            A function that moves the diagnostic or single axis slit to the location defined by 'value'
    
            Parameters
            ----------
            axis: device
                The device axis to move.
            value: float
                The value to move the axis too.

            '''
    
            yield from mv(axis,value)
            setattr(self,location,mv_axis(self.y,self.locations[location],location)) 

        for location in self.locations:
            setattr(self,location,mv_axis(self.y,self.locations[location],location)) 
             
            
    y = Cpt(EpicsMotor, '')



        
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
            if self.y.position >= self.locations[location] - self.in_band and \
                    self.y.position <= self.locations[location] + self.in_band:
                loc_value = location

        out_dict = collections.OrderedDict()
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

#    @property
#    def position(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''
#        loc_value='invalid location'
#        for location in self.locations:
#            if self.y.position >= self.locations[location] - self.in_band and \
#                    self.y.position <= self.locations[location] + self.in_band:
#                loc_value = location
#        return loc_value


    
            
m5mask = Diag_SAslit_unit('XF:02IDD-ES{Msk:Mir5-Ax:Y}Mtr',
                         locations= {'Open':54, 'Thin':34, 'Wide':21, 'Thru':8},
                         name='m5mask')

m3diag = Diag_SAslit_unit('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',
                         locations= {'Diode':-76.4, 'YAG':-49.4, 'Grid':-97.5, 'Out':-1},
                         name='m3diag')

gcdiag = Diag_SAslit_unit('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',
                         locations= {'Diode':-71.4, 'YAG':-43.4, 'Grid':-95.4, 'Out':-1},
                         name='gcdiag')

espgmmask = Diag_SAslit_unit('XF:02IDD-ES{Msk:Mono2-Ax:Y}Mtr',
                         locations= {'YAG':-43.4,'Out':0},
                         name='espgmmask')




    
m3_diag = EpicsMotor('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',name='m3_diag')

gc_diag = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',name='gc_diag')

m4_diag1 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:1}Mtr',name='m4_diag1')
m4_diag2 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:2}Mtr',name='m4_diag2')
m4_diag3 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:3}Mtr',name='m4_diag3')

m5_RPD = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:RPD}Mtr', name='m5_RPD')

SC_QPD = EpicsMotor('XF:02IDD-ES{SC:1-Ax:QPD}Mtr', name='SC_QPD')
SC_IO = EpicsMotor('XF:02IDD-ES{SC:1-Ax:IO}Mtr', name='m5_RPD')
