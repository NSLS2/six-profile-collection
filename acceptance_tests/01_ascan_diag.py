from bluesky.plans import relative_scan
from bluesky.callbacks import LivePlot, LiveTable

RE(relative_scan([qem08], m4_diag1, -1, 1, 5),
   [LiveTable(['rs_diag_1_tey', 'm4_diag1']),
    LivePlot('rs_diag_1_tey', 'm4_diag1')])
