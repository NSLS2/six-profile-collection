# Make ophyd listen to pyepics.
from ophyd import setup_ophyd
from functools import partial
from pyOlog import SimpleOlogClient
from bluesky.callbacks.olog import logbook_cb_factory

setup_ophyd()


# Connect to metadatastore and filestore.
from metadatastore.mds import MDS, MDSRO
from filestore.fs import FileStoreRO
from databroker import Broker
mds_config = {'host': 'xf02id1-ca1',
              'port': 27017,
              'database': 'metadatastore-production-v1',
              'timezone': 'US/Eastern'}
fs_config = {'host': 'xf02id1-ca1',
             'port': 27017,
             'database': 'filestore-production-v1'}
mds = MDS(mds_config)
mds_readonly = MDS(mds_config)
fs_readonly = FileStoreRO(fs_config)
db = Broker(mds_readonly, fs_readonly)

from databroker.core import register_builtin_handlers
register_builtin_handlers(db.fs)

# Subscribe metadatastore to documents.
# If this is removed, data is not saved to metadatastore.
from bluesky.global_state import gs
gs.RE.subscribe('all', mds.insert)

# Import matplotlib and put it in interactive mode.
import matplotlib.pyplot as plt
plt.ion()

# Make plots update live while scans run.
from bluesky.utils import install_qt_kicker
install_qt_kicker()

# Optional: set any metadata that rarely changes.
# RE.md['beamline_id'] = 'YOUR_BEAMLINE_HERE'

# convenience imports
from ophyd.commands import *
from bluesky.callbacks import *
from bluesky.spec_api import *
import bluesky.plans as bp
from bluesky.global_state import gs, abort, stop, resume
from time import sleep
import numpy as np

RE = gs.RE  # convenience alias

# Uncomment the following lines to turn on verbose messages for debugging.
# import logging
# ophyd.logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG)


LOGBOOKS = ['Data Acquisition']    # list of logbook names to publish to
simple_olog_client = SimpleOlogClient()
generic_logbook_func = simple_olog_client.log
configured_logbook_func = partial(generic_logbook_func, logbooks=LOGBOOKS)

cb = logbook_cb_factory(configured_logbook_func)
RE.subscribe('start', cb)

# This is for ophyd.commands.get_logbook, which simply looks for
# a variable called 'logbook' in the global IPython namespace.
logbook = simple_olog_client

# Adding this for more convienient tools

from bluesky.plan_tools import print_summary

from bluesky.callbacks.scientific import PeakStats
from bluesky.callbacks.scientific import plot_peak_stats

# New figure title so no overplot.
def relabel_fig(fig, new_label):
    fig.set_label(new_label)
    fig.canvas.manager.set_window_title(fig.get_label())
