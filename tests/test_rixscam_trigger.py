import ast
from pathlib import Path
from threading import RLock, Timer
import time as ttime
from unittest.mock import MagicMock, patch

import numpy as np
import pytest
from bluesky import RunEngine
from bluesky.plans import count
from bluesky.utils import FailedStatus
from ophyd import Component as Cpt, Device, Signal
from ophyd.areadetector.trigger_mixins import SingleTrigger
from ophyd.device import Staged
from ophyd.status import Status


source_path = Path(__file__).parents[1] / "startup" / "22-rixscam.py"
with source_path.open() as source_file:
    source_tree = ast.parse(source_file.read())
trigger_class = next(node for node in source_tree.body
                     if isinstance(node, ast.ClassDef)
                     and node.name == "RIXSSingleTrigger")
namespace = dict(SingleTrigger=SingleTrigger, Staged=Staged, Status=Status,
                 RLock=RLock, Timer=Timer, np=np, ttime=ttime)
exec(compile(ast.Module(body=[trigger_class], type_ignores=[]),
             str(source_path), "exec"), namespace)


class SimCamera(Device):
    acquire = Cpt(Signal, value=0)
    image_mode = Cpt(Signal, value=1)
    array_counter = Cpt(Signal, value=0)
    num_images = Cpt(Signal, value=1)
    acquire_time = Cpt(Signal, value=0)
    acquire_period = Cpt(Signal, value=0)


class SimImage(Device):
    array_data = Cpt(Signal, value=np.empty((7, 0)))


class SimStorage(Device):
    def generate_datum(self, *args):
        pass


class SimRIXSCam(namespace["RIXSSingleTrigger"], Device):
    cam = Cpt(SimCamera, "")
    image2 = Cpt(SimImage, "")
    hdf5 = Cpt(SimStorage, "")
    centroid_enable = Cpt(Signal, value=False)
    xip_centroid_columns = (
        "x", "y", "x_eta", "y_eta", "y_eta_iso", "sum_regions", "XIP_mode",
    )


@pytest.fixture
def camera():
    detector = SimRIXSCam(name="rixscam", read_attrs=[])
    yield detector
    detector.unstage()


@pytest.mark.parametrize("centroid_enabled", [False, True])
def test_stuck_acquisition_fails_and_stops(camera, centroid_enabled):
    camera.centroid_enable.put(centroid_enabled)
    camera.acquisition_timeout_margin = 0.02
    camera.stage()
    status = camera.trigger()
    with pytest.raises(RuntimeError, match="(?i)camera was stuck in acquire mode, scan terminated"):
        status.wait(timeout=2)
    assert camera.cam.acquire.get() == 0
    assert camera._centroid_status is None
    assert camera._acquisition_timer is None


@pytest.mark.parametrize("centroid_enabled", [False, True])
def test_normal_completion_cancels_timeout(camera, centroid_enabled):
    camera.centroid_enable.put(centroid_enabled)
    camera.stage()
    status = camera.trigger()
    acquisition_status = camera._status
    if centroid_enabled:
        camera.image2.array_data.put(np.ones((7, 2)))
    camera.cam.acquire.put(0)
    status.wait(timeout=2)
    camera._acquisition_timed_out(acquisition_status)
    assert status.success
    assert camera._acquisition_timer is None


@pytest.mark.parametrize("exposure, period, frames, duration", [
    (2, 3, 4, 12), (3, 2, 4, 12), (2, 3, 1, 3),
])
def test_deadline_includes_expected_duration(camera, exposure, period, frames, duration):
    camera.cam.acquire_time.put(exposure)
    camera.cam.acquire_period.put(period)
    camera.cam.num_images.put(frames)
    camera.stage()
    with patch.dict(namespace, Timer=MagicMock()):
        camera.trigger()
        assert namespace["Timer"].call_args.args[0] == duration + 30


def test_old_timeout_cannot_stop_new_trigger(camera):
    camera.stage()
    first_status = camera.trigger()
    camera.cam.acquire.put(0)
    first_status.wait(timeout=2)
    second_status = camera.trigger()
    camera._acquisition_timed_out(first_status)
    assert camera.cam.acquire.get() == 1
    assert not second_status.done
    camera.cam.acquire.put(0)
    second_status.wait(timeout=2)


def test_camera_completion_does_not_timeout_pending_centroids(camera):
    camera.centroid_enable.put(True)
    camera.stage()
    status = camera.trigger()
    acquisition_status = camera._status
    camera.cam.acquire.put(0)
    camera._acquisition_timed_out(acquisition_status)
    assert camera._acquisition_timer is None
    assert not status.done
    camera.image2.array_data.put(np.ones((7, 2)))
    status.wait(timeout=2)


def test_timeout_still_fails_when_stop_write_fails(camera, caplog):
    camera.centroid_enable.put(True)
    camera.stage()
    status = camera.trigger()
    with patch.object(camera.cam.acquire, "put", side_effect=TimeoutError("IOC unavailable")) as stop_write:
        camera._acquisition_timed_out(camera._status)
    with pytest.raises(RuntimeError, match="(?i)camera was stuck in acquire mode"):
        status.wait(timeout=2)
    stop_write.assert_called_once_with(0, wait=False, timeout=1.0)
    assert camera._centroid_status is None
    assert camera._acquisition_timer is None
    assert "Could not stop camera acquisition" in caplog.text


@pytest.mark.parametrize("cleanup", ["stop", "unstage"])
def test_cleanup_releases_pending_statuses(camera, cleanup):
    camera.centroid_enable.put(True)
    camera.stage()
    status = camera.trigger()
    getattr(camera, cleanup)()
    with pytest.raises(RuntimeError, match="(?i)camera acquisition"):
        status.wait(timeout=2)
    assert camera.cam.acquire.get() == 0
    assert camera._acquisition_timer is None
    assert camera._centroid_status is None


def test_run_engine_terminates_and_unstages(camera):
    camera.centroid_enable.put(True)
    camera.acquisition_timeout_margin = 0.02
    engine = RunEngine({})
    documents = []
    engine.subscribe(lambda name, doc: documents.append((name, doc)))
    with pytest.raises(FailedStatus) as failure:
        engine(count([camera]))
    assert "camera was stuck in acquire mode, scan terminated" in str(failure.value.__cause__).lower()
    assert camera._staged == Staged.no
    assert camera.cam.acquire.get() == 0
    assert camera._centroid_subscription is None
    assert engine.state == "idle"
    assert not any(name == "event" for name, doc in documents)
    stop_document = next(doc for name, doc in documents if name == "stop")
    assert stop_document["exit_status"] == "fail"