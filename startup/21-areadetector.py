from typing import Optional, Union
import logging
from functools import reduce

import networkx as nx
from ophyd.quadem import QuadEM, QuadEMPort
from ophyd import (
    ProsilicaDetector,
    SingleTrigger,
    TIFFPlugin,
    ImagePlugin,
    StatsPlugin,
    DetectorBase,
    HDF5Plugin,
    AreaDetector,
    EpicsSignal,
    EpicsSignalRO,
    ROIPlugin,
    TransformPlugin,
    ProcessPlugin,
    Signal,
    Kind,
    OverlayPlugin,
)  # OverlayPlugin was added
from ophyd.status import SubscriptionStatus
from ophyd.areadetector.plugins import (
    PvaPlugin,
    PluginBase,
    HDF5Plugin_V22,
    CircularBuffPlugin_V34,
)
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.trigger_mixins import (
    ContinuousAcquisitionTrigger,
    TriggerStatus,
)
from ophyd.areadetector.cam import AreaDetectorCam, CamBase
from ophyd.areadetector.base import ADComponent, EpicsSignalWithRBV, ADBase
from ophyd import Component as Cpt

start_time = time.monotonic()

logger = logging.getLogger()


class HDF5PluginWithFileStore(HDF5Plugin_V22, FileStoreHDF5IterativeWrite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # In CSS help: "N < 0: Up to abs(N) new directory levels will be created"
        self.stage_sigs.update({"create_directory": -3})
        self.stage_sigs.move_to_end("create_directory", last=False)

    def get_frames_per_point(self):
        return self.parent.cam.num_images.get()  # HACK fixed from =1 to this self.

    # How did this ever work? Pre 2022C1.1 deployment, gc_diag_cam.hdf5.warmup() failed
    # def warmup(self):
    #     """
    #     A convenience method for 'priming' the plugin.
    #
    #     The plugin has to 'see' one acquisition before it is ready to capture.
    #     This sets the array size, etc.
    #     """
    #     set_and_wait(self.enable, 1)
    #     sigs = OrderedDict([(self.parent.cam.array_callbacks, 1),
    #                         (self.parent.cam.image_mode, 'Single'),
    #                         (self.parent.cam.trigger_mode, 'Fixed Rate'),
    #                         # just in case tha acquisition time is set very long...
    #                         (self.parent.cam.acquire_time, 1),
    #                         (self.parent.cam.acquire_period, 1),
    #                         (self.parent.cam.acquire, 1)])
    #
    #     original_vals = {sig: sig.get() for sig in sigs}
    #
    #     for sig, val in sigs.items():
    #         ttime.sleep(0.1)  # abundance of caution
    #         set_and_wait(sig, val)
    #
    #     ttime.sleep(2)  # wait for acquisition
    #
    #     for sig, val in reversed(list(original_vals.items())):
    #         ttime.sleep(0.1)
    #         set_and_wait(sig, val)


# ALL OF THIS COMMENT DOWN TO testing m3_diag_cam is for testing only. DON'T DELETE


class StandardProsilica(SingleTrigger, ProsilicaDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for n in [1, 5]:
            stats = getattr(self, f"stats{n}")
            stats.kind |= Kind.normal
            stats.total.kind = Kind.hinted

    # image = Cpt(ImagePlugin, 'image1:')
    stats1 = Cpt(StatsPlugin, "Stats1:")
    stats2 = Cpt(StatsPlugin, "Stats2:")
    stats3 = Cpt(StatsPlugin, "Stats3:")
    stats4 = Cpt(StatsPlugin, "Stats4:")
    stats5 = Cpt(StatsPlugin, "Stats5:")
    trans1 = Cpt(TransformPlugin, "Trans1:")  # this line was uncommendeted
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    # proc1 = Cpt(ProcessPlugin, 'Proc1:')
    trans1 = Cpt(TransformPlugin, "Trans1:")
    over1 = Cpt(OverlayPlugin, "Over1:")  # this line was added


class StandardProsilicaROI(StandardProsilica):
    """
    A class that is used to add the attributes 'roi_enable', 'roi_set', 'roi_read' and the group ('roiN_minM', roiN_sizeM)
    where N is 1-4 and M is x,y or z. to a camera with the roi plugin enabled.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(1, 4):
            for axis in ["x", "y", "z"]:
                setattr(
                    self,
                    "roi{}_min{}".format(i, axis),
                    getattr(self, "roi" + str(i) + ".min_xyz.min_{}".format(axis)),
                )
                setattr(
                    self,
                    "roi{}_size{}".format(i, axis),
                    getattr(self, "roi" + str(i) + ".size.{}".format(axis)),
                )

    def roi_set(self, min_x, size_x, min_y, size_y, min_z=None, size_z=None, roi_num=1):
        """
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
        """

        if min_x is not None:
            getattr(self, "roi" + str(roi_num) + ".min_xyz.min_x").put(min_x)
        if size_x is not None:
            getattr(self, "roi" + str(roi_num) + ".size.x").put(size_x)
        if min_y is not None:
            getattr(self, "roi" + str(roi_num) + ".min_xyz.min_y").put(min_y)
        if size_y is not None:
            getattr(self, "roi" + str(roi_num) + ".size.y").put(size_y)
        if min_z is not None:
            getattr(self, "roi" + str(roi_num) + ".min_xyz.min_z").put(min_z)
        if size_z is not None:
            getattr(self, "roi" + str(roi_num) + ".size.z").put(size_z)

    def roi_read(self, roi_num=1):
        """
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
        """
        roi_dict = {
            "min_x": getattr(self, "roi" + str(roi_num) + ".min_xyz.min_x").get(),
            "size_x": getattr(self, "roi" + str(roi_num) + ".size.x").get(),
            "min_y": getattr(self, "roi" + str(roi_num) + ".min_xyz.min_y").get(),
            "size_y": getattr(self, "roi" + str(roi_num) + ".size.y").get(),
            "min_z": getattr(self, "roi" + str(roi_num) + ".min_xyz.min_z").get(),
            "size_z": getattr(self, "roi" + str(roi_num) + ".size.z").get(),
            "status": getattr(self, "roi" + str(roi_num) + ".enable").get(),
        }

        return roi_dict

    def roi_enable(self, status, roi_num=1):
        """
        An attribute function for the camera that allows the user to enable or disable an ROI.


        Parameters
        ----------

        status : string
            The string indicating the status to set for the ROI, must be 'Enable' or 'Disable'.

        roi_num : integer, optional
            The roi number to act, default is 1 and it must be 1,2,3 or 4.
        """

        if (status == "Enable") or (status == "Disable"):
            getattr(self, "roi" + str(roi_num) + ".enablE").set(status)
        else:
            raise RuntimeError("in roi_enable status must be Enable or Disable")


class StandardProsilicaSaving(StandardProsilicaROI):
    hdf5 = Cpt(
        HDF5PluginWithFileStore,
        suffix="HDF1:",
        write_path_template=f"/nsls2/data/six/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/prosilica/%Y/%m/%d",
        root=f"/nsls2/data/six/proposals/{RE.md['cycle']}/{RE.md['data_session']}/assets/prosilica",
    )

    def describe(self):
        res = super().describe()
        try:
            is_rgb = bool(
                self.cam.color_mode.get()
            )  # 0 should be Mono, 2 should be RGB1, no kowledge of 1.
        except AttributeError:
            is_rgb == False
        data_key = self.name + "_image"
        if is_rgb and data_key in res:
            res[data_key]["shape"] = (*res[data_key]["shape"], 3)
        return res


# class StandardProsilicaSaving(StandardProsilicaROI):
#    hdf5 = Cpt(HDF5PluginWithFileStore,
#              suffix='HDF1:',
#              _template='/tmp/tempimage/%Y/%m/%d',
#              root='/tmp/')


# diagon_h_cam = StandardProsilicaROI('XF:02IDA-BI{Diag:1-Cam:H}', name='diagon_h_cam')
diagon_h_cam = StandardProsilicaSaving("XF:02IDA-BI{Diag:1-Cam:H}", name="diagon_h_cam")
diagon_v_cam = StandardProsilicaROI("XF:02IDA-BI{Diag:1-Cam:V}", name="diagon_v_cam")
m3_diag_cam = StandardProsilicaSaving(
    "XF:02IDC-BI{Mir:3-Cam:13_U_1}", name="m3_diag_cam"
)
extslt_cam = StandardProsilicaSaving("XF:02IDC-BI{Slt:1-Cam:15_1}", name="extslt_cam")
gc_diag_cam = StandardProsilicaSaving("XF:02IDC-BI{Mir:4-Cam:18_1}", name="gc_diag_cam")
# gc_diag_cam = StandardProsilicaROI('XF:02IDC-BI{Mir:4-Cam:18_1}', name='gc_diag_cam')
sc_navitar_cam = StandardProsilicaSaving(
    "XF:02IDD-BI{SC:1-Cam:S1_2}", name="sc_navitar_cam"
)
# sc_navitar_cam = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')
sc_3 = StandardProsilicaROI("XF:02IDD-BI{SC:1-Cam:S1_3}", name="sc_3")
sc_4 = StandardProsilicaROI("XF:02IDD-BI{SC:1-Cam:S1_4}", name="sc_4")
# sc_5  = StandardProsilicaROI('XF:02IDD-BI{SC:1-Cam:S1_5}', name='sc_5')
# sc_navitar_cam = StandardProsilica('XF:02IDD-BI{SC:1-Cam:S1_2}', name='sc_navitar_cam')
sc_questar_cam = StandardProsilicaSaving(
    "XF:02IDD-BI{SC:1-Cam:S1_1}", name="sc_questar_cam"
)

#####just commenting out this portion to see if it is breaking the ability to use the camera as a det
for cam in [
    diagon_v_cam,
    diagon_h_cam,
    m3_diag_cam,
    extslt_cam,
    gc_diag_cam,
    sc_navitar_cam,
    sc_3,
    sc_4,
    sc_questar_cam,
]:  # ,sc_5]:
    sts_readattrs = [
        "mean_value",
        "sigma",
        "min_value",
        "max_value",
        "total",
    ]  # TODO do we need all of these for general case?sudo -u csstudio sh -c "cd /opt/css/opi/production/cs-studio-xf; git pull"
    cam.read_attrs = ["stats{}".format(j) for j in range(1, 6)]
    # If this camera has 'saving' (HDF5 plugin) set up, do some extra things:
    if hasattr(cam, "hdf5"):
        cam.read_attrs.append("hdf5")
        cam.hdf5.read_attrs = []
    cam.configuration_attrs.append("cam.acquire_time")
    for j in range(1, 5):
        st = getattr(cam, "stats{}".format(j))
        st.nd_array_port.set("ROI{}".format(j))
        st.read_attrs = sts_readattrs
    cam.stats5.read_attrs = sts_readattrs


#####try instead
# m3_diag_cam = StandardCam('XF:02IDC-BI{Mir:3-Cam:13_U_1}', name='m3_diag_cam')


class SIXQuadEM(QuadEM):
    conf = Cpt(QuadEMPort, port_name="EM180")
    em_range = Cpt(EpicsSignalWithRBV, "Range", string=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for c in ['current{}'.format(j) for j in range(1, 5)]:
        #     getattr(self, c).read_attrs = ['mean_value']

        # self.read_attrs = ['current{}'.format(j) for j in range(1, 5)]
        self.stage_sigs.update(
            [
                (self.acquire_mode, "Single")  # single mode
            ]
        )
        self.configuration_attrs = [
            "integration_time",
            "averaging_time",
            "em_range",
            "num_averaged",
            "values_per_read",
        ]


def name_qem(qem, chan_names, chan_numbers=None):
    if chan_numbers is None:
        chan_numbers = [j + 1 for j in range(len(chan_names))]
    read_attrs = []
    for j, chan_name in zip(chan_numbers, chan_names):
        current = getattr(qem, f"current{j}")
        current.mean_value.name = chan_name
        current.kind |= Kind.normal
        current.mean_value.kind |= Kind.normal
        read_attrs.append(f"current{j}.mean_value")
    qem.read_attrs = read_attrs
    return qem


# qem01 = name_qem(SIXQuadEM('XF:02IDA-BI{EM:1}EM180:', name='qem01'),
#                 ['m1slt_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

# qem2 and 3 not working 9/2/22 after power shutdown
# qem02 = name_qem(SIXQuadEM('XF:02IDB-BI{EM:2}EM180:', name='qem02'),
#                 ['pgmslt_u_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

# qem03 = name_qem(SIXQuadEM('XF:02IDB-BI{EM:3}EM180:', name='qem03'),
#                 ['pgmslt_d_{}_tey'.format(s) for s in ('in', 'out', 'bot', 'top')])

qem04 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:4}EM180:", name="qem04"),
    ["m3slt_{}_tey".format(s) for s in ("in", "out", "bot", "top")],
)

qem05 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:5}EM180:", name="qem05"),
    ["m3_diag_{}".format(s) for s in ("diode", "grid")],
)

qem06 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:6}EM180:", name="qem06"),
    ["extslt_{}_tey".format(s) for s in ("hdsl", "hdsr")],
)

qem07 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:7}EM180:", name="qem07"),
    ["gc_diag_{}".format(s) for s in ("diode", "grid")],
    chan_numbers=[1, 3],
)

qem08 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:8}EM180:", name="qem08"),
    ["rs_diag_{}_tey".format(s) for s in ("1", "2")],
)

qem09 = name_qem(
    SIXQuadEM("XF:02IDC-BI{EM:9}EM180:", name="qem09"),
    ["m4slt_{}_tey".format(s) for s in ("in", "out", "bot", "top")],
)

# qem10 = name_qem(SIXQuadEM('XF:02IDC-BI{EM:10}EM180:', name='qem10'),
# ['m4_mir'])
#                 ['m4'.format(s) for s in ('mir')])

# qem11 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:11}EM180:', name='qem11'),
#                  ['sc_diode_{}'.format(s) for s in ('1','2','3','4')])

# JPcommented this 20210426
# qem12 = name_qem(SIXQuadEM('XF:02IDD-BI{EM:12}EM180:', name='qem12'),
#                 ['sample_tey_{}'.format(s) for s in ('top','empty','bot')])

# Maffettone commented this out 20220119 and replaced with a modified name_qem()
# qem07.hints = {'fields': ['gc_diag_grid', 'gc_diag_diode']}
# qem07.current1.mean_value.kind = Kind.hinted
# qem07.current3.mean_value.kind = Kind.hinted
# qem07.current2.mean_value.kind = Kind.normal
# qem07.read_attrs = ['current1.mean_value', 'current3.mean_value']


# JP commented this 20210426
# qem12.hints = {'fields': ['sample_tey_top', 'sample_tey_bot']}
# qem12.read_attrs = ['current1.mean_value', 'current3.mean_value']
# qem12.current1.mean_value.kind = Kind.hinted
# qem12.current3.mean_value.kind = Kind.hinted
class PvaPluginWithPluginAttributes(PvaPlugin):
    nd_array_port = Cpt(EpicsSignalWithRBV, "NDArrayPort", kind="config")
    enable = Cpt(EpicsSignalWithRBV, "EnableCallbacks", string=True, kind="config")


def set_plugin_graph(graph: dict[PluginBase, Union[CamBase, PluginBase]]) -> None:
    for target, source in graph.items():
        target.nd_array_port.set(source.port_name.get()).wait(0.5)

    for plugin in graph.keys():
        plugin.enable.set(1).wait(0.5)


class AxisDetectorCam(AreaDetectorCam):
    """
    Custom AxisDetectorCam class to include a `wait_for_plugins` signal.
    """

    _default_configuration_attrs = AreaDetectorCam._default_configuration_attrs + (
        "gain",
        "prnu",
        "tec",
        "bin_mode",
        # there are functions to add attrs for image corrections when testing (see .startup.detectors)
        # we should add more functionality to enable/disable triggering. if enabled, add atts
    )
    wait_for_plugins = Cpt(EpicsSignal, "WaitForPlugins", string=True, kind="hinted")
    gain = Cpt(EpicsSignalWithRBV, "GainMode", string=True, kind="config")
    prnu = Cpt(EpicsSignalWithRBV, "PRNU", string=True, kind="config")
    tec = Cpt(EpicsSignalWithRBV, "TEC", string=True, kind="config")
    auto_tec = Cpt(EpicsSignalWithRBV, "AutoTEC", string=True, kind="config")
    bin_mode = Cpt(EpicsSignalWithRBV, "BinMode", string=True, kind="config")
    temperature = Cpt(EpicsSignalRO, "Temperature_RBV")
    retry_on_timeout = Cpt(
        EpicsSignalWithRBV, "RetryOnTimeout", string=True, kind="config"
    )
    num_retries = Cpt(EpicsSignalWithRBV, "NumRetries", kind="config")
    frame_speed = Cpt(EpicsSignalWithRBV, "FrameSpeed", kind="config")
    bit_depth = Cpt(EpicsSignalWithRBV, "BitDepth", kind="config")
    auto_exposure = Cpt(EpicsSignalWithRBV, "AutoExposure", string=True, kind="config")
    fan_gear = Cpt(EpicsSignalWithRBV, "FanGear", string=True, kind="config")
    auto_levels = Cpt(EpicsSignalWithRBV, "AutoLevels", string=True, kind="config")
    histogram = Cpt(EpicsSignalWithRBV, "Histogram", string=True, kind="config")
    enhance = Cpt(EpicsSignalWithRBV, "Enhance", string=True, kind="config")
    defect_correction = Cpt(
        EpicsSignalWithRBV, "DefectCorrection", string=True, kind="config"
    )
    enable_denoise = Cpt(
        EpicsSignalWithRBV, "EnableDenoise", string=True, kind="config"
    )
    flat_correction = Cpt(
        EpicsSignalWithRBV, "FlatCorrection", string=True, kind="config"
    )
    dyn_rge_correction = Cpt(
        EpicsSignalWithRBV, "DynRgeCorrection", string=True, kind="config"
    )
    frame_format = Cpt(EpicsSignalWithRBV, "FrameFormat", string=True, kind="config")
    brightness = Cpt(EpicsSignalWithRBV, "Brightness", kind="config")
    black_level = Cpt(EpicsSignalWithRBV, "BlackLevel", kind="config")
    sharpness = Cpt(EpicsSignalWithRBV, "Sharpness", kind="config")
    noise_level = Cpt(EpicsSignalWithRBV, "NoiseLevel", kind="config")
    hdr_k = Cpt(EpicsSignalWithRBV, "HDRK", kind="config")
    gamma = Cpt(EpicsSignalWithRBV, "Gamma", kind="config")
    contrast = Cpt(EpicsSignalWithRBV, "Contrast", kind="config")
    left_levels = Cpt(EpicsSignalWithRBV, "LeftLevels", kind="config")
    right_levels = Cpt(EpicsSignalWithRBV, "RightLevels", kind="config")
    trigger_edge = Cpt(EpicsSignalWithRBV, "TriggerEdge", string=True, kind="config")
    trigger_exposure = Cpt(
        EpicsSignalWithRBV, "TriggerExposure", string=True, kind="config"
    )
    trigger_delay = Cpt(EpicsSignalWithRBV, "TriggerDelay", kind="config")
    software_trigger = Cpt(EpicsSignal, "SoftwareTrigger", string=True)
    trigger_out1_mode = Cpt(EpicsSignalWithRBV, "TriggerOut1Mode", string=True)
    trigger_out1_edge = Cpt(EpicsSignalWithRBV, "TriggerOut1Edge", string=True)
    trigger_out1_delay = Cpt(EpicsSignalWithRBV, "TriggerOut1Delay", kind="config")
    trigger_out1_width = Cpt(EpicsSignalWithRBV, "TriggerOut1Width", kind="config")
    trigger_out2_mode = Cpt(EpicsSignalWithRBV, "TriggerOut2Mode", string=True)
    trigger_out2_edge = Cpt(EpicsSignalWithRBV, "TriggerOut2Edge", string=True)
    trigger_out2_delay = Cpt(EpicsSignalWithRBV, "TriggerOut2Delay", kind="config")
    trigger_out2_width = Cpt(EpicsSignalWithRBV, "TriggerOut2Width", kind="config")
    trigger_out3_mode = Cpt(EpicsSignalWithRBV, "TriggerOut3Mode", string=True)
    trigger_out3_edge = Cpt(EpicsSignalWithRBV, "TriggerOut3Edge", string=True)
    trigger_out3_delay = Cpt(EpicsSignalWithRBV, "TriggerOut3Delay", kind="config")
    trigger_out3_width = Cpt(EpicsSignalWithRBV, "TriggerOut3Width", kind="config")
    acquire_period = ADComponent(
        EpicsSignalWithRBV, "AcquirePeriod", tolerance=0.01, timeout=5, kind="config"
    )


class AxisCamBase(AreaDetector):
    """
    Class for Axis detector with HDF5 file saving.

    The IOC is currently hosted on a Windows machine so the
    `write_path_template` must be specified as a Windows path.
    """

    cam = Cpt(AxisDetectorCam, "cam1:")
    stats1 = Cpt(StatsPlugin, "Stats1:")
    stats2 = Cpt(StatsPlugin, "Stats2:")
    stats3 = Cpt(StatsPlugin, "Stats3:")
    stats4 = Cpt(StatsPlugin, "Stats4:")
    stats5 = Cpt(StatsPlugin, "Stats5:")
    roi1 = Cpt(ROIPlugin, "ROI1:")
    roi2 = Cpt(ROIPlugin, "ROI2:")
    roi3 = Cpt(ROIPlugin, "ROI3:")
    roi4 = Cpt(ROIPlugin, "ROI4:")
    proc1 = Cpt(ProcessPlugin, "Proc1:")
    proc2 = Cpt(ProcessPlugin, "Proc2:")
    trans1 = Cpt(TransformPlugin, "Trans1:")
    trans2 = Cpt(TransformPlugin, "Trans2:")
    over1 = Cpt(OverlayPlugin, "Over1:")
    hdf5 = Cpt(
        HDF5PluginWithFileStore,
        suffix="HDF1:",
        read_path_template="/nsls2/data/csx/legacy/axis_data/hdf5/%Y/%m/%d",
        root="/nsls2/data/csx/legacy/axis_data/hdf5",
        write_path_template="/nsls2/data/csx/legacy/axis_data/hdf5/%Y/%m/%d",
        path_semantics="posix",
    )
    pva1 = Cpt(PvaPluginWithPluginAttributes, "Pva1:")
    _default_plugin_graph: Optional[dict[PluginBase, Union[CamBase, PluginBase]]] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hdf5.kind = "normal"
        self.hdf5.file_path.path_semantics = "posix"
        self.ensure_acquiring = False
        # Camera is currently UInt16, the default is wrong at Int8
        self.cam.data_type.set("UInt16")
        self.additional_timeout = 0.0

        self._use_default_plugin_graph: bool = True
        self._plugin_graph_cache: Optional[
            dict[PluginBase, Union[CamBase, PluginBase]]
        ] = None

    @property
    def default_plugin_graph(
        self,
    ) -> Optional[dict[PluginBase, Union[CamBase, PluginBase]]]:
        return self._default_plugin_graph

    def disable_default_plugin_graph(self):
        logger.warning(
            f"Disabling default plugin graph for {self.name}. This can lead to unexpected behavior."
        )
        self._use_default_plugin_graph = False

    def enable_default_plugin_graph(self):
        self._use_default_plugin_graph = True

    def _stage_plugin_graph(
        self, plugin_graph: dict[PluginBase, Union[CamBase, PluginBase]]
    ):
        for target, source in plugin_graph.items():
            self.stage_sigs[target.nd_array_port] = source.port_name.get()
            self.stage_sigs[target.enable] = True

    def reset_plugin_graph(self):
        """Resets the plugin graph to the default state."""
        set_plugin_graph(self.default_plugin_graph)

    def stage(self):
        # Ensure we continue acquiring in case of failure
        self.ensure_acquiring = (
            self.cam.image_mode.get(as_string=True) == "Continuous"
            and self.cam.acquire.get() == 1
        )

        # Adjust timeout relative to acquire_time and acquire_period
        exposure_time = self.cam.acquire_time.get()
        acquire_period = self.cam.acquire_period.get()
        self.additional_timeout = exposure_time + acquire_period
        self.cam.acquire._timeout += self.additional_timeout

        # Configure the plugin graph to use the default configuration
        # Must use `stage_sigs` in order to reset on unstage
        if self._use_default_plugin_graph and self.default_plugin_graph is not None:
            self._stage_plugin_graph(self.default_plugin_graph)

        ret = super().stage()
        return ret

    def unstage(self):
        super().unstage()

        # Adjust timeout back to original value
        self.cam.acquire._timeout -= self.additional_timeout

        # If the image mode was continuous, start acquiring again
        acquiring = self.cam.acquire.get()
        if self.ensure_acquiring and acquiring == 0:
            self.cam.acquire.set(1).wait(3.0)
        # Otherwise, we were in continuous mode but not acquiring
        # so stop the acquisiton again
        elif (
            not self.ensure_acquiring
            and self.cam.image_mode.get(as_string=True) == "Continuous"
            and acquiring == 1
        ):
            self.cam.acquire.set(0).wait(3.0)

    def ensure_nonblocking(self):
        self.stage_sigs["cam.wait_for_plugins"] = "No"
        for c in self.component_names:
            cpt = getattr(self, c)
            if cpt is self:
                continue
            if hasattr(cpt, "ensure_nonblocking"):
                cpt.ensure_nonblocking()


class StandardAxisCam(SingleTrigger, AxisCamBase):
    """Axis detector that runs in multiple acquisition mode.

    It runs in non-blocking mode by default so that capturing
    frames is not slowed down by the cumulative execution time of the plugins.

    This may mean that the file writing is not complete before subsequent acquisitions.

    The defualt plugin configuration is:
        AXIS1 -> HDF5
              -> STATS5
              -> PROC1 -> TRANS1 -> ROI1 -> STATS1
                                 -> ROI2 -> STATS2
                                 -> ROI3 -> STATS3
                                 -> ROI4 -> STATS4
              -> PROC2 -> TRANS2 -> OVER1 -> PVA1
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs[self.cam.wait_for_plugins] = "No"
        # Changing image_mode stops acquisition every time
        # so using stage_sigs doesn't work
        self.stage_sigs.pop("cam.acquire")
        self.ensure_nonblocking()

        self._default_plugin_graph = {
            self.hdf5: self.cam,
            self.stats5: self.cam,
            self.proc1: self.cam,
            self.proc2: self.cam,
            self.trans1: self.proc1,
            self.trans2: self.proc2,
            self.roi1: self.trans1,
            self.roi2: self.trans1,
            self.roi3: self.trans1,
            self.roi4: self.trans1,
            self.stats1: self.roi1,
            self.stats2: self.roi2,
            self.stats3: self.roi3,
            self.stats4: self.roi4,
            self.over1: self.trans2,
            self.pva1: self.over1,
        }

    def stage(self):
        ret = super().stage()

        # Manually stop acquiring
        if self.cam.acquire.get() == 1:
            self.cam.acquire.set(0).wait(3.0)

        return ret


class ContinuousAxisCam(ContinuousAcquisitionTrigger, AxisCamBase):
    """Axis detector that runs in continuous acquisition mode.

    It uses a circular buffer plugin to trigger capturing frames
    from the detector *driver* instead of directly from the detector.

    It runs in non-blocking mode by default so that any displays can
    update asynchronously from Bluesky plans.

    The defualt plugin configuration is:
        AXIS1 -> CB1 -> HDF5
              -> CB1 -> STATS5
              -> CB1 -> PROC1 -> TRANS1 -> ROI1 -> STATS1
                                        -> ROI2 -> STATS2
                                        -> ROI3 -> STATS3
                                        -> ROI4 -> STATS4
              -> PROC2 -> TRANS2 -> OVER1 -> PVA1
    """

    cb = Cpt(CircularBuffPlugin_V34, "CB1:")
    # This is for regulating exposure during possible movements
    should_skip_frame = Cpt(Signal, kind="config", value=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Changing the image_mode stops acquisition already
        # so we can't use stage_sigs
        self.stage_sigs.pop("cam.acquire")
        self.ensure_nonblocking()

        self._write_status: TriggerStatus | None = None
        self._num_triggered = 0

        self._default_plugin_graph = {
            self.cb: self.cam,
            self.hdf5: self.cb,
            self.stats5: self.cb,
            self.proc1: self.cb,
            self.proc2: self.cam,
            self.trans1: self.proc1,
            self.trans2: self.proc2,
            self.roi1: self.trans1,
            self.roi2: self.trans1,
            self.roi3: self.trans1,
            self.roi4: self.trans1,
            self.stats1: self.roi1,
            self.stats2: self.roi2,
            self.stats3: self.roi3,
            self.stats4: self.roi4,
            self.over1: self.trans2,
            self.pva1: self.over1,
        }

    def stage(self):
        self.stage_sigs[self.cb.post_count] = self.cam.num_images.get()

        res = super().stage()

        self._num_triggered = 0

        if self.cam.acquire.get() == 0:
            # Manually start acquiring
            self.cam.acquire.set(1).wait(3.0)

        # Set up subscriptions for all leaf-node plugins
        # We need to wait for all leaf-node plugins downstream of the circular buffer to finish writing
        # before we can trigger the next acquisition.
        asyn_graph: tuple[nx.DiGraph, dict[str, ADBase]] = self.get_asyn_digraph()
        graph = asyn_graph[0]
        port_map = asyn_graph[1]
        reachable_nodes = nx.descendants(graph, self.cb.port_name.get())
        self._leaf_plugins: list[PluginBase] = [
            port_map[node]
            for node in reachable_nodes
            if graph.out_degree(node) == 0 and isinstance(port_map[node], PluginBase)
        ]

        # Reset array counters to 0 so we can properly wait
        for plugin in self._leaf_plugins:
            plugin.array_counter.set(0).wait()

        return res

    def _skip_frame(self):
        current_frame_number = self.cam.num_images_counter.get()

        def frame_changed(value, old_value, **kwargs):
            return value > current_frame_number

        # Wait until one full frame finishes, timeout indicates that something is wrong
        SubscriptionStatus(self.cam.num_images_counter, frame_changed).wait(
            timeout=self.cam.acquire_period.get() * 2 - 1e-4
        )

    def _plugin_complete(self, old_value, value, **kwargs) -> bool:
        return value == self.cb.post_count.get() * self._num_triggered

    def trigger(self):
        """
        Since we are non-blocking at the EPICS level, we want to wait for the HDF5
        plugin to finish writing before we trigger the next acquisition.
        """
        if self.should_skip_frame.get():
            # We must wait until this first frame is complete before we can
            # start exposing a new frame. Otherwise, we may grab a frame
            # that was exposing during a movement (of a motor or energy or temperature value)
            self._skip_frame()

        # Trigger the circular buffer with the fully exposed frame
        self._num_triggered += 1
        super().trigger()

        # Return a Status that is done when all leaf-node plugins are complete
        statuses = [
            SubscriptionStatus(plugin.array_counter, self._plugin_complete)
            for plugin in self._leaf_plugins
        ]
        return reduce(lambda a, b: a & b, statuses)

    def unstage(self):
        super().unstage()
        self._num_triggered = 0


start_time = time.monotonic()
