from ophyd import (
    Device,
    Component as Cpt,
    EpicsSignal,
    EpicsSignalRO,
    Kind,
    PVPositioner,
    PVPositionerPC,
)

# Map EPICS SCAN field string values to seconds
SCAN_PERIOD_MAP = {
    "Passive": 0,
    "Event": 0,
    "I/O Intr": 0,
    "300 second": 300.0,
    "240 second": 240.0,
    "180 second": 180.0,
    "120 second": 120.0,
    "60 second": 60.0,
    "30 second": 30.0,
    "10 second": 10.0,
    "5 second": 5.0,
    "2 second": 2.0,
    "1 second": 1.0,
    ".5 second": 0.5,
    ".2 second": 0.2,
    ".1 second": 0.1,
}


class Keithley2600BPositionerMixin:
    """Mixin that gets settle_time from the parent channel's measurement scan period."""

    def _get_settle_time(self):
        """Get the effective settle time."""
        settle_time_config = getattr(self, '_settle_time', 0.0)
        if settle_time_config == 0.0 and self.parent is not None and hasattr(self.parent, 'meas_scan_period'):
            scan_str = self.parent.meas_scan_period.get()
            return SCAN_PERIOD_MAP.get(scan_str, 1.0)
        return settle_time_config

    def move(self, position, wait=True, **kwargs):
        """Override move to use dynamic settle_time from parent's meas_scan_period."""
        # Temporarily set _settle_time to our computed value
        original_settle_time = self._settle_time
        self._settle_time = self._get_settle_time()
        try:
            return super().move(position, wait=wait, **kwargs)
        finally:
            # Restore original value
            self._settle_time = original_settle_time


class Keithley2600BVoltage(Keithley2600BPositionerMixin, PVPositionerPC):
    """PVPositioner for direct Keithley 2600B voltage control (immediate)."""

    setpoint = Cpt(EpicsSignal, 'SP-VLvl')
    readback = Cpt(EpicsSignalRO, 'RB-VLvl')


class Keithley2600BCurrent(Keithley2600BPositionerMixin, PVPositionerPC):
    """PVPositioner for direct Keithley 2600B current control (immediate)."""

    setpoint = Cpt(EpicsSignal, 'SP-ILvl')
    readback = Cpt(EpicsSignalRO, 'RB-ILvl')


class Keithley2600BVoltageLimit(PVPositionerPC):
    """PVPositioner for Keithley 2600B voltage limit control."""
    setpoint = Cpt(EpicsSignal, 'SP-LimV')
    readback = Cpt(EpicsSignalRO, 'RB-LimV')


class Keithley2600BCurrentLimit(PVPositionerPC):
    """PVPositioner for Keithley 2600B current limit control."""
    setpoint = Cpt(EpicsSignal, 'SP-LimI')
    readback = Cpt(EpicsSignalRO, 'RB-LimI')


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
    voltage = Cpt(Keithley2600BVoltage, '')
    voltage_limit = Cpt(Keithley2600BVoltageLimit, '')

    # ===== Current Control =====
    current = Cpt(Keithley2600BCurrent, '')
    current_limit = Cpt(Keithley2600BCurrentLimit, '')

    # ===== Measurement Readbacks =====
    measure_mode = Cpt(EpicsSignal, 'Meas-Sel', kind=Kind.config)
    measured_voltage = Cpt(EpicsSignalRO, 'RB-MeasV', kind=Kind.hinted)
    measured_current = Cpt(EpicsSignalRO, 'RB-MeasI', kind=Kind.hinted)
    measured_resistance = Cpt(EpicsSignalRO, 'RB-MeasR', kind=Kind.normal)
    measured_power = Cpt(EpicsSignalRO, 'RB-MeasP', kind=Kind.normal)
    # Measurement scan period - used for settle_time in voltage/current positioners
    meas_scan_period = Cpt(EpicsSignalRO, '_MeasCho1.SCAN', kind=Kind.config, string=True)

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


# Keithley 1 Channel A
k2600b_1a = Keithley2600BChannel('XF:02IDD{K2636B:1-ChA}', name='k2600b_1a')

# Keithley 1 Channel B
k2600b_1b = Keithley2600BChannel('XF:02IDD{K2636B:1-ChB}', name='k2600b_1b')

# Keithley 2 Channel A
k2600b_2a = Keithley2600BChannel('XF:02IDD{K2636B:2-ChA}', name='k2600b_2a')

# Keithley 2 Channel B
k2600b_2b = Keithley2600BChannel('XF:02IDD{K2636B:2-ChB}', name='k2600b_2b')
