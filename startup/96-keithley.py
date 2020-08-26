from ophyd import EpicsSignal


voltage_dc = EpicsSignal('XF:02IDD{K2611:1}SP-VLvl', name = 'voltage_dc')
current_dc = EpicsSignal('XF:02IDD{K2611:1}SP-ILvl', name='current_dc')
keithley_output = EpicsSignal('XF:02IDD{K2611:1}Cmd:Out-Ena', name = 'keithley_output')
current_rbk = EpicsSignal('XF:02IDD{K2611:1}RB-MeasI', name = 'current_rbk')
voltage_rbk = EpicsSignal('XF:02IDD{K2611:1}RB-MeasV',name='voltage_rbk')
current_pulse = EpicsSignal('XF:02IDD{K2611:1}PIMV-CurrLevl', name = 'current_pulse')
time_pulse = EpicsSignal('XF:02IDD{K2611:1}PIMV-TOn', name = 'time_pulse')
interval_pulse = EpicsSignal('XF:02IDD{K2611:1}Cmd-Pulse.SCAN', name = 'interval_pulse')
voltage_pulse_rbk = EpicsSignal('XF:02IDD{K2611:1}Prev-Buf', name = 'voltage_pulse_rbk')

