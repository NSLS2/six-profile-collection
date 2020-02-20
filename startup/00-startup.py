# DAMA hot fix to increase the set_and_wait() timeout to 5 seconds.
# See https://github.com/NSLS-II-SIX/profile_collection/issues/24 for the error report.

import nslsii
nslsii.configure_base(get_ipython().user_ns, 'six', bec=False)

from bluesky.log import current_handler
current_handler.setLevel('CRITICAL')

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
from bluesky.callbacks.best_effort import BestEffortCallback


def factory(name, doc):
    bec = BestEffortCallback()
    bec(name, doc)
    return [bec], []

rr = RunRouter([factory])
RE.subscribe(rr)
