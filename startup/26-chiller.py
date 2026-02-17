from ophyd import Device, Component as Cpt, EpicsSignal, EpicsSignalRO, PVPositionerPC

class BypassPositioner(PVPositionerPC):
    setpoint = Cpt(EpicsSignal, "-SP")

class FlowPositioner(PVPositionerPC):
    setpoint = Cpt(EpicsSignal, "-SP")

class M1HeatExchanger(Device):
    # bypass_v = Cpt(EpicsSignal, "CVbp:Volts-SP")
    # flow_v = Cpt(EpicsSignal, "CVs:Volts-SP")
    # flow_m1 = Cpt(EpicsSignalRO, "F:1-I")
    
    bypass_v = Cpt(BypassPositioner, "CT{Mir:1-HTEX:1}CVbp:Volts")
    flow_v = Cpt(FlowPositioner, "CT{Mir:1-HTEX:1}CVs:Volts")
    flow_m1 = Cpt(EpicsSignalRO, "CT{Mir:1-HTEX:1}F:1-I")

    pressure_m1 = Cpt(EpicsSignalRO, "OP{Mir:1-WPG:1}DI-I")

class PGMHeatExchanger(Device):
    # bypass_v = Cpt(EpicsSignal, "{PGM:1-HTEX:1}CVbp:Volts-SP")
    # flow_v = Cpt(EpicsSignal, "{PGM:1-HTEX:1}CVs:Volts-SP")
    # flow_m2 = Cpt(EpicsSignalRO, "{Mir:2-HTEX:1}F:1-I")
    # flow_pgm = Cpt(EpicsSignalRO, "{Mir:2-PGM:1}F:1-I")

    flow_v = Cpt(FlowPositioner, "CT{PGM:1-HTEX:1}CVbp:Volts")
    bypass_v = Cpt(BypassPositioner, "CT{PGM:1-HTEX:1}CVs:Volts")
    flow_m2 = Cpt(EpicsSignalRO, "CT{Mir:2-HTEX:1}F:1-I")
    flow_pgm = Cpt(EpicsSignalRO, "CT{Mir:2-PGM:1}F:1-I")


    pressure_m2 = Cpt(EpicsSignalRO, "OP{Mir:2-WPG:1}DI-I")
    pressure_pgm = Cpt(EpicsSignalRO, "OP{Gratings-WPG:1}DI-I")

#m1_htex = M1HeatExchanger("XF:02IDA-CT{Mir:1-HTEX:1}", name="m1_htex")
m1_htex = M1HeatExchanger("XF:02IDA-", name="m1_htex")
# pgm_htex = PGMHeatExchanger("XF:02IDB-CT", name="pgm_htex")
pgm_htex = PGMHeatExchanger("XF:02IDB-", name="pgm_htex")
