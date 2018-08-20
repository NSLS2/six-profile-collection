def m1_align_fine_temp():

    m1x_init=0.46
    m1pit_init=1980
    m1pit_start=1850
    m1pit_step=50

    for i in range(0,6):
        yield from mv(m1.pit,m1pit_start+i*m1pit_step)
        yield from scan([qem05],m1.x,-3.5,3.5,36)
        yield from mv(m1.x,-3.5)
    yield from mv(m1.pit,m1pit_start)

def alignM3x_temp():
    # get things out of the way
    yield from m3diag.out
    # read gas cell diode
    yield from gcdiag.grid

    # set detector e.g. gas cell diagnostics qem
    detList=[qem07]
    # set V exit slit value to get enough signal
    yield from mv(extslt.vg, 30)
    # open H slit full open
    yield from mv(extslt.hg, 9000)

    #move extslt.hs appropriately and scan m3.x
    yield from mv(extslt.hc,-9)
    yield from relative_scan(detList,m3.x,-6,6,61)

    yield from mv(extslt.hc,-3)
    yield from relative_scan(detList,m3.x,-6,6,61)
    yield from mv(extslt.hc,3)
    yield from relative_scan(detList,m3.x,-6,6,61)


def m4_cryo_z_vfocus():
    d11=[qem11]
    cryo_z_ref=7
    cryo_z_init=1
    cryo_z_final=17
    cryo_z_step=1
    
    for i in range(0,17):
        yield from mv(cryo.z,cryo_z_init+i*cryo_z_step)
        yield from sleep(10)
        yield from mv(cryo.x,38.7-(i-6)*0.147/2)
        yield from mv(cryo.y,96.098) # to be adjusted   94.57 @z=1
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.15,0.15,91)

        yield from mv(cryo.y,peaks['cen']['sc_diode_1']-1) 
        yield from mv(cryo.x,40.24-(i-6)*0.147/2) # to be adjusted 40.76 @z=1 38.55 @z=31 40.02 @z=11
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.x,-0.15,0.15,91)
    yield from mv(cryo.z,cryo_z_ref)

def m4_cryo_z_vfocus_2():
    #FE SLITS closed to 0.75mmx0.75mm and epu.gap=39mm
    yield from mv(epu1.gap,39)
    yield from mv(feslt.hg,0.75)
    yield from mv(feslt.vg,0.75)

    d11=[qem11]
    cryo_z_ref=11
    cryo_z_init=1
    cryo_z_final=31
    cryo_z_step=2
    
    for i in range(0,17):
        yield from mv(cryo.z,cryo_z_init+(i+15)*cryo_z_step)
        yield from sleep(10)
        yield from mv(cryo.x,39.2-(i+15)*0.147)
        yield from mv(cryo.y,95.97) # to be adjusted   94.57 @z=1
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.15,0.15,91)

    #for i in range(0,16):
    #    yield from mv(cryo.z,cryo_z_init+i*cryo_z_step)
    #    yield from mv(cryo.y,94.97) 
    #    yield from mv(cryo.x,40.6-i*0.147) # to be adjusted 40.76 @z=1 38.55 @z=31 40.02 @z=11
    #    yield from sleep(10)
    #    yield from rel_scan([qem11],cryo.x,-0.15,0.15,91)

    yield from mv(epu1.gap,38)
    yield from mv(feslt.hg,2.5)
    yield from mv(feslt.vg,2.5)

def m4_y():
    m4_y_start=96.875
    m4_y_step=0.1
    
#    for i in range(0, 25):
#    for i in range(21, 25):
    for i in range(0, 21):
        yield from mv(m4.y,m4_y_start+(i-10)*m4_y_step)
        yield from sleep(10)
        yield from mv(cryo.x,38)
        yield from mv(cryo.y,95.92+(i-10)*m4_y_step*1.2) # to be adjusted
        #yield from rel_scan([qem11],cryo.y,-1,1,21)
        #yield from mv(cryo.y,peaks['cen']['sc_diode_1'])
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.15,0.15,91)

        #yield from mv(cryo.y,peaks['cen']['sc_diode_1']-1)
        #yield from mv(cryo.x,40.45) # to be adjusted
        #yield from sleep(30)
        #yield from rel_scan([qem11],cryo.x,-2,2,21)
        #yield from sleep(30)
        #yield from mv(cryo.x,peaks['cen']['sc_diode_1'])
        #yield from sleep(30)
        #yield from rel_scan([qem11],cryo.x,-0.5,0.5,101)
    
    yield from mv(m4.y,m4_y_start)


def m4_y_m4slt_m4roll():
    m4_y_start=96.585
    m4_y_step=0.1
    m4slt_bot_start=4.54
    m4slt_top_start=-8.8
    yield from mv(m4slt.bot,0)
    yield from mv(m4slt.top,0)
    for i in range(0, 21):
        yield from mv(m4.y,m4_y_start+(i-10)*m4_y_step)
        yield from sleep(10)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.120+(i-10)*m4_y_step*1.2) # to be adjusted
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.15,0.15,101)

    yield from mv(m4.y,m4_y_start)
    m4slt_step=0.1
    for i in range(0, 12):
        yield from mv(m4slt.bot,m4slt_bot_start+(i-5)*m4slt_step)
        yield from mv(m4slt.top,m4slt_top_start+(i-5)*m4slt_step)
        yield from sleep(10)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.120) # to be adjusted
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.10,0.10,81)

    yield from mv(m4slt.bot,0)
    yield from mv(m4slt.top,0)

    mir4_rol_init = 2.5520
    mir4_rol_step= 0.002
    for i in range(0, 9):
        yield from mv(m4.rol,mir4_rol_init+mir4_rol_step*(i-4))
        yield from sleep(30)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.120) 
        yield from sleep(30)
        yield from rel_scan([qem11],cryo.y,-0.1,0.1,61)
        yield from mv(cryo.y,peaks['cen']['sc_diode_1']-1) 
        yield from mv(cryo.x,40.75) 
        yield from sleep(30)
        yield from rel_scan([qem11],cryo.x,-0.1,0.1,61)


def m4slt_h():
    m4_y_start=96.685
    m4slt_bot_start=5.04
    m4slt_top_start=-8.3
    m4slt_out_start=0
    m4slt_inb_start=10
    yield from mv(m4slt.bot,0)
    yield from mv(m4slt.top,0)

    yield from mv(m4.y,m4_y_start)
    m4slt_step=0.1
    for i in range(0, 13):
        yield from mv(m4slt.inb,m4slt_inb_start+(i-6)*m4slt_step)
        yield from mv(m4slt.out,m4slt_out_start+(i-6)*m4slt_step)
        yield from sleep(10)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.22) # to be adjusted
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.10,0.10,81)

    yield from mv(m4slt.bot,5.04)
    yield from mv(m4slt.top,-8.3)
    for i in range(0, 13):
        yield from mv(m4slt.inb,m4slt_inb_start+(i-6)*m4slt_step)
        yield from mv(m4slt.out,m4slt_out_start+(i-6)*m4slt_step)
        yield from sleep(10)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.22) # to be adjusted
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.10,0.10,81)
    yield from mv(m4slt.bot,0)
    yield from mv(m4slt.top,0)
    yield from mv(m4slt.inb,5)
    yield from mv(m4slt.out,5)

def m4_roll():  
    cryo.x.settle_time=1
    cryo.y.settle_time=1
    d11 = [qem11]
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    mir4_rol_init = 2.558
    mir4_rol_step= 0.002

    for i in range(0, 9):
        yield from mv(m4.rol,mir4_rol_init+mir4_rol_step*(i-4))
        yield from sleep(30)
        yield from mv(cryo.x,39.25)
        yield from mv(cryo.y,96.230) 
        yield from sleep(30)
        yield from rel_scan(d11,cryo.y,-0.1,0.1,61)
        #yield from mv(cryo.y,peaks['cen']['sc_diode_1']-1) 
        #yield from mv(cryo.x,40.75) 
        #yield from sleep(30)
        #yield from rel_scan(d11,cryo.x,-0.1,0.1,61)

def m4_yaw():  
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    d11 = [qem11]
    yield from mv(extslt.vg,10)
    yield from mv(extslt.hg,150)
    mir4_yaw_init = -1.1962
    mir4_yaw_step= 0.0015

    for i in range(0, 4):
        yield from mv(m4.yaw,mir4_yaw_init+mir4_yaw_step*(-i-5))
        yield from sleep(10)
        yield from mv(cryo.x,38)
        yield from mv(cryo.y,95.92)
        #yield from rel_scan([qem11],cryo.y,-0.5,0.5,16)
        #yield from mv(cryo.y,peaks['cen']['sc_diode_1'])
        yield from sleep(10)
        yield from rel_scan([qem11],cryo.y,-0.075,0.075,51) 
        #yield from mv(cryo.y,peaks['cen']['sc_diode_1']-1) 
        #yield from mv(cryo.x,40.00) 
        #yield from sleep(30)
        #yield from rel_scan(d11,cryo.x,-0.10,0.10,61)


def m4_pit():
    cryo.x.settle_time=0.2
    cryo.y.settle_time=0.2
    d11 = [qem11]
    yield from mv(extslt.vg,30)
    yield from mv(extslt.hg,150)
    mir4_pit_init = -4.056
    mir4_pit_step= 0.002

    for i in range(0, 5):
        yield from mv(m4.pit,mir4_pit_init+mir4_pit_step*(1*i))
        yield from sleep(30)
        yield from mv(cryo.x,38)
        yield from mv(cryo.y,95.97) # to be adjusted
        #yield from rel_scan(d11,cryo.y,-1.5,1,11)
        #yield from mv(cryo.y,peaks['cen']['sc_diode_1'])
        yield from sleep(30)
        yield from rel_scan(d11,cryo.y,-0.1,0.1,61)
        #yield from mv(cryo.y,93.5)
        #yield from mv(cryo.x,40.55+0.0873*(1*i-5))
        #yield from mv(cryo.x,42.7) # to be adjusted
        #yield from sleep(30)
        #yield from rel_scan(d11,cryo.x,-0.2,0.2,91)




