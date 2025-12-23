from ophyd.areadetector import AreaDetector, HDF5Plugin
from ophyd.areadetector.plugins import PluginBase
from ophyd.areadetector.cam import ADCpt

from ophyd.areadetector.filestore_mixins import (FileStoreHDF5IterativeWrite,
                                                 FileStorePluginBase,
                                                 FileStoreIterativeWrite)
from ophyd.areadetector.trigger_mixins import SingleTrigger
from ophyd import (Component as Cpt, EpicsSignal, EpicsSignalRO, Device)
from ophyd.areadetector.base import EpicsSignalWithRBV as SignalWithRBV
from ophyd.signal import Signal
from ophyd.device import Staged
from ophyd.sim import NullStatus
from databroker.assets.handlers_base import HandlerBase
import time as ttime
import os.path
import h5py


class HDF5SingleHandler(HandlerBase):
    '''Handler for hdf5 data stored 1 image per file.


    Parameters
    ----------
    fpath : string
        filepath
    template : string
        filename template string.
    filename : string
        filename
    key : string
        the 'path' inside the file to the data set.
    frame_per_point : float
        the number of frames per point.
    '''
    specs = {'AD_HDF5_SINGLE'} | HandlerBase.specs

    def __init__(self, fpath, template, filename, key, frame_per_point=1):
        self._path = os.path.join(fpath, '')
        self._fpp = frame_per_point
        self._template = template
        self._filename = filename
        self._key = key

    def _fnames_for_point(self, point_number):
        start = int(point_number * self._fpp)
        stop = int((point_number + 1) * self._fpp)
        for j in range(start, stop):
            yield self._template % (self._path, self._filename, j)

    def __call__(self, point_number):
        ret = []
        for fn in self._fnames_for_point(point_number):
            f = h5py.File(fn, 'r')
            data = f[self._key]
            ret.append(data)
        return ret

    def get_file_list(self, datum_kwargs):
        ret = []
        for d_kw in datum_kwargs:
            ret.extend(self._fnames_for_point(**d_kw))
        return ret


class AreaDetectorHDF5SingleHandler(HDF5SingleHandler):
    '''Handler for hdf5 data stored 1 image per file by areadetector

    Parameters
    ----------
    fpath : string
        filepath
    template : string
        filename template string.
    filename : string
        filename
    frame_per_point : float
        the number of frames per point.
    '''
    def __init__(self, fpath, template, filename, frame_per_point=1):
        hardcoded_key = '/entry/data/data'
        super(AreaDetectorHDF5SingleHandler, self).__init__(
            fpath=fpath, template=template, filename=filename,
            key=hardcoded_key, frame_per_point=frame_per_point)


#db.reg.register_handler('AD_HDF5_SINGLE', AreaDetectorHDF5SingleHandler)


class FileStoreHDF5Single(FileStorePluginBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filestore_spec = 'AD_HDF5_SINGLE'  # spec name stored in res. doc

        self.stage_sigs.update([('file_template', '%s%s_%6.6d.h5'),
                                ('file_write_mode', 'Single'),
                                ])
        # 'Single' file_write_mode means one image : one file.
        # It does NOT mean that 'num_images' is ignored.

    def get_frames_per_point(self):
        return self.parent.cam.num_images.get()

    def stage(self):
        super().stage()
        # this over-rides the behavior is the base stage
        self._fn = self._fp

        resource_kwargs = {'template': self.file_template.get(),
                           'filename': self.file_name.get(),
                           'frame_per_point': self.get_frames_per_point()}
        self._generate_resource(resource_kwargs)


class FileStoreHDF5SingleIterativeWrite(FileStoreHDF5Single, FileStoreIterativeWrite):
    pass


class XIPPlugin(PluginBase):
    'A class for the centroiding plugin'
    _suffix_re = r'XIP\d:'
    _default_read_attrs = (PluginBase._default_read_attrs + (
                           'count_possible_event', 'count_above_threshold',
                           'count_below_threshold', 'count_neighbours',
                           'count_event_2x2', 'count_event_3x3'))
    _default_configuration_attrs = (PluginBase._default_configuration_attrs + (
                                    'algorithm', 'output_mode',
                                    'bkgd_update_mode', 'bkgd_value',
                                    'sum_3x3_threshold_min',
                                    'sum_3x3_threshold_max', 'hist_start',
                                    'hist_bin_width', 'hist_bin_count',
                                    'source_region', 'dim0_region_start',
                                    'dim0_region_size', 'dim1_region_start',
                                    'dim1_region_size', 'x_expansion_factor',
                                    'y_expansion_factor',
                                    'centroid_correction', 'beamline_energy',
                                    'isolinear_correction',
                                    'isolinear_coefficient_x2_1',
                                    'isolinear_coefficient_x1_1',
                                    'isolinear_coefficient_x0_1',
                                    'isolinear_coefficient_x2_2',
                                    'isolinear_coefficient_x1_2',
                                    'isolinear_coefficient_x0_2',
                                    'isolinear_threshold'))

    algorithm = Cpt(EpicsSignal, 'ALGORITHM', string=True)
    output_mode = Cpt(EpicsSignal, 'OUTPUT_MODE', string=True)

    bkgd_update_mode = Cpt(EpicsSignal, 'BACKGROUND_UPDATE_MODE', string=True)
    bkgd_value = Cpt(SignalWithRBV, 'BACKGROUND_VALUE')

    sum_3x3_threshold_min = Cpt(SignalWithRBV, 'SUM3X3_THRESHOLD_MINIMUM')
    sum_3x3_threshold_max = Cpt(SignalWithRBV, 'SUM3X3_THRESHOLD_MAXIMUM')

    hist_start = Cpt(SignalWithRBV, 'HISTOGRAM_RANGEMINIMUM')
    hist_bin_width = Cpt(SignalWithRBV, 'HISTOGRAM_BINWIDTH')
    hist_bin_count = Cpt(SignalWithRBV, 'HISTOGRAM_BINCOUNT')

    source_region = Cpt(EpicsSignal, 'ENABLE_SOURCE_REGION', string=True)
    dim0_region_start = Cpt(SignalWithRBV, 'DIM0_MIN')
    dim0_region_size = Cpt(SignalWithRBV, 'DIM0_SIZE')
    dim1_region_start = Cpt(SignalWithRBV, 'DIM1_MIN')
    dim1_region_size = Cpt(SignalWithRBV, 'DIM1_SIZE')

    x_expansion_factor = Cpt(SignalWithRBV, 'EXPAND_FACTOR_X')
    y_expansion_factor = Cpt(SignalWithRBV, 'EXPAND_FACTOR_Y')

    frames_accumulated = Cpt(EpicsSignalRO, 'FRAMES_ACCUMULATED_RBV')

    centroid_correction = Cpt(EpicsSignal, 'CENTROID_FILENAME', string=True)
    beamline_energy = Cpt(EpicsSignal, 'BEAMLINE_ENERGY')

    isolinear_correction = Cpt(EpicsSignal, 'ENABLE_ISOLINEAR_CORRECTION',
                               string=True)
    isolinear_coefficient_x2_1 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X2_1')
    isolinear_coefficient_x1_1 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X1_1')
    isolinear_coefficient_x0_1 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X0_1')
    isolinear_coefficient_x2_2 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X2_2')
    isolinear_coefficient_x1_2 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X1_2')
    isolinear_coefficient_x0_2 = Cpt(SignalWithRBV,
                                     'ISOLINEAR_COEFFICIENT_X0_2')
    isolinear_threshold = Cpt(EpicsSignal,
                              'HR_ISOLINEAR_CALIBRATION_THRESHOLD')

    count_possible_event = Cpt(EpicsSignalRO, 'COUNT_POSSIBLE_EVENT_RBV')
    count_above_threshold = Cpt(EpicsSignalRO, 'COUNT_ABOVE_THRESHOLD_RBV')
    count_below_threshold = Cpt(EpicsSignalRO, 'COUNT_BELOW_THRESHOLD_RBV')
    count_neighbours = Cpt(EpicsSignalRO, 'COUNT_NEIGHBOURING_RBV')
    count_event_2x2 = Cpt(EpicsSignalRO, 'COUNT_ACTUAL_2X2_RBV')
    count_event_3x3 = Cpt(EpicsSignalRO, 'COUNT_ACTUAL_3X3_RBV')

    max_threads = Cpt(SignalWithRBV, 'MAX_THREADS')


class TriggeredCamExposure(Device):
    '''A class designed for the setting of the detector exposure parameters
    (acquire_time, acquire_period and num_images) at once.

    This class is used to provide an attribute for setting the exposure
    parameters in a single command. It sets the aqcuire_time (and at the same
    time the delay generator parameters) the acquire_period and the num_images.
    These are set via the child 'set' attribute.
    '''

    def __init__(self, *args, **kwargs):
        self._Tc = 0.004
        self._To = 0.0035
        self._readout = 0.080
        super().__init__(*args, **kwargs)

    def set(self, exp):
        '''Used for the setting of the detector exposure parameters
        (acquire_time, acquire_period and num_images) and the delay
        generator parameters.

        This function is used to provide an attribute for setting the exposure
        parameters in a single command. It sets the aqcuire_time (and at the
        same time the delay generator parameters) the acquire_period and the
        num_images.

        PARAMETERS
        ----------
        exp: tuple.
        A tuple with the structure (aqcuire_time, acquire_period, num_images).
        '''

        # Exposure time = 0
        # Cycle time = 1

        if exp[0] is not None:
            Efccd = exp[0] + self._Tc + self._To
            # To = start of FastCCD Exposure
            aa = 0                          # Shutter open
            bb = Efccd - self._Tc + aa      # Shutter close
            cc = self._To * 3               # diag6 gate start
            dd = exp[0] - (self._Tc * 2)    # diag6 gate stop
            ee = 0                          # Channel Adv Start
            ff = 0.001                      # Channel Adv Stop
            gg = self._To                   # MCS Count Gate Start
            hh = exp[0] + self._To          # MCS Count Gate Stop

            # Set delay generator
            self.parent.dg1.A.set(aa)
            self.parent.dg1.B.set(bb)
            self.parent.dg1.C.set(cc)
            self.parent.dg1.D.set(dd)
            self.parent.dg1.E.set(ee)
            self.parent.dg1.F.set(ff)
            self.parent.dg1.G.set(gg)
            self.parent.dg1.H.set(hh)

            # Set AreaDetector
            self.parent.cam.acquire_time.set(Efccd)

        # Now do period
        if exp[1] is not None:
            if exp[1] < (Efccd + self._readout):
                p = Efccd + self._readout
            else:
                p = exp[1]

        self.parent.cam.acquire_period.set(p)

        if exp[2] is not None:
            self.parent.cam.num_images.set(exp[2])

        return NullStatus()

    def get(self):
        return None


class RIXSCamHDF5PluginWithFileStore(HDF5Plugin, FileStoreHDF5IterativeWrite):

    def get_frames_per_point(self):
        return self.parent.cam.num_images.get()

    # Override the write_path_template code in FileStoreBase because is
    # assumes UNIX, not Windows, and adds a trailing forward slash.
    @property
    def write_path_template(self):
        return self._naive_write_path_template

    @write_path_template.setter
    def write_path_template(self, val):
        self._naive_write_path_template = val


class RIXSCamHDF5PluginForXIP(HDF5Plugin, FileStoreHDF5SingleIterativeWrite):
    '''This modifies the `array_size` attribute so that the second value is
    'unknown'.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the filestore_spec name
        self.filestore_spec = 'AD_HDF5_SINGLE_XIP'

    # Add some parameters required to retrieve the data as a pandas dataframe
    key = '/entry/data/data'
    column_names = ('x', 'y', 'x_eta', 'y_eta', 'y_eta_iso', 'sum_regions',
                    'XIP mode')

    # Override the write_path_template code in FileStoreBase because is
    # assumes UNIX, not Windows, and adds a trailing forward slash.
    @property
    def write_path_template(self):
        return self._naive_write_path_template

    @write_path_template.setter
    def write_path_template(self, val):
        self._naive_write_path_template = val

    # write a new stage method that adds `column_names` and `key` to
    # resource_kwargs.
    def stage(self):
        super().stage()
        # this over-rides the behavior is the base stage
        self._fn = self._fp

        resource_kwargs = {'template': self.file_template.get(),
                           'filename': self.file_name.get(),
                           'key': self.key,
                           'column_names': self.column_names,
                           'frame_per_point': self.get_frames_per_point()}
        self._generate_resource(resource_kwargs)


class RIXSSingleTrigger(SingleTrigger):
    '''Modifies the `trigger` attribute so that it triggers the 2 hdf5 files
    independently.

    This avoids the `dispatch` attribute entirely, but requires that both hdf5
    and hdf2 attributes are included for the detector. It only generates the
    hdf2 field if self.centroid is true.
    '''
    def trigger(self):
        if self._staged != Staged.yes:
            raise RuntimeError("This detector is not ready to trigger."
                               "Call the stage() method before triggering.")

        self._status = self._status_type(self)
        self._acquisition_signal.put(1, wait=False)
        # Here we do away with the `dispatch` method used in `SingleTrigger` as
        # that gives the same field to multiple datafiles which DB can't handle
        self.hdf5.generate_datum('rixscam_image', ttime.time(), {})
        if self.centroid_enable:
            self.hdf2.generate_datum('rixscam_centroids', ttime.time(), {})
        return self._status


class RIXSCam(RIXSSingleTrigger, AreaDetector):

    exposure = Cpt(TriggeredCamExposure, '')

    centroid_enable = Cpt(Signal, value=False)

    xip = Cpt(XIPPlugin, suffix='XIP1:')

    trigger_mode = ADCpt(SignalWithRBV, 'TriggerMode', string=True)  # override string=False default
    

    hdf5 = Cpt(RIXSCamHDF5PluginWithFileStore,
               suffix='HDF1:',
               write_path_template=f'Z:\\{RE.md["cycle"]}\\{RE.md["data_session"]}\\assets\\rixscam\\%Y\\%m\\%d\\',
               read_path_template=f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam/%Y/%m/%d',
               root=f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam'
    )

# Once the hdf2 IOC issues are sorted then Uncomment out the next 6 lines
    hdf2 = Cpt(RIXSCamHDF5PluginForXIP,
               suffix='HDF2:' ,
               write_path_template=f'Z:\\{RE.md["cycle"]}\\{RE.md["data_session"]}\\assets\\rixscam\\%Y\\%m\\%d\\',
               read_path_template=f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam/%Y/%m/%d',
               root=f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam'
            )

    set_node = Cpt(EpicsSignal, 'cam1:SEQ_NODE_SELECTION')
    # Delays
    delay_adc = Cpt(EpicsSignal, 'cam1:SEQ_ADC_DELAY')
    delay_intminus = Cpt(EpicsSignal, 'cam1:SEQ_INT_MINUS_DELAY')
    delay_intplus = Cpt(EpicsSignal, 'cam1:SEQ_INT_PLUS_DELAY')
    delay_inttime = Cpt(EpicsSignal, 'cam1:SEQ_INT_TIME')
    delay_serialT = Cpt(EpicsSignal, 'cam1:SEQ_SERIAL_T')
    delay_parT = Cpt(EpicsSignal, 'cam1:SEQ_PARALLEL_T')

    # Sensor Physical Size (this will never change)
    sensor_xsize = 1648
    sensor_ysize = 1608
    # ROI definition (aka Region size/start)
    sensor_region_xsize = Cpt(EpicsSignal, 'cam1:SizeX')
    sensor_region_ysize = Cpt(EpicsSignal, 'cam1:SizeY')
    sensor_region_xstart = Cpt(EpicsSignal, 'cam1:MinX')
    sensor_region_ystart = Cpt(EpicsSignal, 'cam1:MinY')
    # Binning
    sensor_binning_x = Cpt(EpicsSignal, 'cam1:BinX')
    sensor_binning_y = Cpt(EpicsSignal, 'cam1:BinY')

    # Voltages
    # CCD1
    vod1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_OD_1')
    vdd1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_DD_1')
    vrd1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_RD_1')
    vog1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_OG_1')
    vss1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_SS_1')
    hv_dc1 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HVDC_1')
    pedestal = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_PEDESTAL_1')
    ccd1_hv = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HV_1')
    vclk_im1 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_IMAGE_1')
    vclk_st1 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_STORE_1')
    vclk_se1 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_SERIAL_1')
    vclk_rst1 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_RESET_1')
    # CCD2
    vod2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_OD_2')
    vdd2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_DD_2')
    vrd2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_RD_2')
    vog2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_OG_2')
    vss2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_SS_2')
    hv_dc2 = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HVDC_2')
    pedestal = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_PEDESTAL_2')
    ccd2_hv = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HV_2')
    vclk_im2 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_IMAGE_2')
    vclk_st2 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_STORE_2')
    vclk_se2 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_SERIAL_2')
    vclk_rst2 = Cpt(EpicsSignal, 'cam1:VOLT_CLOCK_RESET_2')

    # Temperature Control
    en_ctr = Cpt(EpicsSignal, 'cam1:TEMP_ENABLE')
    ctr_mode = Cpt(EpicsSignal, 'cam1:TEMP_MANUAL_MODE')
    heater_sel = Cpt(EpicsSignal, 'cam1:TEMP_HEATER_SELECT')
    sensor_sel = Cpt(EpicsSignal, 'cam1:TEMP_SENSOR_SELECT')
    err_lim = Cpt(EpicsSignal, 'cam1:TEMP_ACCUMULATED_ERROR_LIMIT')
    out_bias = Cpt(EpicsSignal, 'cam1:TEMP_OUTPUT_BIAS')
    gain_prop = Cpt(EpicsSignal, 'cam1:TEMP_PROP_GAIN')
    gain_int = Cpt(EpicsSignal, 'cam1:TEMP_INT_GAIN')
    gain_der = Cpt(EpicsSignal, 'cam1:TEMP_DERIV_GAIN')
    rate_prop = Cpt(EpicsSignal, 'cam1:TEMP_PROP_RATE')
    rate_int = Cpt(EpicsSignal, 'cam1:TEMP_INT_RATE')
    rate_der = Cpt(EpicsSignal, 'cam1:TEMP_DERIV_RATE')

    def set_HR_RT(self):
        yield from self.set_HR()
        yield from mv(self.vss1,9.0)
        yield from mv(self.vss2,9.0)
        
    def set_LS_RT(self):
        yield from self.set_LS()
        yield from mv(self.vss1,9.0)
        yield from mv(self.vss2,9.0)       
        yield from mv(self.ccd1_hv,20)
        yield from mv(self.ccd2_hv,20)        
        
        
    def set_voltages(self):
        yield from mv(self.vod1,32.85)
        yield from mv(self.vdd1,20.02)
        yield from mv(self.vrd1,19.08)
        yield from mv(self.vog1,5.64)
        yield from mv(self.vss1,6.20)
        yield from mv(self.hv_dc1,5.73)
        yield from mv(self.pedestal,1.16)
        yield from mv(self.vclk_im1,6.60)
        yield from mv(self.vclk_st1,11.90)
        yield from mv(self.vclk_se1,12.38)
        yield from mv(self.vclk_rst1,9.02)

        yield from mv(self.vod2,32.85)
        yield from mv(self.vdd2,20.02)
        yield from mv(self.vrd2,19.08)
        yield from mv(self.vog2,5.64)
        yield from mv(self.vss2,6.20)
        yield from mv(self.hv_dc2,5.73)
        yield from mv(self.pedestal,1.16)
        yield from mv(self.vclk_im2,6.60)
        yield from mv(self.vclk_st2,11.90)
        yield from mv(self.vclk_se2, 12.38)
        yield from mv(self.vclk_rst2, 9.02)

    def set_HR(self):
        # missing Node Readout mode "HR node"
        yield from self.set_voltages()
        yield from mv(self.set_node,1)
        yield from mv(self.delay_adc,1)
        yield from mv(self.delay_intminus,14)
        yield from mv(self.delay_intplus,13)
        yield from mv(self.delay_inttime,255)
        yield from mv(self.delay_serialT,3)
        yield from mv(self.delay_parT,255)
        yield from mv(self.ccd1_hv,20)
        yield from mv(self.ccd2_hv,20)

    def set_LS(self):
        # missing Node Readout mode "LS node"
        yield from self.set_voltages()
        yield from mv(self.set_node,0)
        yield from mv(self.delay_adc,168)
        yield from mv(self.delay_intminus,4)
        yield from mv(self.delay_intplus,2)
        yield from mv(self.delay_inttime,80)
        yield from mv(self.delay_serialT,255)
        yield from mv(self.delay_parT,151)
        yield from self.set_LS_high_voltages()

    def set_LS_high_voltages(self):
        #Calibration done on 10/10/2018 for the CCD HV values below using LED light
        yield from mv(self.ccd1_hv,44.88) #Nov 08, 2021 #45.2V from Energy Calibration Oct 2021 #44.5V up to October 4 - 2021
        yield from mv(self.ccd2_hv,45.47) #Nov 08, 2021 #45.6V from Energy Calibration Oct 2021 #45.1V up to October 4 - 2021

    def set_temp_control(self):

        yield from mv(self.en_ctr,'On')
        yield from mv(self.ctr_mode, 'Auto')
        yield from mv(self.heater_sel, 'Output 1')
        yield from mv(self.sensor_sel, 'Input 1')
        yield from mv(self.err_lim, 8192)
        yield from mv(self.out_bias, 13087)
        yield from mv(self.gain_prop, 255)
        yield from mv(self.gain_int, 255)
        yield from mv(self.gain_der, 0)
        yield from mv(self.rate_prop, 128)
        yield from mv(self.rate_int, 128)
        yield from mv(self.rate_der, 7)

    def set_mode(self, mode):
        '''This function sets the device to either perform centroiding or not.

        Parameters
        ----------

        mode : str
            This is a string which indicates weather the detector should be run
            in centroiding mode ( `mode = 'centroid'`) or image mode ( `mode =
            'image'`).

        '''

        if mode == 'image':
            self.read_attrs = ['hdf5']
            yield from mv(self.centroid_enable,False)
            yield from mv(self.hdf2.enable, 'Disable', self.xip.enable, 'Disable')

        elif mode == 'centroid':
            self.read_attrs = ['hdf5', 'hdf2', 'xip']
            yield from mv(self.centroid_enable,True)
            yield from mv(self.hdf2.enable, 'Enable', self.xip.enable, 'Enable')

        else:
            raise ValueError("The input parameter, mode, needs to be 'image' or\
                             'centroid' but got {}".format(mode))


rixscam = RIXSCam('XF:02ID1-ES{RIXSCam}:', name='rixscam')
rixscam.hdf5.read_attrs = []
rixscam.xip.enable.set('Enable')
rixscam.hdf2.enable.set('Enable')

#rixscam.read_attrs = ['hdf5']
rixscam.read_attrs = ['hdf5','hdf2', 'xip'] 
#rixscam.read_attrs = ['hdf2', 'xip']

#TODO once ioc for LS mode threshold works, add threshold and energy values to config attrs
rixscam.configuration_attrs = ['cam.acquire_time', 'cam.acquire_period',
                               'cam.num_images',
                               'cam.temperature', 'cam.temperature_actual',
                               'cam.trigger_mode', 'ccd1_hv', 'ccd2_hv',
                               'set_node', 'centroid_enable',
                               # 'sensor_xsize', 'sensor_ysize',d
                               'sensor_region_xsize', 'sensor_region_ysize',
                               'sensor_region_xstart', 'sensor_region_ystart',
                               'sensor_binning_x', 'sensor_binning_y']


#rixscam.xip.count_neighbours.kind = Kind.hinted
#rixscam.xip.count_event_3x3.kind = Kind.hinted


def rixscam_asleep():
    yield from mv(rixscam.ccd1_hv,20)
    yield from mv(rixscam.ccd2_hv,20)
    print('RIXSCam HVs are set to 20V. Remember to run rixscam_awake() before resuming operation.')

def rixscam_awake():
    yield from rixscam.set_LS_high_voltages()
    print('RIXSCam HVs are set to LS standard values. You can now use the detector for centroiding mode.')