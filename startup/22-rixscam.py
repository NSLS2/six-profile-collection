from ophyd.areadetector import AreaDetector, HDF5Plugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.trigger_mixins import SingleTrigger
from ophyd import (PVPositioner, Component as Cpt, EpicsSignal, EpicsSignalRO,
                   Device)

class RIXSCamHDF5PluginWithFileStore(HDF5Plugin, FileStoreHDF5IterativeWrite):

    def get_frames_per_point(self):
        return 1  # HACK

    # Override the write_path_template code in FileStoreBase because is
    # assumes UNIX, not Windows, and adds a trailing forward slash.
    @property
    def write_path_template(self):
        return self._naive_write_path_template

    @write_path_template.setter
    def write_path_template(self, val):
        self._naive_write_path_template = val


class RIXSCam(SingleTrigger, AreaDetector):

    hdf5 = Cpt(RIXSCamHDF5PluginWithFileStore,
              suffix='HDF1:',
              read_path_template='/XF02ID1/RIXSCAM/DATA/%Y/%m/%d',
              write_path_template='X:\RIXSCAM\DATA\\%Y\\%m\\%d\\',
              root='/XF02ID1',
              reg=db.reg)
    set_node = Cpt(EpicsSignal, 'cam1:SEQ_NODE_SELECTION')
    delay_adc = Cpt(EpicsSignal, 'cam1:SEQ_ADC_DELAY')
    delay_intminus = Cpt(EpicsSignal, 'cam1:SEQ_INT_MINUS_DELAY')
    delay_intplus = Cpt(EpicsSignal, 'cam1:SEQ_INT_PLUS_DELAY')
    delay_inttime = Cpt(EpicsSignal, 'cam1:SEQ_INT_TIME')
    delay_serialT = Cpt(EpicsSignal, 'cam1:SEQ_SERIAL_T')
    delay_parT = Cpt(EpicsSignal, 'cam1:SEQ_PARALLEL_T')

    ccd1_hv = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HV_1')
    ccd2_hv = Cpt(EpicsSignal, 'cam1:VOLT_BIAS_HV_2')


    def set_HR(self):
        self.stage_sigs[self.set_node] = 1        
        self.stage_sigs[self.delay_adc] = 1
        self.stage_sigs[self.delay_intminus] = 14
        self.stage_sigs[self.delay_intplus] = 13
        self.stage_sigs[self.delay_inttime] = 255
        self.stage_sigs[self.delay_serialT] = 3
        self.stage_sigs[self.delay_parT] = 255
        self.stage_sigs[self.ccd1_hv] = 20
        self.stage_sigs[self.ccd2_hv] = 20

    def set_LS(self):
        self.stage_sigs[self.set_node] = 0
        self.stage_sigs[self.delay_adc] = 168
        self.stage_sigs[self.delay_intminus] = 4
        self.stage_sigs[self.delay_intplus] = 2
        self.stage_sigs[self.delay_inttime] = 80
        self.stage_sigs[self.delay_serialT] = 255
        self.stage_sigs[self.delay_parT] = 151
        #Calibration done on 6/13/2017 for the CCD HV values below
        self.stage_sigs[self.ccd1_hv] = 44.5
        self.stage_sigs[self.ccd2_hv] = 44.6



rixscam = RIXSCam('XF:02ID1-ES{RIXSCam}:', name='rixscam')
rixscam.hdf5.read_attrs = []
rixscam.read_attrs = ['hdf5']
rixscam.configuration_attrs = ['cam.acquire_time', 'cam.acquire_period',
                               'cam.num_exposures',
                               'cam.temperature', 'cam.temperature_actual',
                               'cam.trigger_mode']




