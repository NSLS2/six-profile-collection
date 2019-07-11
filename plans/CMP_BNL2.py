RE.md['proposal'] =  '303063'
RE.md['sample'] = 'K-NiO'

def my_plan_overnight():
    



    Ei_vals = np.arange(580,586.1,0.1)
    m7_pit_vals = None #[5.4210,  5.4210]#
    
    #thetas = [15, 30]
    #zs = [16.45, 17.47 ]

    yield from rixscam_acquire(Ei_vals,m7_pit_vals, 1, 'H', 'puck B-1, sample 1' )

    #for in range(len(thetas)):
        #yield from mv(cryo.t, thetas[i], cryo.z, zs[i] )
        #yield from rixscam_energies_2(12, 'H')


def plan_first_night():
    
    m7_pit_vals = None

    #yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(850,853.0,0.1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'H', 'sample 1 - Pol H' )
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(853,856.09,0.1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'H', 'sample 1 - Pol H' )

    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(850,853.0,0.1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'V', 'sample 1 - Pol V' )
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(853,856.09,0.1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'V', 'sample 1 - Pol V' )

