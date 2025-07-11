import os
import bluesky.callbacks.mpl_plotting
import nslsii
import time as ttime
from databroker import Broker
from enum import Enum
from nslsii.sync_experiment import sync_experiment as sync_exp
from ophyd.signal import EpicsSignalBase
from tiled.client import from_profile


class ENDSTATION_ENUM(Enum):
    SIX = "six-"
    Keithley = "keithley-"


print("Please select an endstation from:")
for e in ENDSTATION_ENUM:
    print(f"\t- {e.name}")
endstation_choice = input("Enter your selection: ")
try:
    endstation_prefix = ENDSTATION_ENUM[endstation_choice]
except KeyError as e:
    raise Exception(
        f"Endstation choice '{endstation_choice}' is not one of the valid options."
    ) from e


def sync_experiment(proposal_number):
    sync_exp(proposal_number, beamline="six", prefix=endstation_prefix.value)
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
    rixscam.hdf2.write_path_template = rixscam_wp
    rixscam.hdf2.read_path_template = rixscam_rp
    rixscam.hdf2.reg_root = rixscam_root

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


class TiledInserter:
    def insert(self, name, doc):
        ATTEMPTS = 20
        error = None
        for attempt in range(ATTEMPTS):
            try:
                tiled_writing_client.post_document(name, doc)
            except Exception as exc:
                print("Document saving failure:", repr(exc))
                error = exc
            else:
                break
            ttime.sleep(2)
        else:
            # Out of attempts
            raise error


# Define tiled catalog
tiled_writing_client = from_profile(
    "nsls2", api_key=os.environ["TILED_BLUESKY_WRITING_API_KEY_SIX"]
)["six"]["raw"]
tiled_inserter = TiledInserter()
c = tiled_reading_client = from_profile("nsls2")["six"]["raw"]
db = Broker(c)


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
# nslsii.configure_base(
#    get_ipython().user_ns,
#    "six",
#    bec=False,
#    publish_documents_with_kafka=True,
#    redis_url="info.six.nsls2.bnl.gov",
# )
nslsii.configure_base(
    get_ipython().user_ns,
    tiled_inserter,
    bec=False,
    publish_documents_with_kafka=False,
    redis_url="info.six.nsls2.bnl.gov",
    redis_prefix=endstation_prefix.value,
)
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
