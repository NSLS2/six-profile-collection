from ophyd.quadem import QuadEM, QuadEMPort


from ophyd import (ProsilicaDetector, SingleTrigger, TIFFPlugin,
                   ImagePlugin, StatsPlugin, DetectorBase, HDF5Plugin,
                   AreaDetector, EpicsSignal, EpicsSignalRO, ROIPlugin,
                   TransformPlugin, ProcessPlugin, Signal, Kind)
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV, ADBase
from ophyd.areadetector.plugins import HDF5Plugin_V22

start_time=time.monotonic()


class HDF5PluginWithFileStore(HDF5Plugin_V22, FileStoreHDF5IterativeWrite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In CSS help: "N < 0: Up to abs(N) new directory levels will be created"
        self.stage_sigs.update({"create_directory": -3})
        self.stage_sigs.move_to_end("create_directory", last=False)

    def get_frames_per_point(self):
        return self.parent.cam.num_images.get()  # HACK fixed from =1 to this self.


#ALL OF THIS COMMENT DOWN TO testing m3_diag_cam is for testing only. DON'T DELETE 

class StandardProsilica(SingleTrigger, ProsilicaDetector):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for n in [1, 5]:
            stats = getattr(self, f'stats{n}')
            stats.kind |= Kind.normal
            stats.total.kind = Kind.hinted
        
    #image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, 'Stats1:')
    stats2 = Cpt(StatsPlugin, 'Stats2:')
    stats3 = Cpt(StatsPlugin, 'Stats3:')
    stats4 = Cpt(StatsPlugin, 'Stats4:')
    stats5 = Cpt(StatsPlugin, 'Stats5:')
    #trans1 = Cpt(TransformPlugin, 'Trans1:')
    roi1 = Cpt(ROIPlugin, 'ROI1:')
    roi2 = Cpt(ROIPlugin, 'ROI2:')
    roi3 = Cpt(ROIPlugin, 'ROI3:')
    roi4 = Cpt(ROIPlugin, 'ROI4:')
    #proc1 = Cpt(ProcessPlugin, 'Proc1:')



class StandardProsilicaROI(StandardProsilica):
    '''
    A class that is used to add the attributes 'roi_enable', 'roi_set', 'roi_read' and the group ('roiN_minM', roiN_sizeM) 
    where N is 1-4 and M is x,y or z. to a camera with the roi plugin enabled.
    '''    

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        for i in range(1, 4):
            for axis in ['x','y','z']:
                setattr(self,'roi{}_min{}'.format(i, axis),
                        getattr(self, 'roi' + str(i) + '.min_xyz.min_{}'.format(axis)))
                setattr(self,'roi{}_size{}'.format(i, axis),
                        getattr(self, 'roi' + str(i) + '.size.{}'.format(axis)))
    
    
    def roi_set(self,min_x, size_x, min_y, size_y, min_z=None, size_z=None, roi_num=1):
        ''' 
        An attribute function for the camera that allows the user to set an roi size and position. setting
        any of the values to 'None' means they are ignored(left as is).

        TODO add a 'set' method tothe ROIPlugin class to supprt 'cam.roi1.set(...)'
            
        Parameters
        ----------
        min_x : integer
            The pixel number position of the left edge of the ROI.
        size_x : integer
            The pixel number width of the ROI.

        min_y : integer
            The pixel number position of the bottom edge of the ROI.
        size_y : integer
            The pixel number height of the ROI.

        min_z : integer,optional
            The pixel number minima of the intensity region of the ROI.
        size_z : integer,optional
            The pixel number maxima of the intensity region of the ROI.

        roi_num : integer, optional
            The roi number to act, default is 1 and it must be 1,2,3 or 4.        
        '''

        if min_x is not None:
            getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_x').put(min_x)
        if size_x is not None:
            getattr(self, 'roi' + str(roi_num) + '.size.x').put(size_x)
        if min_y is not None:
            getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_y').put(min_y)
        if size_y is not None:
            getattr(self, 'roi' + str(roi_num) + '.size.y').put(size_y)
        if min_z is not None:
            getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_z').put(min_z)
        if size_z is not None:
            getattr(self, 'roi' + str(roi_num) + '.size.z').put(size_z)

    def roi_read(self, roi_num=1):
        ''' 
        An attribute function for the camera that allows the user to read the current values of  
        an roi size and position.

        Usage hints: to extract a specific value use "cam_name.roi_read()['keyword']" where 'keyword'
        is min_x, size_x, min_y, size_y, min_z, size_z or status.        
            
        Parameters
        ----------
        
        roi_num : integer, optional
            The roi number to act, default is 1 and it must be 1,2,3 or 4.  
        
        roi_dict : output
            A dictionary which gives the current roi positions in the form: 
            {'min_x':value,'size_x':value,'min_y':value,'size_y':value,'min_z':value,'size_z':value,'status':status}
        '''
        roi_dict={'min_x' : getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_x').get(),
                  'size_x': getattr(self, 'roi' + str(roi_num) + '.size.x').get(),
                  'min_y': getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_y').get(),
                  'size_y': getattr(self, 'roi' + str(roi_num) + '.size.y').get(),
                  'min_z' : getattr(self, 'roi' + str(roi_num) + '.min_xyz.min_z').get(),
                  'size_z' : getattr(self, 'roi' + str(roi_num) + '.size.z').get(),
                  'status' : getattr(self, 'roi' + str(roi_num) + '.enable').get()}
        
        return roi_dict

    def roi_enable(self, status, roi_num=1):
        ''' 
        An attribute function for the camera that allows the user to enable or disable an ROI.
      
            
        Parameters
        ----------
        
        status : string
            The string indicating the status to set for the ROI, must be 'Enable' or 'Disable'.
        
        roi_num : integer, optional
            The roi number to act, default is 1 and it must be 1,2,3 or 4.    
        '''   

        if status is 'Enable' or status is 'Disable':
            getattr(self, 'roi' + str(roi_num) + '.enablE').set(status)
        else:
            raise RuntimeError('in roi_enable status must be Enable or Disable')


class StandardProsilicaSaving(StandardProsilicaROI):
    hdf5 = Cpt(HDF5PluginWithFileStore,
              suffix='HDF1:',
              write_path_template='/nsls2/data/six/legacy/prosilica/%Y/%m/%d',
              root='/nsls2/data/six/legacy')


diagon_h_cam = StandardProsilicaROI('XF:02IDA-BI{Diag:1-Cam:H}', name='diagon_h_cam')
diagon_v_cam = StandardProsilicaROI('XF:02IDA-BI{Diag:1-Cam:V}', name='diagon_v_cam')
m3_diag_cam = StandardProsilicaSaving('XF:02IDC-BI{Mir:3-Cam:13_U_1}', name='m3_diag_cam')
extslt_cam = StandardProsilicaSaving('XF:02IDC-BI{Slt:1-Cam:15_1}', name='extslt_cam')
gc_diag_cam = StandardProsilicaSaving('XF:02IDC-BI{Mir:4-Cam:18_1}', name='gc_diag_cam')
#gc_diag_cam = StandardProsilicaROI('XF:02IDC-BI{Mir:4-Cam:18_1}', name='gc_diag_cam')
sc_navitar_cam = StandardProsilicaSaving('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')
#sc_navitar_cam = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')
sc_3  = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_3}', name='sc_3')
sc_4  = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_4}', name='sc_4')
#sc_5  = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_5}', name='sc_5')
#sc_navitar_cam = StandardProsilica('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')
sc_questar_cam = StandardProsilicaSaving('XF:02IDD-BI{SC:1-Cam:S1_1}', name='sc_questar_cam')

#####just commenting out this portion to see if it is breaking the ability to use the camera as a det
for cam in [diagon_v_cam, diagon_h_cam, m3_diag_cam, extslt_cam, gc_diag_cam,sc_navitar_cam, sc_3,sc_4]:#,sc_5]:
    sts_readattrs = ['mean_value', 'sigma', 'min_value', 'max_value', 'total']  #TODO do we need all of these for general case?sudo -u csstudio sh -c "cd /opt/css/opi/production/cs-studio-xf; git pull"
    cam.read_attrs = ['stats{}'.format(j) for j in range(1, 6)]
    # If this camera has 'saving' (HDF5 plugin) set up, do some extra things:
    if hasattr(cam, 'hdf5'):
        cam.read_attrs.append('hdf5')
        cam.hdf5.read_attrs = []
    cam.configuration_attrs.append('cam.acquire_time')
    for j in range(1, 5):
        st = getattr(cam, 'stats{}'.format(j))
        st.nd_array_port.set('ROI{}'.format(j))
        st.read_attrs = sts_readattrs
    cam.stats5.read_attrs = sts_readattrs


#####try instead
#m3_diag_cam = StandardCam('XF:02IDC-BI{Mir:3-Cam:13_U_1}', name='m3_diag_cam')


class SIXQuadEM(QuadEM):
    conf = Cpt(QuadEMPort, port_name='EM180')
    em_range = Cpt(EpicsSignalWithRBV, 'Range', string=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #for c in ['current{}'.format(j) for j in range(1, 5)]:
        #     getattr(self, c).read_attrs = ['mean_value']

        # self.read_attrs = ['current{}'.format(j) for j in range(1, 5)]
        self.stage_sigs.update([(self.acquire_mode, 'Single')  # single mode
                                ])
        self.configuration_attrs = ['integration_time', 'averaging_time','em_range','num_averaged','values_per_read']



def name_qem(qem, chan_name):
    read_attrs = []
    for j, n in enumerate(chan_name):
        current = getattr(qem, f'current{j+1}')
        current.mean_value.name = n
        current.kind |= Kind.normal
        current.mean_value.kind |= Kind.normal
        read_attrs.append(f'current{j+1}.mean_value')
    qem.read_attrs = read_attrs
    return qem

#qem01 = name_qem(SIXQuadEM('XF:02IDA-BI{EM:1}EM180:', name='qem01'),
#                 ['m1slt_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

qem02 = name_qem(SIXQuadEM('XF:02IDB-BI{EM:2}EM180:', name='qem02'),
                 ['pgmslt_u_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

qem03 = name_qem(SIXQuadEM('XF:02IDB-BI{EM:3}EM180:', name='qem03'),
                 ['pgmslt_d_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

qem04 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:4}EM180:', name='qem04'),
                 ['m3slt_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

qem05 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:5}EM180:', name='qem05'),
                 ['m3_diag_{}'.format(s) for s in ('diode', 'grid')])

qem06 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:6}EM180:', name='qem06'),
                 ['extslt_{}_tey'.format(s) for s in ('hdsl', 'hdsr')])

qem07 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:7}EM180:', name='qem07'),
                 ['gc_diag_{}'.format(s) for s in ('diode', 'empty', 'grid')])

qem08 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:8}EM180:', name='qem08'),
                 ['rs_diag_{}_tey'.format(s) for s in ('1','2')])

qem09 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:9}EM180:', name='qem09'),
                 ['m4slt_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

#qem10 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:10}EM180:', name='qem10'),
#		 ['m4_mir'])
#                 ['m4'.format(s) for s in ('mir')])

qem11 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:11}EM180:', name='qem11'),
                 ['sc_diode_{}'.format(s) for s in ('1','2','3','4')])

#JPcommented this 20210426
#qem12 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:12}EM180:', name='qem12'),
#                 ['sample_tey_{}'.format(s) for s in ('top','empty','bot')])

# qem07.hints = {'fields': ['gc_diag_grid', 'gc_diag_diode']}
qem07.current1.mean_value.kind = Kind.hinted
qem07.current3.mean_value.kind = Kind.hinted
qem07.current2.mean_value.kind = Kind.normal
qem07.read_attrs = ['current1.mean_value', 'current3.mean_value']
#qem12.hints = {'fields': ['sample_tey_top', 'sample_tey_bot']}

#JP commented this 20210426
#qem12.read_attrs = ['current1.mean_value', 'current3.mean_value']
#qem12.current1.mean_value.kind = Kind.hinted
#qem12.current3.mean_value.kind = Kind.hinted



start_time=time.monotonic()
