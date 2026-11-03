import collections
import logging
import os
import bluesky.callbacks.mpl_plotting
import nslsii
import time as ttime
from databroker import Broker
from enum import Enum
from nslsii.sync_experiment import sync_experiment as sync_exp
from ophyd.signal import EpicsSignalBase
from tiled.client import from_profile
from bluesky_tiled_plugins import BufferingWrapper, TiledInserter, TiledWriter
from redis_json_dict import RedisJSONDict
from bluesky.run_engine import RunEngine


class ENDSTATION_ENUM(Enum):
    SIX = "six"
    Keithley = "keithley"

endstation_to_redis_db = {
    ENDSTATION_ENUM.SIX: 0,
    ENDSTATION_ENUM.Keithley: 1,
}


print("Please select an endstation from:")
for e in ENDSTATION_ENUM:
    print(f"\t- {e.name}")
endstation_choice = input("Enter your selection: ")
try:
    endstation = ENDSTATION_ENUM[endstation_choice]
except KeyError as e:
    raise Exception(
        f"Endstation choice '{endstation_choice}' is not one of the valid options."
    ) from e


def sync_experiment(proposal_number):
    sync_exp(proposal_number, beamline="six", redis_db=endstation_to_redis_db[endstation], redis_ssl=True)
    sync_write_paths()


def sync_write_paths():
    rixscam_wp = (
        f'Z:\\{RE.md["cycle"]}\\{RE.md["data_session"]}\\assets\\rixscam\\%Y\\%m\\%d\\'
    )
    rixscam_rp = f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam/%Y/%m/%d'
    rixscam_root = f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/rixscam'
    prosilica_wp = f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/prosilica/%Y/%m/%d'
    prosilica_root = f'/nsls2/data/six/proposals/{RE.md["cycle"]}/{RE.md["data_session"]}/assets/prosilica'

    rixscam.hdf5.write_path_template = rixscam_wp
    rixscam.hdf5.read_path_template = rixscam_rp
    rixscam.hdf5.reg_root = rixscam_root
    #rixscam.hdf2.write_path_template = rixscam_wp  # Commented out Oct. 8, 2026 as we no longer use
    #rixscam.hdf2.read_path_template = rixscam_rp
    #rixscam.hdf2.reg_root = rixscam_root

    diagon_h_cam.hdf5.write_path_template = prosilica_wp
    diagon_h_cam.hdf5.reg_root = prosilica_root
    m3_diag_cam.hdf5.write_path_template = prosilica_wp
    m3_diag_cam.hdf5.reg_root = prosilica_root
    extslt_cam.hdf5.write_path_template = prosilica_wp
    extslt_cam.hdf5.reg_root = prosilica_root
    gc_diag_cam.hdf5.write_path_template = prosilica_wp
    gc_diag_cam.hdf5.reg_root = prosilica_root
    sc_navitar_cam.hdf5.write_path_template = prosilica_wp
    sc_navitar_cam.hdf5.reg_root = prosilica_root
    sc_questar_cam.hdf5.write_path_template = prosilica_wp
    sc_questar_cam.hdf5.reg_root = prosilica_root


TILED_BACKUP_ROOT = "/nsls2/data/six/shared/config/bluesky/tiled_backup"
# Define tiled catalog
tiled_writing_client = from_profile(
    "nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SIX"], timeout={"connect": 5, "read": 120, "write": 120, "pool": 5} # Added Oct. 8, 2026
)["six"]
tiled_writing_client_raw = tiled_writing_client["raw"]
tiled_writing_client_raw.context.http_client.headers['tiled-qos'] = 'acquisition'
tiled_writing_client_sql = tiled_writing_client["migration"]
tiled_writing_client_sql.context.http_client.headers['tiled-qos'] = 'acquisition'
tiled_inserter = TiledInserter(
    tiled_writing_client_raw,
    "six",
    backup_directory=f"{TILED_BACKUP_ROOT}/raw",
)
tiled_inserter = BufferingWrapper(tiled_inserter)  # in-process queue: RE never blocks
tw = TiledWriter(
        tiled_writing_client_sql,
        backup_directory=f"{TILED_BACKUP_ROOT}/sql",
        spec_to_mimetype={
            "AD_HDF5": "application/x-hdf5",
            "AD_TIFF": "multipart/related;type=image/tiff",
        })
tw = BufferingWrapper(tw)  # in-process queue: RE never blocks


def flush_tiled(timeout=30):
    """Block until all queued documents have been written to Tiled.

    Documents are written to Tiled in background threads. Call this before
    reading back a run that was just taken.

    Raises RuntimeError if a buffer does not drain within ``timeout``
    seconds or its worker thread has died.
    """
    for label, buffer in (("raw", tiled_inserter), ("migration", tw)):
        if not buffer.flush(timeout):
            raise RuntimeError(
                f"Tiled {label} buffer was not flushed within {timeout} s "
                "(timed out or its worker thread died)."
            )
tiled_reading_client_raw = from_profile("nsls2")["six"]["raw"]
c = tiled_reading_client_sql = from_profile("nsls2")["six"]["migration"]
c.context.http_client.headers['tiled-qos'] = 'acquisition'
db = Broker(tiled_reading_client_raw)


# check the current logged in + active user
def whoami():
    try:
        print(f"\nLogged in to Tiled as: {c.context.whoami()['identities'][0]['id']}\n")
    except TypeError as e:
        print("\nNot authenticated with Tiled! Please login...\n")
    print(f"To login as a different user, call 'c.login()'")


# check the currently active proposal
def whichproposal():
    try:
        print(f"\nThe currently active proposal is: {RE.md['data_session']}\n")
    except KeyError as e:
        print("\nNo active proposal! Please activate a proposal...\n")
    print(
        f"To activate a different proposal, use 'sync_experiment(proposal_number_here)'"
    )


EpicsSignalBase.set_defaults(timeout=10, connection_timeout=10)
nslsii.configure_base(
    get_ipython().user_ns,
    tiled_inserter,
    bec=False,
    publish_documents_with_kafka=False,
    redis_url="xf02id1-six-redis1.nsls2.bnl.gov",
    redis_port=6380,
    redis_ssl=True,
    redis_db=endstation_to_redis_db[endstation],
)
RE.subscribe(tw)


class _RunTracker:
    """Remember the scan_id and start/stop times of recent runs, by start uid.

    The Tiled writers are buffered, so a run may not be in Tiled yet when a
    plan reads it back. Plans that only need a run's scan_id or times get them
    from here instead of from ``db``. The RunEngine calls subscribers before
    ``open_run``/``close_run`` return, so a uid returned by a scan plan is
    already known here. Only the uid, scan_id and two timestamps are kept,
    for at most ``maxlen`` runs started by this session's RunEngine.
    """

    def __init__(self, maxlen=10_000):
        self._maxlen = maxlen
        self._runs = collections.OrderedDict()

    def __call__(self, name, doc):
        # Never raise: an exception in a subscriber would abort the scan.
        try:
            if name == "start":
                self._runs[doc["uid"]] = {
                    "scan_id": doc.get("scan_id"),
                    "start_time": doc.get("time"),
                    "stop_time": None,
                }
                while len(self._runs) > self._maxlen:
                    self._runs.popitem(last=False)
            elif name == "stop":
                run = self._runs.get(doc.get("run_start"))
                if run is not None:
                    run["stop_time"] = doc.get("time")
        except Exception:
            logging.getLogger(__name__).exception("_RunTracker failed on %r", name)

    def _get(self, uid):
        """Look up by start uid, or by negative index (-1 = latest run)."""
        if isinstance(uid, int) and uid < 0:
            try:
                return list(self._runs.values())[uid]
            except IndexError:
                raise KeyError(
                    f"Fewer than {-uid} runs started in this session"
                ) from None
        try:
            return self._runs[uid]
        except KeyError:
            raise KeyError(
                f"Run {uid!r} was not started in this session (or is too old); "
                "read it from db instead"
            ) from None

    def scan_id_of(self, uid):
        return self._get(uid)["scan_id"]

    def run_times(self, uid):
        run = self._get(uid)
        return run["start_time"], run["stop_time"]


_run_tracker = _RunTracker()
RE.subscribe(_run_tracker)
scan_id_of = _run_tracker.scan_id_of  # scan_id_of(uid) or scan_id_of(-1)
run_times = _run_tracker.run_times  # run_times(uid) -> (start_time, stop_time)

# this has been uncommented based on TS
nslsii.configure_kafka_publisher(RE, beamline_name="six")

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

print("#" * 50)
whoami()
whichproposal()
print()
print("#" * 50)
