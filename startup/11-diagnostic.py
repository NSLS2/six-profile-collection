from ophyd import EpicsMotor


def mv_Diag_SAslit_unit(axis,value):
    '''
    A function that moves the diagnostic or single axis slit to hte location defined by 'value'
    
    Parameters
    ----------
    axis: device
        The device axis to move.
    value: float
        The value to move the axis too.

    '''
    
    yield from mv(axis,value)
    

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

    '''
    def __init__(self, *args, locations=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = locations
        for location in locations:
            setattr(self,location,mv_Diag_SAslit_unit(self.y,locations[location]))
            
                
    y = Cpt(EpicsMotor, '')


            
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
                         locations= {'YAG':-43.4},
                         name='espgmmask')




    
m3_diag = EpicsMotor('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',name='m3_diag')

gc_diag = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',name='gc_diag')

m4_diag1 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:1}Mtr',name='m4_diag1')
m4_diag2 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:2}Mtr',name='m4_diag2')
m4_diag3 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:3}Mtr',name='m4_diag3')

m5_RPD = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:RPD}Mtr', name='m5_RPD')

SC_QPD = EpicsMotor('XF:02IDD-ES{SC:1-Ax:QPD}Mtr', name='SC_QPD')
SC_IO = EpicsMotor('XF:02IDD-ES{SC:1-Ax:IO}Mtr', name='m5_RPD')
