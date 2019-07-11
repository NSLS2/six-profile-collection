RE.md['proposal'] =  '303063'
RE.md['sample'] = 'K-NiO'

bec.disable_baseline()  #disable print to screen of baseline tables


def my_plan_overnight():
    



    Ei_vals = np.arange(580,586.1,0.1)
    m7_pit_vals = None #[5.4210,  5.4210]#
    
    #thetas = [15, 30]
    #zs = [16.45, 17.47 ]

    yield from rixscam_acquire(Ei_vals,m7_pit_vals, 1, 'H', 'puck B-1, sample 1' )

    #for in range(len(thetas)):
        #yield from mv(cryo.t, thetas[i], cryo.z, zs[i] )
        #yield from rixscam_energies_2(12, 'H')





def plan_day28():
    
    c_tape =   [27.024,24.80,19.84]

    sample_1 = [27.054,28.2640,19.84]
    sample_2 = [27.054,28.2640-0.032,19.84]
    sample_3 = [27.054,28.2640-0.064,19.84]
    sample_4 = [27.054,28.2640-0.096,19.84]

    m7_pit_vals = None

    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)
    
    
    yield from align.m1pit
    yield from m3_check()
    yield from pol_V(3)
    Erange = [850,853,856.08]
    E_1 = list(np.arange(850,853.0,0.2))
    E_2 = list(np.arange(853,856.09,0.2))

    yield from mv(cryo.x, c_tape[0], c_tape[1], cryo.z, c_tape[2])
    yield from rixscam_acquire(E_1,m7_pit_vals,  1, None, 'sample 3 A ' )
    yield from rixscam_acquire(E_1,m7_pit_vals,  1, None, 'sample 3 A ' )
    yield from align.m1pit
    yield from m3_check()  

    yield from rixscam_acquire_sample_c_tape(E_2,m7_pit_vals, sample_4, c_tape, 1, None, 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from pol_H(0)

    yield from rixscam_acquire_sample_c_tape(E_1,m7_pit_vals, sample_1, c_tape, 1, None, 'sample 3 A ' )
    yield from align.m1pit
    yield from m3_check()  

    yield from rixscam_acquire_sample_c_tape(E_2,m7_pit_vals, sample_2, c_tape, 1, None, 'sample 3 A' )





def plan_night27b():
    
    c_tape =   [27.024,24.80,19.84]

    sample_1 = [27.054,28.2640,19.84]
    sample_2 = [27.054,28.2640-0.032,19.84]
    sample_3 = [27.054,28.2640-0.064,19.84]
    sample_4 = [27.054,28.2640-0.096,19.84]

    m7_pit_vals = None
    yield from mv(qem11.averaging_time, 60)
    yield from mv(qem12.averaging_time, 60)
    
    
    yield from align.m1pit
    yield from m3_check()
    yield from pol_V(3)
    E = list(np.arange(850,853.0,0.2))
    yield from rixscam_acquire_sample_c_tape(E,m7_pit_vals, sample_3, c_tape, 1, None, 'sample 3 A ' )
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(853,856.09,0.2))
    yield from rixscam_acquire_sample_c_tape(E,m7_pit_vals, sample_4, c_tape, 1, None, 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from pol_H(0)
    E = list(np.arange(850,853.0,0.2))
    yield from rixscam_acquire_sample_c_tape(E,m7_pit_vals, sample_1, c_tape, 1, None, 'sample 3 A ' )
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(853,856.09,0.2))
    yield from rixscam_acquire_sample_c_tape(E,m7_pit_vals, sample_2, c_tape, 1, None, 'sample 3 A' )


def plan_lunch_28():
    #yield from pol_H(0)
    #yield from align.m1pit
    #yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)  
    E = list(np.arange(853,856.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )

def plan_afternoon_28():
    #yield from pol_H(0)
    yield from align.m1pit
    yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)  
    E = list(np.arange(856.02,858,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)  
    E = list(np.arange(850,853.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )

def plan_evening_28():
    #yield from pol_V(3)
    #yield from align.m1pit
    #yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)  
    E = list(np.arange(850.0,854.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 300)
    yield from mv(qem11.averaging_time, 300)
    yield from mv(qem12.averaging_time, 300)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )
    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)


def plan_night_28(): 



    #SAMPLE 4 Puck B - NiO 4% K doped
    #yield from mv(cryo.x,26.6821)
    #yield from mv(cryo.y,75.2)
    #yield from mv(cryo.z,19.93)
    yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.00,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 4 B' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 4 B' )

    
    #SAMPLE 1 Puck B - NiO undoped
    yield from mv(cryo.x,26.1)
    yield from mv(cryo.y,72.0)
    yield from mv(cryo.z,15.82)
    #yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)


def plan_earlymorning_31():

    #SAMPLE 1 Puck B - NiO undoped
    yield from mv(cryo.x,25.9)
    yield from mv(cryo.y,70.9)
    yield from mv(cryo.z,15.35)
    #yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol V' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol V' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

    yield from pol_H(0)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol H' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol H' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_afternoon_31():

    #SAMPLE 1 Puck B - NiO undoped
    #yield from pol_V(3)
    #yield from align.m1pit
    #yield from m3_check()
    #yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol V' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B pol V' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_night_31():

    #SAMPLE 6 Puck top - NiO 32% (K, In)
    #yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    #yield from pol_H(0)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,852.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(852.0,854.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,856.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(856.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 6 A' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)


def plan_morning_1():

    #SAMPLE 3 Puck top - NiO 16% (K)
    #yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 5 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 5 A' )


def plan_evening_1():

    #SAMPLE 3 Puck top - NiO 16% (K)
    #yield from pol_V(3)
    #yield from align.m1pit
    #yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 3 A' )
   


def plan_morning_30(): 

   #SAMPLE 1 Puck B - NiO undoped
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_afternoon_30(): 

    #SAMPLE 1 Puck B - NiO undoped
    #yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(850.0,854,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(854.0,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)

def plan_evening_30(): 

    #SAMPLE 1 Puck B - NiO undoped

    yield from align.m1pit
    yield from m3_check()
    yield from sleep(30)
    m7_pit_vals = None
    yield from mv(rixscam.cam.acquire_time, 240)
    yield from mv(qem11.averaging_time, 240)
    yield from mv(qem12.averaging_time, 240)  
    E = list(np.arange(856.6,858.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, None, 'sample 1 B' )

    yield from mv(qem11.averaging_time, 1)
    yield from mv(qem12.averaging_time, 1)



def plan_lunch27():
    
    m7_pit_vals = None
    yield from pol_H(0)
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(850,856.09,1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'H', 'sample 3 puck 2 top - Pol H' )
    yield from pol_V(3)
    yield from align.m1pit
    yield from m3_check() 
    E = list(np.arange(850,856.09,1))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'V', 'sample 3 puck 2 top - Pol V' )


def plan_lunch27b():
    
    m7_pit_vals = None

    #yield from align.m1pit
    #yield from m3_check()  
    E = list(np.arange(850,853.0,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'H', 'sample 3 A ' )
    yield from align.m1pit
    yield from m3_check()  
    E = list(np.arange(853,856.09,0.2))
    yield from rixscam_acquire(E,m7_pit_vals, 1, 'H', 'sample 3 A' )

    yield from align.m1pit
    yield from m3_check()  
   # E = list(np.arange(850,853.0,0.2))
   # yield from rixscam_acquire(E,m7_pit_vals, 1, 'V', 'sample 3 A' )
   # yield from align.m1pit
   # yield from m3_check()  
   # E = list(np.arange(853,856.09,0.2))
   # yield from rixscam_acquire(E,m7_pit_vals, 1, 'V', 'sample 3 A' )


def tests():
    yield from gcdiag.grid
    yield from rixscam_acquire(Ei_vals,m7_pit_vals, 1, None, 'TEST' )
    yield from gcdiag.out

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

    

