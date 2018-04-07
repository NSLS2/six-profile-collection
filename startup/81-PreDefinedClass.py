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
    neighbours : Dictionary
        A keyword:value dictionary where each keyword is a location defined in 'locations' and 
        each value is a list of 'neighbours' for that location. When defined motion occurs only 
        between neighbours, for non-neighbours a path through various locations will be used, if 
        it is found using self.find_path. 
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
        


    def find_path(self,to_location):
        '''
        Find the shortest path from 'from_location' to 'to_location' passing only thorugh the 
        neighbours for each location defiend by the dictionary 'neighbours'. Returns an empty list 
        if no path found otherwise returns a list of 'locations' that define the path.

        Paramters
        ---------
        to_location: string
            The name of the ending location required for the path.
        neighbours: dictionary
            The dictionary that specifes the list of neighbours for each location in the device.
        path_list: list, output
            A list locations indicating the path to take to reach the required position.

        '''
    
    
        #Generator that calculates all possible, cycle free, paths that start at 'from_location'.
        def paths(from_location,neighbours):
            '''
            Generate the maximal cycle-free paths in neighbours starting at from_location. The output
            of the generator is a set of lists that start at the 'from_location'.
        
            Parameters
            ----------        
            from_location: string
                The name of the starting location.

            '''
            path = [from_location]                  # path traversed so far
            seen = {from_location}                  # set of vertices in path
            def search():
                dead_end = True
                for neighbour in neighbours[path[-1]]:
                    if neighbour not in seen:
                        dead_end = False
                        seen.add(neighbour)
                        path.append(neighbour)
                        yield from search()
                        path.pop()
                        seen.remove(neighbour)
                if dead_end:
                    yield list(path)
    
            yield from search()

        if self.neighbours is None:        
            return [to_location]
        elif isinstance(self.status_list,str):
            print (self.status_list)
        else:
        
            path_list=[]
            for from_location in self.status_list:
                prev_path_list=path_list
                path_list=[]
                #Start the process of finding the path
                if self.neighbours is None or to_location in self.neighbours[from_location]: 
                    #1 move deep
                    path_list = [to_location]
                else:
                    #more than 1 move deep
                    for path in paths(from_location,self.neighbours):
                        if to_location in path:
                            if len(path_list)<1:
                                path_list=path[:path.index(to_location)+1]
                            elif len(path[:path.index(to_location)+1]) < len(path_list):
                                path_list=path[:path.index(to_location)+1]

                if len(prev_path_list)>1 and len(prev_path_list)<len(path_list):
                    path_list=prev_path_list

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
                if loc_list == 'unknown location':
                    loc_list = [location]
                else:
                    loc_list.append(location)

        return loc_list
   
    @property  
    def status(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''

        if isinstance(self.status_list,list):
            position=''
            for location in self.status_list:
                if len(position)>1:
                    position+=' , '

                position+= location
        else:
            position = self.status_list

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
    neighbours : Dictionary
        A keyword:value dictionary where each keyword is a location defined in 'locations' and 
        each value is a list of 'neighbours' for that location. When defined motion occurs only 
        between neighbours, for non-neighbours a path through various locations will be used, if 
        it is found using self.find_path. 

 
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

    def find_path(self,to_location):
        '''
        Find the shortest path from 'from_location' to 'to_location' passing only thorugh the 
        neighbours for each location defiend by the dictionary 'neighbours'. Returns an empty list 
        if no path found otherwise returns a list of 'locations' that define the path.

        Paramters
        ---------
        to_location: string
            The name of the ending location required for the path.
        neighbours: dictionary
            The dictionary that specifes the list of neighbours for each location in the device.
        path_list: list, output
            A list locations indicating the path to take to reach the required position.

        '''
    
    
        #Generator that calcualtes all possible, cycle free, paths that start at 'from_location'.
        def paths(from_location,neighbours):
            '''
            Generate the maximal cycle-free paths in neighbours starting at from_location. The output
            of the generator is a set of lists that start at the 'from_location'.
        
            Parameters
            ----------        
            from_location: string
                The name of the starting location.

            '''
            path = [from_location]                  # path traversed so far
            seen = {from_location}                  # set of vertices in path
            def search():
                dead_end = True
                for neighbour in neighbours[path[-1]]:
                    if neighbour not in seen:
                        dead_end = False
                        seen.add(neighbour)
                        path.append(neighbour)
                        yield from search()
                        path.pop()
                        seen.remove(neighbour)
                if dead_end:
                    yield list(path)
    
            yield from search()

        if self.neighbours is None:        
            return [to_location]
        elif isinstance(self.status_list,str):
            print (self.status_list)
        else:
        
            path_list=[]
            for from_location in self.status_list:
                prev_path_list=path_list
                path_list=[]
                #Start the process of finding the path
                if self.neighbours is None or to_location in self.neighbours[from_location]: 
                    #1 move deep
                    path_list = [to_location]
                else:
                    #more than 1 move deep
                    for path in paths(from_location,self.neighbours):
                        if to_location in path:
                            if len(path_list)<1:
                                path_list=path[:path.index(to_location)+1]
                            elif len(path[:path.index(to_location)+1]) < len(path_list):
                                path_list=path[:path.index(to_location)+1]

                if len(prev_path_list)>1 and len(prev_path_list)<len(path_list):
                    path_list=prev_path_list

            return path_list

     
    @property
    def status_list(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''
        
        loc_list='unknown location'
        for location in self.locations:
            in_position=True
            for i in range(0,len(self.locations[location]),2):
                device = getattr(self,self.locations[location][i])
                device_location = self.locations[location][i+1]
                if device_location not in getattr(device,'status_list'):
                    in_position=False

            if in_position: 
                if loc_list == 'unknown location':
                    loc_list = [location]
                else:
                    loc_list.append(location)

        return loc_list



    @property  
    def status(self):
        '''The current location of the device
        
        Returns
        -------
        position : string
        '''
        if isinstance(self.status_list,list):
            position=''
            for location in self.status_list:
                if len(position)>1:
                    position+=' , '

                position+= location
        else:
            position = self.status_list

        return position




