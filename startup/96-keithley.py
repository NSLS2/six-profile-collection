from ophyd import EpicsSignal


voltage_dc = EpicsSignal('XF:02IDD{K2636B:1-ChA}SP-VLvl', name = 'voltage_dc')
current_dc = EpicsSignal('XF:02IDD{K2636B:1-ChA}SP-ILvl', name='current_dc')
keithley_output = EpicsSignal('XF:02IDD{K2636B:1-ChA}Cmd:Out-Ena', name = 'keithley_output')
current_rbk = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasI', name = 'current_rbk')
voltage_rbk = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasV',name='voltage_rbk')
resistance_rbk = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasR',name='resistance_rbk')
current_pulse = EpicsSignal('XF:02IDD{K2636B:1-ChA}PIMV-CurrLevl', name = 'current_pulse')
meaure_mode = EpicsSignal('XF:02IDD{K2636B:1-ChA}Meas-Sel', name = 'measure_mode')
time_pulse = EpicsSignal('XF:02IDD{K2636B:1-ChA}PIMV-TOn', name = 'time_pulse')
interval_pulse = EpicsSignal('XF:02IDD{K2636B:1-ChA}Cmd-Pulse.SCAN', name = 'interval_pulse')
voltage_pulse_rbk = EpicsSignal('XF:02IDD{K2636B:1-ChA}Prev-Buf', name = 'voltage_pulse_rbk')


voltage_dc_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}SP-VLvl', name = 'voltage_dc_B')
current_dc_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}SP-ILvl', name='current_dc_B')
keithley_output_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Cmd:Out-Ena', name = 'keithley_output_B')
current_rbk_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasI', name = 'current_rbk_B')
voltage_rbk_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasV',name='voltage_rbk_B')
resistance_rbk_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasR',name='resistance_rbk_B')
meaure_mode_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Meas-Sel', name = 'measure_mode_B')
current_pulse_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}PIMV-CurrLevl', name = 'current_pulse_B')
time_pulse_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}PIMV-TOn', name = 'time_pulse_B')
interval_pulse_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Cmd-Pulse.SCAN', name = 'interval_pulse_B')
voltage_pulse_rbk_B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Prev-Buf', name = 'voltage_pulse_rbk_B')

