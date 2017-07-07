
def xassearch():
    for i in range(0, 7):
        yield from bp.mv(m4_diag1,-62-i*0.5)
        print('Moving m4_diag_1 to ',m4_diag1.user_readback.value)
        yield from a2scan(pgm.en,870,990,epu1.gap,39.05,41.8,240)


def gascell2():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
        
    for i in range(0, 8):
        yield from bp.mv(extslt.vg,10+i*5)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402,epu1.gap,27.451,27.545,250)


def gascell_vs_cff2():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.601)
    yield from bp.sleep(10)
    yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,20)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,40)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)

    yield from bp.mv(extslt.vg,30)
    for i in range(0, 15):
        yield from bp.mv(pgm.cff,2.2598+i*0.01)
        yield from bp.mv(pgm.en,399,epu1.gap,27.601)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.601,27.72,290)
        

def gascell_vs_cff():
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(pgm.cff,2.3298)
    yield from bp.mv(pgm.en,399,epu1.gap,27.451)
    yield from bp.sleep(10)
    yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)
    
    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)

    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)

    for i in range(0, 21):
        yield from bp.mv(pgm.cff,2.0298+i*0.03)
        yield from bp.mv(pgm.en,399,epu1.gap,27.451)
        yield from bp.sleep(10)
        yield from a2scan(pgm.en,399,402.5,epu1.gap,27.451,27.56,290)
        

        

def FEscan2():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)
        
    yield from bp.mv(feslt.hg,0.33)
    yield from bp.mv(feslt.vg,0.33)
    yield from bp.mv(epu1.gap,41.3)
    
    for i in range(0, 5):
        yield from bp.mv(feslt.vc,0.66-0.33*i)
        for j in range(0, 5):
            yield from bp.mv(feslt.hc,0.66-0.33*j)
            yield from bp.mv(pgm.en,900)
            yield from bp.sleep(5)
            yield from ascan(pgm.en,900,970,70)


def FEscan3():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    for i in range(0, 7):
        yield from bp.mv(feslt.vc,0.6-0.2*i)
        for j in range(0, 7):
            yield from bp.mv(feslt.hc,0.6-0.2*j)
            yield from bp.mv(pgm.en,880)
            yield from bp.sleep(5)
            yield from ascan(pgm.en,880,960,80)     
   
def FEscan4():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)

    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    yield from bp.mv(feslt.vc,-0.6)
    for j in range(0, 7):
        yield from bp.mv(feslt.hc,0.6-0.2*j)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(5)
        yield from ascan(pgm.en,880,960,80)  

            
            
def FEscan():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)
        
    #yield from bp.mv(feslt.hg,1)
    #yield from bp.mv(feslt.vg,1)
    yield from bp.mv(epu1.gap,41.3)
    
    for i in range(0, 7):
        yield from bp.mv(feslt.vc,-3+i)
        for j in range(0, 7):
            yield from bp.mv(feslt.hc,-3+j)
            yield from bp.mv(pgm.en,900)
            yield from bp.sleep(10)
            yield from ascan(pgm.en,900,970,210)
  


def FEscan_gap():
    if feslt.hc not in gs.DETS:
        gs.DETS.append(feslt.hc)
    if feslt.vc not in gs.DETS:
        gs.DETS.append(feslt.vc)
    if feslt.hg not in gs.DETS:
        gs.DETS.append(feslt.hg)
    if feslt.vg not in gs.DETS:
        gs.DETS.append(feslt.vg)
    if epu1.gap not in gs.DETS:
        gs.DETS.append(epu1.gap)
    if extslt.vg not in gs.DETS:
        gs.DETS.append(extslt.vg)
    if pgm.cff not in gs.DETS:
        gs.DETS.append(pgm.cff)


    yield from bp.mv(feslt.hc,0)
    yield from bp.mv(feslt.vc,0)
    yield from bp.mv(epu1.gap,41.3)
    
 # Check Vertical Gap   
    yield from bp.mv(feslt.hg,1.5) 
    yield from bp.mv(feslt.vg,1.5)
    
    for i in range(0, 12):
        yield from bp.mv(feslt.vg,1.5-0.1*i)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(10)
        yield from ascan(pgm.en,880,960,80)     

 # Check Horizontal Gap   
    yield from bp.mv(feslt.hg,1.5) 
    yield from bp.mv(feslt.vg,1.5) 

    for i in range(0, 12):
        yield from bp.mv(feslt.hg,1.5-0.1*i)
        yield from bp.mv(pgm.en,880)
        yield from bp.sleep(10)
        yield from ascan(pgm.en,880,960,80)     

# Repeat FE Slit Center Search
    yield from bp.mv(feslt.hg,0.8) #feslt.hg=0.6 --> zero value
    yield from bp.mv(feslt.vg,0.8) #feslt.vg=0.6 --> zero value
    yield from bp.mv(epu1.gap,41.3)

    for i in range(0, 9):
        yield from bp.mv(feslt.vc,0.8-0.2*i)
        for j in range(0, 9):
            yield from bp.mv(feslt.hc,0.8-0.2*j)
            yield from bp.mv(pgm.en,880)
            yield from bp.sleep(10)
            yield from ascan(pgm.en,880,960,80) 



def Jun29lunch():
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    #feslt.vg is 0.2, fesl.hg is 1.5
    yield from ascan(pgm.en,880,960,80)
    yield from bp.mv(feslt.vg,1.5,feslt.hg,0.3)   
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    yield from ascan(pgm.en,880,960,80)
    yield from bp.mv(feslt.vg,1.5,feslt.hg,0.2)
    yield from bp.mv(pgm.en,880,epu1.gap,41.3)
    yield from bp.sleep(10)
    yield from ascan(pgm.en,880,960,80)


        
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
    
