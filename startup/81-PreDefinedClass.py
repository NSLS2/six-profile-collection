from ophyd import EpicsMotor,Device
import collections
import time



class PreDefinedPositions(Device):
    '''
    A class that is used to create a diagnostic unit and/or a single axis mask units. The
    class has the axis as an attribute as well as a series of pre-defined 'locations'. It also 
    allows motion between these locations via 'paths' defined by the optional keyword dictionary
    neighbours. If neighbours is not none it will define the shortest path between the current 
    location and the requested location moving only from a location to it's 'neighbours'.
    
    Parameters
    ----------
    self : numerous paramters
        All of the parameters associated with the parent class 'Device'
    locations : dictionary
        A keyword:Value dictionary that lists all of the predefined locations (keyword) and a 
        list of axis-value pairs to be set in this location in the form: 
        {location1:['axis1_name',value1,axis2_name',value2,...], 
            location2:['axis1_name',value1,axis2_name',value2,...],.....}.
            NOTE: Not all axes need to have a specifed value for each device location, only 
            those with a specifed value are moved/checked for a given location. 
    in_band : float or dictionary
        A float that gives the in-band range for all axes when deciding if the device is 'in' the 
        correct location or not. The default value is 0.1. The optional keyword:value dictionary 
        that lists all of the predefined locations (keyword) and a sub-dictionary that has axis_name
        keywords and [min_val,max_val] values denoting the range of values for this location and 
        axis. This dictionary has the form: 

            {location1:{'axis1_name':[axis1_min_val,axis1_max_val],
                                                   'axis2_name':[axis2_min_val,axis2_max_val],...}, 
            location2:{'axis1_name':[axis1_min_val,axis1_max_val],
                                                   'axis2_name':[axis2_min_val,axis2_max_val],...},
                                          ....}.
            NOTE: All axes defined with a value in 'locations', for a given location, must have a 
            range in this dictionary for the given location, unless the 'value' in location is a 
            string.

    cam_list : list
        A list of cameras associated with this device, they will be accesible via the attribute
        cam or cam1,cam2 etc.
    qem_list : list
        A list of qem's associated with this device, they will be accesible via the attribute
        qem or qem1,qem2 etc.
    gv_list : list
        A list of gv's associated with this device, they will be accesible via the attribute
        gv or gv1,gv2 etc.

    NOTES ON PREDEFINED MOTION WITH NEIGHBOURS:
    1. The locations dictionary can include gate valves and/or parameter sets as axes with the 
        value being 'string'.
    2. To ensure the motion to a predefined location always occurs when using neighbours to define
        motion 'paths' it is best to ensure that the device is always in a 'location' by making sure
        that motion can not move the device outside of all 'locations'.
    3. Devices can be in more than one location at a time.
    4. To ensure that motion occurs always via a path then each 'point' in the path should be a 
        location, and it should only have the neighbours that are before or after it in the required
        path.
    '''
    def __init__(self, *args, locations=None, neighbours=None,in_band=0.1, cam_list=None, 
            qem_list=None, gv_list=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.locations = locations
        self.in_band = in_band
        self.neighbours = neighbours
        if isinstance(cam_list,list):
            print (cam_list)
            if len(cam_list)==1:
                self.cam=cam_list[0]
            else:
                for i,cam in enumerate(cam_list):
                    setattr(self,'cam{}'.format(i+1),cam_list[i])                

        if isinstance(qem_list,list): 
            if len(qem_list)==1:
                self.qem=qem_list[0]
            else:
                for i,qem in enumerate(qem_list):
                    setattr(self,'qem{}'.format(i+1),qem_list[i])  

        if isinstance(gv_list,list): 
            if len(gv_list)==1:
                self.gv=gv_list[0]
            else:
                for i,gv in enumerate(gv_list):
                    setattr(self,'qem{}'.format(i+1),gv_list[i])  



        def mv_axis(to_location):
            '''
            A function that moves the diagnostic or single axis slit to the location defined by 
            'value'
    
            Parameters
            ----------
            to_location: string
                The name of the location that it is required to move too.
            '''
            
            setattr(self,to_location,mv_axis(to_location))#this resolves an issue with the definition
                                                          #being set to None after a call 
            
            path_list = self.find_path(to_location)
            if path_list == 'unknown starting location':#if the current location is unknown
                print ('current location is not pre-defined, move to predefined position first')
                print ('a list of locations and axis values can be found using the "locations"')
                print ('attribute, e.g. device.locations')
            else:
                for location in path_list:
                    print ('Move to "{}"'.format(location))
                    axis_value_list=self.get_axis_value_list(location)
                    yield from mv(*axis_value_list)
                    


        for location in self.locations:#define the position attributes
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

        out_dict = collections.OrderedDict()
        out_dict[self.name+'_location'] = {'timestamp':time.time(),'value':self.status }

        read_dict = super().read()
        read_dict.update(out_dict)
        
        return read_dict

    
    
    def describe(self):
        '''
        An attribute that returns the current 'location'description of the output data as an 
        ordered dictionary. This is used identically to the describe attribute function for a 
        standard device and therefore can be used in the baseline.
        
        Parameters
        ----------
        describe_dict: ordered dictionary, ouput
            The output dictionary that matches the standard output for a Device.
        '''

        out_dict = collections.OrderedDict()
        out_dict[self.name+'_location'] = {'dtype': 'string',
               'lower_ctrl_limit': None,
               'precision': None,
               'shape': [],
               'source': 'None',
               'units': None,
               'upper_ctrl_limit': None}
              
        describe_dict = super().describe()
        describe_dict.update(out_dict)
        
        return describe_dict



    def get_axis_value_list(self,location):
        '''
        Returns the axis-value list for a defined location
        
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
        


    def find_path(self, to_location):
        '''
        This function returns the shortest path between the current location and the to_location.
        If it returns None then no path was found.
        NOTE: if the current location is unknown then it returns 'unknown starting location'.
        Parameters
        ----------
        to_location: string
            The ending location for the required path.

        Returns
        -------
        path_list, list
            A list of strings containing the names of the locations that the path should take. If 
            it is None when no path was found and returns "unknown starting location" if the current
            position is not a predefined location.

        '''
        path_list=None
        for from_location in self.status_list:
            new_path_list=find_path_default(from_location, to_location,self.neighbours)
            if new_path_list is not None:
                if path_list is None:
                    path_list = new_path_list
                elif new_path_list != 'unknown starting location' and \
                            path_list == 'unknown starting location':
                    path_list = new_path_list
                else:
                    min([path_list,new_path_list], key=len)

        return path_list 


    @property
    def status_list(self):
        '''The current locations of the device as a list
        
        Returns
        -------
        position : list
        '''
        loc_list=['unknown location']
        for location in self.locations:
            in_position=True
            for i in range(0,len(self.locations[location]),2):
                axis = self.locations[location][i]
                value = self.locations[location][i+1]

                if hasattr(getattr(self,axis),'position'):
                    if isinstance(self.in_band, float):
                        if getattr(self,axis).position < value - self.in_band or \
                            getattr(self,axis).position > value + self.in_band:
                            in_position=False
                    else:
                        if getattr(self,axis).position < self.in_band[location][axis][0] or \
                            getattr(self,axis).position > self.in_band[location][axis][1] :
                            in_position=False

                elif hasattr(getattr(self,axis),'get'):
                    if isinstance(self.in_band, float):
                        if getattr(self,axis).get() < value - self.in_band or \
                            getattr(self,axis).get() > value + self.in_band:
                            in_position=False
                    else:
                        if getattr(self,axis).get() < self.in_band[location][axis][0] or \
                            getattr(self,axis).get() > self.in_band[location][axis][1] :
                            in_position=False

                elif hasattr(getattr(self,axis),'status'):
                    if getattr(self,axis).status is not value:
                        in_position=False

            if in_position: 
                if loc_list == ['unknown location']:
                    loc_list = [location]
                else:
                    loc_list.append(location)

        return loc_list

    @property
    def status(self):
        '''The current locations of the device as a string

        Returns
        -------
        position: string

        '''
        position =''
        for location in self.status_list:
            if len(position)>1:
                position+=' , '
                
            position+= location

        return position
       


class PreDefinedPositionsGroup():
    '''
    This is a class that can be used to 'combine' a set of PreDefinedPosition devices into a 
    coherant whole. It is used in order to move to, or check a, location for all devices in the 
    group with a single command.

    Parameters
    ----------
    devices : list
        A list of devices that are to be 'combined' into a single group.
    locations : dictionary
        A keyword:Value dictionary that lists all of the predefined locations (keyword) and a 
        list of device-location list to be set in this location in the form: 
        {location1:[[device1_name,device1_location,device2_name,device2_location,...], 
            location2:[device1_name,device1_location,device2_name,device2_location,.....]}.
            NOTE: not all devices need to have a specifed location for each group location, only 
            those with a specifed location are moved/checked for a given location. 
 
    '''
    def __init__(self,devices,locations,neighbours=None,name=None):
        self.devices=devices
        self.locations=locations
        self.neighbours=neighbours
        self.name=name
        
        for device in devices:
            setattr(self,device.name,device)    
        

        def mv_axis(to_location):
            '''
            A function that moves the diagnostic or single axis slit to the location defined by 
            'value'
    
            Parameters
            ----------
            to_location: string
                The name of the location that it is required to move too.
            '''
            
            setattr(self,to_location,mv_axis(to_location))#this resolves an issue with the definition
                                                    #being set to None after a call 
            
            path_list = self.find_path(to_location)
            if path_list is None:#if no path was found to the too location.
                print ('no path between current location and requested location found')
            if path_list == 'unknown starting location':#if the current location is unknown.
                print ('current location is not pre-defined, move to predefined position first')
                print ('a list of locations and axis values can be found using the "locations"')
                print ('attribute, e.g. device.locations')
            else:
                for location in path_list:
                    print ('Move to "{}"'.format(location))
                    axis_value_list=self.get_axis_value_list(location)
                    yield from mv(*axis_value_list)
                                     


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
            out_dict[self.name+'_'+dev.name+'_location'] = {'timestamp':time.time(),
                                                            'value':dev.status }

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
            #creates a single list for all devices related to the current location.
            device = getattr(self,self.locations[location][i])
            device_location = self.locations[location][i+1]
            axis_value_list.extend(getattr(device,'get_axis_value_list')(device_location))
                    
        return axis_value_list


    def find_path(self, to_location):
        '''
        This function returns the shortest path between the current location and the to_location.
        If it returns None then no path was found.
        NOTE: if the current location is unknown then it returns 'unknown starting location'.
        Parameters
        ----------
        to_location: string
            The ending location for the required path.

        Returns
        -------
        path_list, list
            A list of strings containing the names of the locations that the path should take. If 
            it is None when no path was found and returns "unknown starting location" if the current
            position is not a predefined location.

        '''
        path_list=None
        for from_location in self.status_list:
            new_path_list=find_path_default(from_location, to_location,self.neighbours)
            if new_path_list is not None:
                if path_list is None:
                    path_list = new_path_list
                elif new_path_list != 'unknown starting location' and \
                            path_list == 'unknown starting location':
                    path_list = new_path_list
                else:
                    min([path_list,new_path_list], key=len)

        return path_list 
    
    @property
    def status_list(self):
        '''The current location of the device
        
        Returns
        -------
        position : list
        '''
        loc_list='unknown location'
        for location in self.locations:
            in_position=True
            for i in range(0,len(self.locations[location]),2):
                device = getattr(self,self.locations[location][i])
                device_location = self.locations[location][i+1]
                if device_location not in getattr(device,'location'):
                    in_position=False

            if in_position: 
                if loc_list == 'unknown location':
                    loc_list = [location]
                else:
                    loc_list.append(location)

        return loc_list


    @property
    def status(self):
        '''The current locations of the device as a string

        Returns
        -------
        position: string

        '''
        position =''
        for location in self.status_list:
            if len(position)>1:
                position+=' , '

            position+= location

        return position



def find_path_default(from_location,to_location,neighbours):
    '''
    This is a default routine that searches through the neighbours dictioanry to find the quickest
    path between 2 locations in the dictionary. It will find a path up to 7 transfers deep.

    
    Parameters
    ----------
    from_location: string
        The starting location for the required path.
    to_location: string
        The ending location for the required path.
    neighbours: dictionary
        The dictionary that list the nearest neighbours for each location.

    Returns
    -------
    path_list, list
        A list of strings contaitng the names of the locations that the path should take. If it is
        None then no path was found.

    '''

    adj_dict=neighbours
    path_list=None
    
    if neighbours is None:
        # if neighbours data is not defined just return to_location
        path_list = [to_location]

    elif from_location == 'unknown location':
        #if the current location is undefined return an error string..
        path_list='unknown starting location'

    elif to_location in adj_dict[from_location] or from_location == to_location: 
        #1 move deep
        path_list = [to_location]

    else:
        for loc1 in adj_dict[from_location]:  
            #2 moves deep
            if to_location in adj_dict[loc1]:      
                path_list = [loc1,to_location]
        
        if path_list is None:
            #3 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    if to_location in adj_dict[loc2]:
                        path_list = [loc1,loc2,to_location]
                        break
                else:
                    continue 
                break          

        if path_list is None:
            #4 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        if to_location in adj_dict[loc3]:
                            path_list = [loc1,loc2,loc3,to_location]
                            break        
                    else:
                        continue  
                    break  
                else:
                    continue 
                break  
        
        if path_list is None:
            #5 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            if to_location in adj_dict[loc4]:
                                path_list = [loc1,loc2,loc3,loc4,to_location]
                                break      
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break  
        
        if path_list is None:
            #6 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            for loc5 in adj_dict[loc4]:
                                if to_location in adj_dict[loc5]:
                                    path_list = [loc1,loc2,loc3,loc4,loc5,to_location]
                                    break      
                            else:
                                continue
                            break
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break  

        if path_list is None:
            #7 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            for loc5 in adj_dict[loc4]:
                                for loc6 in adj_dict[loc5]:
                                    if to_location in adj_dict[loc6]:
                                        path_list = [loc1,loc2,loc3,loc4,loc5,loc6,to_location]
                                        break
                                else:
                                    continue
                                break      
                            else:
                                continue
                            break
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break
     
        if path_list is None:
            #8 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            for loc5 in adj_dict[loc4]:
                                for loc6 in adj_dict[loc5]:
                                    for loc7 in adj_dict[loc6]:
                                        if to_location in adj_dict[loc7]:
                                            path_list = [loc1,loc2,loc3,loc4,loc5,
                                                        loc6,loc7,to_location]
                                            break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break      
                            else:
                                continue
                            break
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break
  
        if path_list is None:
            #9 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            for loc5 in adj_dict[loc4]:
                                for loc6 in adj_dict[loc5]:
                                    for loc7 in adj_dict[loc6]:
                                        for loc8 in adj_dict[loc7]:
                                            if to_location in adj_dict[loc8]:
                                                path_list = [loc1,loc2,loc3,loc4,loc5,
                                                        loc6,loc7,loc8,to_location]
                                                break
                                            else:
                                                continue
                                            break
                                        else:
                                            continue
                                        break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break      
                            else:
                                continue
                            break
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break

        if path_list is None:
            #10 moves deep
            for loc1 in adj_dict[from_location]:
                for loc2 in adj_dict[loc1]:
                    for loc3 in adj_dict[loc2]:
                        for loc4 in adj_dict[loc3]:
                            for loc5 in adj_dict[loc4]:
                                for loc6 in adj_dict[loc5]:
                                    for loc7 in adj_dict[loc6]:
                                        for loc8 in adj_dict[loc7]:
                                            for loc9 in adj_dict[loc8]:
                                                if to_location in adj_dict[loc9]:
                                                    path_list = [loc1,loc2,loc3,loc4,loc5,
                                                            loc6,loc7,loc8,loc9,to_location]
                                                else:
                                                    continue
                                                break
                                            break
                                        else:
                                            continue
                                        break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break      
                            else:
                                continue
                            break
                        else:
                            continue
                        break  
                    else:
                        continue  
                    break  
                else:
                    continue 
                break

 
    return path_list



