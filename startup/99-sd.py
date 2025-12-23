sd.baseline = [ring_curr, gcpress,
epu1.gap, epu1.phase, 
feslt.hc, feslt.vc, feslt.hg, feslt.vg, 
m1.x, m1.pit, m1.rol, 
pgm.cff, pgm.en, pgm.grx, pgm.m2pit, pgm.grpit, pgm.grlines, 
m3slt.hs, m3slt.ha, m3slt.vs, m3slt.va,
m3diag,
m3.x, m3.y, m3.z, m3.yaw, m3.pit, m3.rol,
extslt.hg, extslt.vg, extslt.hc, 
gcdiag, 
m4_diag1,
m4slt.inb, m4slt.out, m4slt.bot, m4slt.top, 
m4.x, m4.y, m4.z, m4.yaw, m4.pit, m4.rol,
cryo.x, cryo.y, cryo.z, cryo.t, 
ow,
m5.x, m5.y, m5.z, m5.yaw, m5.pit, m5.rol,
m5mask, m6_msk,
m6.pit, m6.z,
espgm.cff, espgm.en, espgm.m7pit, espgm.grpit, espgm.grxrb, espgmmask, #espgm.grx,
oc.y, oc.z, oc.roll, oc.twoth,
dcslt.inb,dcslt.out,dcslt.bot,dcslt.top,
dc.z, dc.twoth]


sd.baseline = [ring_curr, 
gcpress, # voltage_dc, current_rbk,
epu1, 
feslt, 
m1, 
pgm,
pgm.grlines, #added on 12/15/2020 DOESN'T WORK
m3slt,
m3diag,
m3,
extslt,
gcdiag, 
m4_diag1,
m4slt, 
m4,
cryo,
stemp.temp.A.T, #this doesn't work
stemp.temp.B.T, #this doesn't work
stemp.ctrl2.readback, #this just puts in the setpoint readback
ow,
m5,
m5mask, m6_msk,
m6,
espgm.m7pit, espgm.grpit, espgm.grx, 
espgmmask, # espgm.cff, espgm.e
#espgm.grlines, #added on 12/15/2020 DOESN'T WORK
oc,
dcslt,
dc,
]


optional = [
"voltage_dc_1A",
"current_dc_1A",
"voltage_dc_sp_rbk_1A",
"current_dc_sp_rbk_1A",
"current_rbk_1A",
"voltage_rbk_1A",
"current_pulse_1A",
"time_pulse_1A",
"interval_pulse_1A",
"voltage_pulse_rbk_1A",
"voltage_dc_1B",
"current_dc_1B",
"voltage_dc_sp_rbk_1B",
"current_dc_sp_rbk_1B",
"current_rbk_1B",
"voltage_rbk_1B",
"current_pulse_1B",
"time_pulse_1B",
"interval_pulse_1B",
"voltage_pulse_rbk_1B"
]

for device_name in optional:
    try:
        # Get the device if it is defined.
        device = globals()[device_name]
    except KeyError:
        # Skip it; it's probably unplugged.
        print(f"Omitting {device_name} from baseline readings because it is not defined.")
        pass
    else:
        sd.baseline.append(device)

# To avoid baseline are printed on screen:
# bec.disable_baseline()%

