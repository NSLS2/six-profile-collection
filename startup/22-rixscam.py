from ophyd.areadetector import AreaDetector, HDF5Plugin
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.trigger_mixins import SingleTrigger


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
    


rixscam = RIXSCam('XF:02ID1-ES{RIXSCam}:', name='rixscam')
rixscam.hdf5.read_attrs = []
rixscam.read_attrs = ['hdf5']
rixscam.configuration_attrs = ['cam.acquire_time', 'cam.acquire_period',
                               'cam.num_exposures',
                               'cam.temperature', 'cam.temperature_actual',
                               'cam.trigger_mode']


