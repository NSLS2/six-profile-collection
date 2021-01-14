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


voltage_dc_B = EpicsSignal('XF:02IDD{K2611:1B}SP-VLvl', name = 'voltage_dc_B')
current_dc_B = EpicsSignal('XF:02IDD{K2611:1B}SP-ILvl', name='current_dc_B')
keithley_output_B = EpicsSignal('XF:02IDD{K2611:1B}Cmd:Out-Ena', name = 'keithley_output_B')
current_rbk_B = EpicsSignal('XF:02IDD{K2611:1B}RB-MeasI', name = 'current_rbk_B')
voltage_rbk_B = EpicsSignal('XF:02IDD{K2611:1B}RB-MeasV',name='voltage_rbk_B')
current_pulse_B = EpicsSignal('XF:02IDD{K2611:1B}PIMV-CurrLevl', name = 'current_pulse_B')
time_pulse_B = EpicsSignal('XF:02IDD{K2611:1B}PIMV-TOn', name = 'time_pulse_B')
interval_pulse_B = EpicsSignal('XF:02IDD{K2611:1B}Cmd-Pulse.SCAN', name = 'interval_pulse_B')
voltage_pulse_rbk_B = EpicsSignal('XF:02IDD{K2611:1B}Prev-Buf', name = 'voltage_pulse_rbk_B')
