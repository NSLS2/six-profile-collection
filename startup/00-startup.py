# DAMA hot fix to increase the set_and_wait() timeout to 5 seconds.
# See https://github.com/NSLS-II-SIX/profile_collection/issues/24 for the error report.

import nslsii
nslsii.configure_base(get_ipython().user_ns, 'six', bec=False)

# After the above call, you will now have the following in your namespace:
# 
#	RE : RunEngine 
#	db : databroker 
#	sd : SupplementalData
#	pbar_manager : ProgressBarManager
#	bec : BestEffortCallback
#	peaks : bec.peaks
#	plt : matplotlib.pyplot
#	np : numpy
#	bc : bluesky.callbacks
#	bp : bluesky.plans
#	bps : bluesky.plan_stubs
#	mv : bluesky.plan_stubs.mv
#	mvr : bluesky.plan_stubs.mvr
#	mov : bluesky.plan_stubs.mov
#	movr : bluesky.plan_stubs.movr
#	bpp : bluesky.preprocessors


# At the end of every run, verify that files were saved and
# print a confirmation message.
from bluesky.callbacks.broker import verify_files_saved
# RE.subscribe(post_run(verify_files_saved), 'stop')


# Optional: set any metadata that rarely changes.
# RE.md['beamline_id'] = 'YOUR_BEAMLINE_HERE'

# Uncomment the following lines to turn on verbose messages for
# debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)

# New figure title so no overplot.
def relabel_fig(fig, new_label):
    fig.set_label(new_label)
    fig.canvas.manager.set_window_title(fig.get_label())

# Implementing grid on plots:
import matplotlib as mpl
mpl.rcParams['axes.grid'] = True


from event_model import RunRouter
from bluesky.callbacks.best_effort import BestEffortCallback, PeakResults


peaks = PeakResults()


class _CustomBestEffortCallback(BestEffortCallback):

    def stop(self, doc):
        global peaks
        ret = super().stop(doc)
        peaks = self.peaks

        return ret


def factory(name, doc):
    bec = _CustomBestEffortCallback()
    bec(name, doc)
    return [bec], []

rr = RunRouter([factory])
RE.subscribe(rr)


def peaks_not_found():
    msg = (f'\n{"="*80}\n'
           f'            No peaks were found. Calibration is not successful.'
           f'\n{"="*80}\n')
    print(msg)
    raise RuntimeError(msg)


from pathlib import Path

import appdirs

try:
    from bluesky.utils import PersistentDict
except ImportError:
    import msgpack
    import msgpack_numpy
    import zict

    class PersistentDict(zict.Func):
        def __init__(self, directory):
            self._directory = directory
            self._file = zict.File(directory)
            super().__init__(self._dump, self._load, self._file)

        @property
        def directory(self):
            return self._directory

        def __repr__(self):
            return f"<{self.__class__.__name__} {dict(self)!r}>"

        @staticmethod
        def _dump(obj):
            "Encode as msgpack using numpy-aware encoder."
            # See https://github.com/msgpack/msgpack-python#string-and-binary-type
            # for more on use_bin_type.
            return msgpack.packb(
                obj,
                default=msgpack_numpy.encode,
                use_bin_type=True)

        @staticmethod
        def _load(file):
            return msgpack.unpackb(
                file,
                object_hook=msgpack_numpy.decode,
                raw=False)

runengine_metadata_dir = appdirs.user_data_dir(appname="bluesky") / Path("runengine-metadata")

# PersistentDict will create the directory if it does not exist
RE.md = PersistentDict(runengine_metadata_dir)


import logging
logging.getLogger('ophyd').setLevel('WARNING')  # ophyd is too verbose right now
