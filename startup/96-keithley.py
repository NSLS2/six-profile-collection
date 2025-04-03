from ophyd import EpicsSignal


voltage_dc_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}SP-VLvl', name = 'voltage_dc_1A')
current_dc_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}SP-ILvl', name='current_dc_1A')
voltage_dc_sp_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-VLvl', name = 'voltage_dc_sp_rbk_1A')
current_dc_sp_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-ILvl', name='current_dc_sp_rbk_1A')
keithley_output_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}Cmd:Out-Ena', name = 'keithley_output_1A')
current_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasI', name = 'current_rbk_1A')
voltage_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasV',name='voltage_rbk_1A')
resistance_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}RB-MeasR',name='resistance_rbk_1A')
current_pulse_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}PIMV-CurrLevl', name = 'current_pulse_1A')
meaure_mode_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}Meas-Sel', name = 'measure_mode_1A')
time_pulse_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}PIMV-TOn', name = 'time_pulse_1A')
interval_pulse_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}Cmd-Pulse.SCAN', name = 'interval_pulse_1A')
voltage_pulse_rbk_1A = EpicsSignal('XF:02IDD{K2636B:1-ChA}Prev-Buf', name = 'voltage_pulse_rbk_1A')


voltage_dc_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}SP-VLvl', name = 'voltage_dc_1B')
current_dc_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}SP-ILvl', name='current_dc_1B')
voltage_dc_sp_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-VLvl', name = 'voltage_dc_sp_rbk_1B')
current_dc_sp_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-ILvl', name='current_dc_sp_rbk_1B')
keithley_output_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Cmd:Out-Ena', name = 'keithley_output_1B')
current_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasI', name = 'current_rbk_1B')
voltage_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasV',name='voltage_rbk_1B')
resistance_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}RB-MeasR',name='resistance_rbk_1B')
meaure_mode_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Meas-Sel', name = 'measure_mode_1B') ########## FIX THIS #########
current_pulse_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}PIMV-CurrLevl', name = 'current_pulse_1B')
time_pulse_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}PIMV-TOn', name = 'time_pulse_1B')
interval_pulse_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Cmd-Pulse.SCAN', name = 'interval_pulse_1B')
voltage_pulse_rbk_1B = EpicsSignal('XF:02IDD{K2636B:1-ChB}Prev-Buf', name = 'voltage_pulse_rbk_1B')



voltage_dc_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}SP-VLvl', name = 'voltage_dc_2A')
current_dc_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}SP-ILvl', name='current_dc_2A')
voltage_dc_sp_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}RB-VLvl', name = 'voltage_dc_sp_rbk_2A')
current_dc_sp_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}RB-ILvl', name='current_dc_sp_rbk_2A')
keithley_output_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}Cmd:Out-Ena', name = 'keithley_output_2A')
current_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}RB-MeasI', name = 'current_rbk_2A')
voltage_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}RB-MeasV',name='voltage_rbk_2A')
resistance_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}RB-MeasR',name='resistance_rbk_2A')
current_pulse_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}PIMV-CurrLevl', name = 'current_pulse_2A')
meaure_mode_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}Meas-Sel', name = 'measure_mode_2A')
time_pulse_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}PIMV-TOn', name = 'time_pulse_2A')
interval_pulse_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}Cmd-Pulse.SCAN', name = 'interval_pulse_2A')
voltage_pulse_rbk_2A = EpicsSignal('XF:02IDD{K2636B:2-ChA}Prev-Buf', name = 'voltage_pulse_rbk_2A')


voltage_dc_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}SP-VLvl', name = 'voltage_dc_2B')
current_dc_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}SP-ILvl', name='current_dc_2B')
voltage_dc_sp_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}RB-VLvl', name = 'voltage_dc_sp_rbk_2B')
current_dc_sp_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}RB-ILvl', name='current_dc_sp_rbk_2B')
keithley_output_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}Cmd:Out-Ena', name = 'keithley_output_2B')
current_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}RB-MeasI', name = 'current_rbk_2B')
voltage_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}RB-MeasV',name='voltage_rbk_2B')
resistance_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}RB-MeasR',name='resistance_rbk_2B')
meaure_mode_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}Meas-Sel', name = 'measure_mode_2B')
current_pulse_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}PIMV-CurrLevl', name = 'current_pulse_2B')
time_pulse_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}PIMV-TOn', name = 'time_pulse_2B')
interval_pulse_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}Cmd-Pulse.SCAN', name = 'interval_pulse_2B')
voltage_pulse_rbk_2B = EpicsSignal('XF:02IDD{K2636B:2-ChB}Prev-Buf', name = 'voltage_pulse_rbk_2B')

#temperature_cryostat = EpicsSignal('XF:02IDD-ES{TCtrl:1-Chan:B}T-I', name = 'temperature_cryostat')
#temperature_sample = EpicsSignal('XF:02IDD-ES{TCtrl:1-Chan:A}T-I', name = 'temperature_sample')

