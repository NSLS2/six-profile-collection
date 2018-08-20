def pol_V(offset=None):
    cur_mono_e = pgm.en.user_readback.value
    yield from mv(epu1.table,3)
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,28.5)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    print('\nFinished moving the polarization to vertical.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))

def pol_H(offset=None):
    cur_mono_e = pgm.en.user_readback.value
    yield from mv(epu1.table,1)
    if offset is not None:
        yield from mv(epu1.offset,offset)
    yield from mv(epu1.phase,0)
    yield from mv(pgm.en,cur_mono_e+1)  #TODO this is dirty trick.  figure out how to process epu.table.input
    yield from mv(pgm.en,cur_mono_e)
    print('\nFinished moving the polarization to horizontal.\n\tNote that the offset for epu calibration is {}eV.\n\n'.format(offset))


def m3_check():
    temp_extslt_vg=extslt.vg.user_readback.value
    temp_extslt_hg=extslt.hg.user_readback.value
    temp_gcdiag = gcdiag.y.user_readback.value
    yield from mv(qem07.averaging_time, 1)
    yield from mv(extslt.hg,10)
    yield from mv(extslt.vg,30)
    yield from gcdiag.grid
    yield from rel_scan([qem07],m3.pit,-0.0005,0.0005,31, md = {'reason':'checking m3 before cff'})
    yield from mv(m3.pit,peaks.cen['gc_diag_grid'])
    yield from mv(extslt.hg,temp_extslt_hg)
    yield from mv(extslt.vg,temp_extslt_vg)
    yield from mv(gcdiag.y,temp_gcdiag)


