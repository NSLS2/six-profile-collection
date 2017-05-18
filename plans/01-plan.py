
def xassearch():
    for i in range(0, 7):
        yield from bp.mv(m4_diag1,-62-i*0.5)
        print('Moving m4_diag_1 to ',m4_diag1.user_readback.value)
        yield from a2scan(pgm.en,870,990,epu1.gap,39.05,41.8,240)

        

#pitch mirror 1
#change something
#scan again

#def myplan():
   # mir1[0.234,0.236,0.336]
   # for i range(0,4):
    #    yield from bp.mv(m1.pit,mir1[i])
    #   print('Moving M1 to ',m1.pit.user_readback.value)
    #    yield from bp.mv()
    #    yield from dscan(m3.pit,-0.2,0.22,0)
        # this should work below
    #    olog('Scan ID {} m3 pitch scan {}m1 pitch {} m3 trans'.format(db[-1].start.scan_id,m1.pit.user_readback.value,m3.x.user_readback.value))
        

#def myplan2(m1_stp,m3_stp):
   # m1_start = m1.pit.user_readback.value
   # m3_start = m3.x.user_readback.value
   # yield from bp.sleep(0.3)
   # for i range(0,4):
       # yield from bp.mv(m1.pit,m1_start+i*m1_stp,m3.x+i*m3_stp)
       # yield from dscan(m3.pit,-0.2,0.2,20)
        #olog()
    
