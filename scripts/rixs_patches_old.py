import os.path
import numpy
import pandas as pd


# In theory the columns can vary (set in the Resource document)
# but in practice across all Runs they have never changed.
columns = ("x", "y", "x_eta", "y_eta", "y_eta_iso", "sum_regions", "XIP mode")
dtype_list = [(name, "<f4") for name in columns] + [("frame", "<i2")]
dtype = numpy.dtype(dtype_list)
# Because we cannot put variable-length arrays into xarray,
# we pad out to a fixed length and then truncate the padding
# on the client side.
LENGTH = 4800  # twice the longest we have seen (increased from 2400 in March 2023)


def patch_descriptor(doc):
    if "rixscam_centroids" in doc["data_keys"]:
        data_key = doc["data_keys"]["rixscam_centroids"]
        data_key["dtype_str"] = dtype.str
        data_key["dtype_descr"] = dtype.descr
        data_key["shape"] = (LENGTH,)
    if "rixscam_image" in doc["data_keys"]:
        doc["data_keys"]["rixscam_image"]["dtype_str"] = "<u2"
    if "extslt_hg_user_setpoint" in doc["data_keys"]:
        doc["data_keys"]["extslt_hg_user_setpoint"]["dtype_str"] = "<f8"
    if "extslt_vg_user_setpoint" in doc["data_keys"]:
        doc["data_keys"]["extslt_vg_user_setpoint"]["dtype_str"] = "<f8"
    return doc


class Handler:
    """
    Adapted from sixtools.AD_Handler:AreaDetector_HDF5SingleHandler_DataFrame

    Handler for hdf5 data stored 1 image per file and returned as a
    Pandas.DataFrame.

    This will work with all hdf5 files that are a mxn arrays and the data is
    'table like' where m is the number of columns and n is the number of rows.

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
    column_names : list[str]
        The column names of the table
    frame_per_point : float
        the number of frames per point.
    """

    def __init__(
        self,
        fpath,
        template,
        filename,
        key="/entry/data/data",
        column_names=None,
        frame_per_point=1,
    ):
        # I have included defaults for `key` and 'column_names' for back
        # compatibility with existing files at SIX.
        self._path = os.path.join(fpath, "")
        self._fpp = frame_per_point
        self._template = template
        self._filename = filename
        self._key = key
        self._column_names = column_names

    def _fnames_for_point(self, point_number):
        start = int(point_number * self._fpp)
        stop = int((point_number + 1) * self._fpp)
        for j in range(start, stop):
            yield self._template % (self._path, self._filename, j)

    def __call__(self, point_number):
        dfs = []
        import h5py

        for i, fn in enumerate(self._fnames_for_point(point_number)):
            with h5py.File(fn, "r") as f:
                dataframe = pd.DataFrame(f[self._key][:], columns=self._column_names)
                dataframe["frame"] = i
            dfs.append(dataframe)
        arr = numpy.empty(LENGTH, dtype=dtype)
        arr.fill(-1)  # 'frame' of -1 is our sentinel for "padding"
        records = pd.concat(dfs).to_records(
            column_dtypes={name: dtype for name, dtype in dtype_list}, index=False
        )
        assert records.dtype == arr.dtype
        arr[: len(records)] = records
        return arr

    def get_file_list(self, datum_kwargs):
        ret = []
        for d_kw in datum_kwargs:
            ret.extend(self._fnames_for_point(**d_kw))
        return ret
