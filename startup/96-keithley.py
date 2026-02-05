from ophyd import (
    Device,
    Component as Cpt,
    EpicsSignal,
    EpicsSignalRO,
    Kind,
    PVPositioner,
    PVPositionerPC,
)


class Keithley2600BVoltage(PVPositionerPC):
    """PVPositioner for direct Keithley 2600B voltage control (immediate)."""

    setpoint = Cpt(EpicsSignal, 'SP-VLvl')
    readback = Cpt(EpicsSignalRO, 'RB-VLvl')


class Keithley2600BCurrent(PVPositionerPC):
    """PVPositioner for direct Keithley 2600B current control (immediate)."""

    setpoint = Cpt(EpicsSignal, 'SP-ILvl')
    readback = Cpt(EpicsSignalRO, 'RB-ILvl')


class Keithley2600BVoltageRamped(PVPositioner):
    """PVPositioner for ramped Keithley 2600B voltage control (speed-controlled)."""

    setpoint = Cpt(EpicsSignal, 'Val:SP-E_u')
    readback = Cpt(EpicsSignalRO, 'RB-VLvl')
    done = Cpt(EpicsSignalRO, 'DMOV-E')
    done_value = 1


class Keithley2600BCurrentRamped(PVPositioner):
    """PVPositioner for ramped Keithley 2600B current control (speed-controlled)."""

    setpoint = Cpt(EpicsSignal, 'Val:SP-I_u')
    readback = Cpt(EpicsSignalRO, 'RB-ILvl')
    done = Cpt(EpicsSignalRO, 'DMOV-I')
    done_value = 1


class Keithley2600BChannel(Device):
    """Ophyd device for Keithley 2600B Source Meter single channel."""

    # ===== Identification =====
    identity = Cpt(EpicsSignalRO, 'Val:Idnt-I', kind=Kind.config)

    # ===== Output Control =====
    output_enable = Cpt(EpicsSignal, 'Cmd:Out-Ena', kind=Kind.config)
    output_status = Cpt(EpicsSignalRO, 'Sts:Out-Ena', kind=Kind.normal)
    abort = Cpt(EpicsSignal, 'Cmd:Abort', kind=Kind.omitted)

    # ===== Source Function =====
    source_select = Cpt(EpicsSignal, 'Sour-Sel', kind=Kind.config)
    source_status = Cpt(EpicsSignalRO, 'Sour:Sts', kind=Kind.normal)

    # ===== Voltage Control =====
    # Direct (immediate) control
    voltage = Cpt(Keithley2600BVoltage, '')
    # Ramped (speed-controlled) control
    voltage_ramped = Cpt(Keithley2600BVoltageRamped, '')
    voltage_ramp_speed = Cpt(EpicsSignal, 'Speed-E', kind=Kind.config)
    voltage_ramp_stop = Cpt(EpicsSignal, 'STOP-E', kind=Kind.omitted)
    voltage_limit_setpoint = Cpt(EpicsSignal, 'SP-LimV', kind=Kind.config)
    voltage_limit_readback = Cpt(EpicsSignalRO, 'RB-LimV', kind=Kind.config)

    # ===== Current Control =====
    # Direct (immediate) control
    current = Cpt(Keithley2600BCurrent, '')
    # Ramped (speed-controlled) control
    current_ramped = Cpt(Keithley2600BCurrentRamped, '')
    current_ramp_speed = Cpt(EpicsSignal, 'Speed-I', kind=Kind.config)
    current_ramp_stop = Cpt(EpicsSignal, 'STOP-I', kind=Kind.omitted)
    current_limit_setpoint = Cpt(EpicsSignal, 'SP-LimI', kind=Kind.config)
    current_limit_readback = Cpt(EpicsSignalRO, 'RB-LimI', kind=Kind.config)

    # ===== Measurement Readbacks =====
    measure_mode = Cpt(EpicsSignal, 'Meas-Sel', kind=Kind.config)
    measured_voltage = Cpt(EpicsSignalRO, 'RB-MeasV', kind=Kind.hinted)
    measured_current = Cpt(EpicsSignalRO, 'RB-MeasI', kind=Kind.hinted)
    measured_resistance = Cpt(EpicsSignalRO, 'RB-MeasR', kind=Kind.normal)
    measured_power = Cpt(EpicsSignalRO, 'RB-MeasP', kind=Kind.normal)

    # ===== Source Auto Range =====
    source_auto_range_voltage_sp = Cpt(EpicsSignal, 'SP-SourAutoRangV', kind=Kind.config)
    source_auto_range_voltage_sts = Cpt(EpicsSignalRO, 'Sts:SourAutoRangV', kind=Kind.config)
    source_auto_range_current_sp = Cpt(EpicsSignal, 'SP-SourAutoRangI', kind=Kind.config)
    source_auto_range_current_sts = Cpt(EpicsSignalRO, 'Sts:SourAutoRangI', kind=Kind.config)

    # ===== Measure Auto Range =====
    meas_auto_range_voltage_sp = Cpt(EpicsSignal, 'SP-MeasAutoRangV', kind=Kind.config)
    meas_auto_range_voltage_sts = Cpt(EpicsSignalRO, 'Sts:MeasAutoRangV', kind=Kind.config)
    meas_auto_range_current_sp = Cpt(EpicsSignal, 'SP-MeasAutoRangI', kind=Kind.config)
    meas_auto_range_current_sts = Cpt(EpicsSignalRO, 'Sts:MeasAutoRangI', kind=Kind.config)

    # ===== Source Range =====
    source_range_voltage_sp = Cpt(EpicsSignal, 'SP-SourVRang', kind=Kind.config)
    source_range_voltage_sts = Cpt(EpicsSignalRO, 'Sts-SourVRang', kind=Kind.config)
    source_range_current_sp = Cpt(EpicsSignal, 'SP-SourIRang', kind=Kind.config)
    source_range_current_sts = Cpt(EpicsSignalRO, 'Sts-SourIRang', kind=Kind.config)

    # ===== Measure Range =====
    meas_range_voltage_sp = Cpt(EpicsSignal, 'SP-MeasVRang', kind=Kind.config)
    meas_range_voltage_sts = Cpt(EpicsSignalRO, 'Sts-MeasVRang', kind=Kind.config)
    meas_range_current_sp = Cpt(EpicsSignal, 'SP-MeasIRang', kind=Kind.config)
    meas_range_current_sts = Cpt(EpicsSignalRO, 'Sts-MeasIRang', kind=Kind.config)

    # ===== Pulse Configuration =====
    pulse_current_bias = Cpt(EpicsSignal, 'PIMV-CurrBias', kind=Kind.config)
    pulse_current_level = Cpt(EpicsSignal, 'PIMV-CurrLevl', kind=Kind.config)
    pulse_voltage_limit = Cpt(EpicsSignal, 'PIMV-VLim', kind=Kind.config)
    pulse_time_on = Cpt(EpicsSignal, 'PIMV-TOn', kind=Kind.config)
    pulse_time_off = Cpt(EpicsSignal, 'PIMV-TOff', kind=Kind.config)
    pulse_count = Cpt(EpicsSignal, 'PIMV-NPuls', kind=Kind.config)
    configure_pulse_current = Cpt(EpicsSignal, 'Conf-PulseI', kind=Kind.omitted)
    configure_pulse_current_status = Cpt(EpicsSignalRO, 'Conf-PulseI-Sts', kind=Kind.omitted)
    configure_pulse_voltage = Cpt(EpicsSignalRO, 'Conf-PulseV', kind=Kind.omitted)
    run_pulse = Cpt(EpicsSignalRO, 'Cmd-Pulse', kind=Kind.omitted)
    pulse_buffer = Cpt(EpicsSignalRO, 'Prev-Buf', kind=Kind.normal)

    # ===== Test Commands =====
    load_beep_test = Cpt(EpicsSignal, 'Cmd:LoadBeepTest', kind=Kind.omitted)
    run_beep_test = Cpt(EpicsSignal, 'Cmd:BeepTest', kind=Kind.omitted)


# Keithley 1 Channel A
k2600b_1a = Keithley2600BChannel('XF:02IDD{K2636B:1-ChA}', name='k2600b_1a')

# Keithley 1 Channel B
k2600b_1b = Keithley2600BChannel('XF:02IDD{K2636B:1-ChB}', name='k2600b_1b')

# Keithley 2 Channel A
k2600b_2a = Keithley2600BChannel('XF:02IDD{K2636B:2-ChA}', name='k2600b_2a')

# Keithley 2 Channel B
k2600b_2b = Keithley2600BChannel('XF:02IDD{K2636B:2-ChB}', name='k2600b_2b')
