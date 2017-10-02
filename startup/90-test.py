## Some useful functions for remembering how to put diagnostics in the beam

# M3 diagnostic
# m3d means m3 diode in
def m3d_diode():
    return (yield from mv(m3_diag, -76.4))

# m3d_yag means m3 yag in
def m3d_yag():
    return (yield from mv(m3_diag, -49.4))

def m3d_grid():
    return (yield from mv(m3_diag, -97.5))

# m3d_out means m3diagnostic fully retracted
def m3d_out():
    return (yield from mv(m3_diag, -1))


            
# Gas Cell diagnostic
def gcd_yag():
    return (yield from mv(gc_diag, -43.4))

def gcd_diode():
    return (yield from mv(gc_diag, -71.4))

def gcd_grid():
    return (yield from mv(gc_diag, -95.4))

def gcd_out():
    return (yield from mv(gc_diag, -1))            

def master_plan():
    yield from m3d_diode()
    yield from ct()
    yield from m3d_out()
    yield from ct()



# Data export function
def save_scan2csv(first_id, last_id):
    for scanid in range(first_id, last_id+1,1):
        df=db.get_table(db[scanid])
        #df.to_csv('~/Scans/scan_%d.csv' % scanid)
        df.to_csv('~/Scans/scan_%d.csv' % scanid, columns=['pgm_en','pgm_en_user_setpoint','epu1_gap','epu1_gap_setpoint','rs_diag_1_tey']) #List here all the usefull columns that may be in the scan, to avoid saving time stamp, etc...




## spec count
def ct_bfl():
    print('top blade:\t',qem07.current1.mean_value.value)


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
    
