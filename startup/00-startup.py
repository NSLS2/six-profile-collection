import bluesky.callbacks.mpl_plotting
import nslsii
from ophyd.signal import EpicsSignalBase


EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)
nslsii.configure_base(
    get_ipython().user_ns,
    "six",
    bec=False,
    publish_documents_with_kafka=True,
    redis_url="info.six.nsls2.bnl.gov",
)

bluesky.callbacks.mpl_plotting.initialize_qt_teleporter()


def print_now():
    return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")


# After the above call, you will now have the following in your namespace:
#
# 	RE : RunEngine
# 	db : databroker
# 	sd : SupplementalData
# 	pbar_manager : ProgressBarManager
# 	bec : BestEffortCallback
# 	peaks : bec.peaks
# 	plt : matplotlib.pyplot
# 	np : numpy
# 	bc : bluesky.callbacks
# 	bp : bluesky.plans
# 	bps : bluesky.plan_stubs
# 	mv : bluesky.plan_stubs.mv
# 	mvr : bluesky.plan_stubs.mvr
# 	mov : bluesky.plan_stubs.mov
# 	movr : bluesky.plan_stubs.movr
# 	bpp : bluesky.preprocessors


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

mpl.rcParams["axes.grid"] = True


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
    msg = (
        f'\n{"="*80}\n'
        f"            No peaks were found. Calibration is not successful."
        f'\n{"="*80}\n'
    )
    print(msg)
    raise RuntimeError(msg)


import logging
