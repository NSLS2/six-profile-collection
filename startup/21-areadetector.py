from ophyd.quadem import QuadEM


from ophyd import (ProsilicaDetector, SingleTrigger, TIFFPlugin,
                   ImagePlugin, StatsPlugin, DetectorBase, HDF5Plugin,
                   AreaDetector, EpicsSignal, EpicsSignalRO, ROIPlugin,
                   TransformPlugin, ProcessPlugin, Signal)
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.cam import AreaDetectorCam
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV


class HDF5PluginWithFileStore(HDF5Plugin, FileStoreHDF5IterativeWrite):

    def get_frames_per_point(self):
        return 1  # HACK


#ALL OF THIS COMMENT DOWN TO testing m3_diag_cam is for testing only. DON'T DELETE 

class StandardProsilica(SingleTrigger, ProsilicaDetector):
#class StandardCam(SingleTrigger, AreaDetector):
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

    @property
    def hints(self):
        return {'fields': [self.stats1.total.name,
                           self.stats5.total.name]}


class StandardProsilicaSaving(StandardProsilica):
    hdf5 = Cpt(HDF5PluginWithFileStore,
              suffix='HDF1:',
              write_path_template='/XF02ID1/prosilica_data/%Y/%m/%d',
              root='/XF02ID1',
              reg=db.reg)



diagon_h_cam = StandardProsilica('XF:02IDA-BI{Diag:1-Cam:H}', name='diagon_h_cam')
diagon_v_cam = StandardProsilica('XF:02IDA-BI{Diag:1-Cam:V}', name='diagon_v_cam')
m3_diag_cam = StandardProsilica('XF:02IDC-BI{Mir:3-Cam:13_U_1}', name='m3_diag_cam')
extslt_cam = StandardProsilicaSaving('XF:02IDC-BI{Slt:1-Cam:15_1}', name='extslt_cam')
gc_diag_cam = StandardProsilica('XF:02IDC-BI{Mir:4-Cam:18_1}', name='gc_diag_cam')
sc_navitar_cam = StandardProsilicaSaving('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')


#####just commenting out this portion to see if it is breaking the ability to use the camera as a det
for cam in [diagon_v_cam, diagon_h_cam, m3_diag_cam, extslt_cam, gc_diag_cam]:
    sts_readattrs = ['mean_value', 'sigma', 'min_value', 'max_value', 'total']
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
    port_name = Cpt(Signal, value='EM180')
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
    fields = []
    for j, n in enumerate(chan_name):
        nm = 'current{}.mean_value'.format(j+1)
        getattr(qem, nm).name = n
        read_attrs.append(nm)
        fields.append(n)
    qem.read_attrs = read_attrs
    qem.hints = {'fields': fields}
    return qem

qem01 = name_qem(SIXQuadEM('XF:02IDA-BI{EM:1}EM180:', name='qem01'),
                 ['m1slt_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

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

qem10 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:10}EM180:', name='qem10'),
		 ['m4_mir'])
#                 ['m4'.format(s) for s in ('mir')])

qem11 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:11}EM180:', name='qem11'),
                 ['sc_diode_{}'.format(s) for s in ('1','2','3','4')])

# Device is disconnected (physically) for now
#qem12 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:12}EM180:', name='qem12'),
#                 ['sample_tey_{}'.format(s) for s in ('top','bot')])

qem07.hints = {'fields': ['gc_diag_grid', 'gc_diag_diode']}
qem07.read_attrs = ['current1.mean_value', 'current3.mean_value']
