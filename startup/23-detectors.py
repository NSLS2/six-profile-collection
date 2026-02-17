# this startup file is for misc. detectors and monitors


from ophyd import (EpicsSignal, EpicsSignalRO, EpicsScaler, Device, Kind)
from ophyd import Component as Cpt


ring_curr = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_curr')

gcpress = EpicsSignalRO('XF:02IDC-VA{BT:16-TCG:16_1}P-I', name = 'gc_tcg_pressure') 


#sclr = ScalerCH('XF:02ID1-ES:1{Sclr:1}scaler1', name = 'sclr')
sclr = EpicsScaler('XF:02ID1-ES:1{Sclr:1}scaler1', name = 'sclr')


for chan in sclr.channels.read_attrs:
    chanNUM = getattr(sclr.channels, chan)
    chanNUM.kind = Kind.omitted

sclr.channels.chan1.kind = Kind.normal #this is the time base
sclr.channels.chan2.kind = Kind.hinted #this is the first detector channel on the scalar card. - changed these to 
sclr.channels.chan6.kind = Kind.hinted #
sclr.channels.chan8.kind = Kind.hinted #

def sclr_enable():
    sclr.channels.chan2.kind = Kind.hinted
    sclr.channels.chan6.kind = Kind.hinted
    sclr.channels.chan8.kind = Kind.hinted

def sclr_disable():
    sclr.channels.chan2.kind = Kind.normal
    sclr.channels.chan6.kind = Kind.normal
    sclr.channels.chan8.kind = Kind.normal


# Femtoanalyzer via GPIO (EK9000)
# we added this on 02/05/2026
class Femtoanalyzer(Device):
    signal = Cpt(EpicsSignalRO, '1}AI:Ch1-I', kind=Kind.hinted)
    gain_bit0 = Cpt(EpicsSignal, '11}DO:Ch1-Cmd', kind=Kind.config)  # Pin10 Least Significant Bit 
    gain_bit1 = Cpt(EpicsSignal, '11}DO:Ch2-Cmd', kind=Kind.config)  # Pin11
    gain_bit2 = Cpt(EpicsSignal, '11}DO:Ch3-Cmd', kind=Kind.config)  # Pin12
    gain_bit3 = Cpt(EpicsSignal, '11}DO:Ch4-Cmd', kind=Kind.config)  # Pin13 Most Significant Bit 

femto = Femtoanalyzer(prefix="XF:02ID1-ES{GPIO:1_", name="femto")

