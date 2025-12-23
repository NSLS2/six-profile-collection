from ophyd import Device, Component as Cpt, EpicsSignal, EpicsSignalRO


class M1HeatExchanger(Device):
    bypass_v = Cpt(EpicsSignal, "CVbp:Volts-SP")
    flow_v = Cpt(EpicsSignal, "CVs:Volts-SP")
    flow_m1 = Cpt(EpicsSignalRO, "F:1-I")

class PGMHeatExchanger(Device):
    bypass_v = Cpt(EpicsSignal, "{PGM:1-HTEX:1}CVbp:Volts-SP")
    flow_v = Cpt(EpicsSignal, "{PGM:1-HTEX:1}CVs:Volts-SP")
    flow_m2 = Cpt(EpicsSignalRO, "{Mir:2-HTEX:1}F:1-I")
    flow_pgm = Cpt(EpicsSignalRO, "{Mir:2-PGM:1}F:1-I")

m1_htex = M1HeatExchanger("XF:02IDA-CT{Mir:1-HTEX:1}")
pgm_htex = PGMHeatExchanger("XF:02IDB-CT")
