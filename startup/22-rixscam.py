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
    #Delays
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


    #Voltages
    #CCD1
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
    #CCD2
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

    #Temperature Control
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
 
    def set_voltages(self):
        self.vod1.put(32.85)
        self.vdd1.put(20.02)
        self.vrd1.put(19.08)
        self.vog1.put(5.64)
        self.vss1.put(6.20)
        self.hv_dc1.put(5.73)
        self.pedestal.put(1.16)
        self.vclk_im1.put(6.60)
        self.vclk_st1.put(11.90)
        self.vclk_se1.put(12.38)
        self.vclk_rst1.put(9.02)

        self.vod2.put(32.85)
        self.vdd2.put(20.02)
        self.vrd2.put(19.08)
        self.vog2.put(5.64)
        self.vss2.put(6.20)
        self.hv_dc2.put(5.73)
        self.pedestal.put(1.16)
        self.vclk_im2.put(6.60)
        self.vclk_st2.put(11.90)
        self.vclk_se2.put(12.38)
        self.vclk_rst2.put(9.02)
        
    def set_HR(self):
        #missing Node Readout mode "HR node"
        self.set_voltages()
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
        #missing Node Readout mode "LS node"
        self.set_voltages()
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

    def set_temp_control(self):
        en_ctr.put('On')
        ctr_mode = 'Manual'
        heater_sel = 'Output 1'
        sensor_sel = 'Input 1'
        err_lim = 8192
        out_bias = 13087
        gain_prop = 255
        gain_int = 255
        gain_der = 0
        rate_prop = 128
        rate_int = 128
        rate_der = 7

rixscam = RIXSCam('XF:02ID1-ES{RIXSCam}:', name='rixscam')
rixscam.hdf5.read_attrs = []
rixscam.read_attrs = ['hdf5']
rixscam.configuration_attrs = ['cam.acquire_time', 'cam.acquire_period',
                               'cam.num_exposures',
                               'cam.temperature', 'cam.temperature_actual',
                               'cam.trigger_mode', 'ccd1_hv', 'ccd2_hv', 
                               'set_node',
                               #'sensor_xsize', 'sensor_ysize',
                               'sensor_region_xsize', 'sensor_region_ysize', 
                               'sensor_region_xstart', 'sensor_region_ystart', 
                               'sensor_binning_x', 'sensor_binning_y'] 


