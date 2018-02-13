from ophyd import EpicsMotor

m3_diag = EpicsMotor('XF:02IDC-OP{Mir:3-Diag:12_U_1-Ax:1}Mtr',name='m3_diag')

gc_diag = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:16_U_1-Ax:1}Mtr',name='gc_diag')

m4_diag1 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:1}Mtr',name='m4_diag1')
m4_diag2 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:2}Mtr',name='m4_diag2')
m4_diag3 = EpicsMotor('XF:02IDC-OP{Mir:4-Diag:17_U_1-Ax:3}Mtr',name='m4_diag3')

m5_RPD = EpicsMotor('XF:02IDD-ES{Mir:5-Ax:RPD}Mtr', name='m5_RPD')

SC_QPD = EpicsMotor('XF:02IDD-ES{SC:1-Ax:QPD}Mtr', name='SC_QPD')
SC_IO = EpicsMotor('XF:02IDD-ES{SC:1-Ax:IO}Mtr', name='m5_RPD')
