# this startup file is for misc. detectors and monitors


from ophyd import (EpicsSignal, EpicsSignalRO, EpicsScaler)


ring_curr = EpicsSignalRO('SR:OPS-BI{DCCT:1}I:Real-I', name='ring_curr')

gcpress = EpicsSignalRO('XF:02IDC-VA{BT:16-TCG:16_1}P-I', name = 'gc_tcg_pressure') 


#sclr = ScalerCH('XF:02ID1-ES:1{Sclr:1}scaler1', name = 'sclr')
sclr = EpicsScaler('XF:02ID1-ES:1{Sclr:1}scaler1', name = 'sclr')

for chan in sclr.channels.read_attrs:
    chanNUM = getattr(sclr.channels, chan)
    chanNUM.kind = Kind.omitted

sclr.channels.chan1.kind = Kind.normal #this is the time base
sclr.channels.chan2.kind = Kind.hinted #this is the first detector channel on the scalar card.
sclr.channels.chan8.kind = Kind.hinted #
