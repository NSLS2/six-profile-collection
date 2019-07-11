def single_image(grating_pitch,dets=[rixscam],exp_time=600,sample = 'NdNiO3'):
    yield from rixscam_extra_stage(exp_time)
    yield from mv(rixscam.cam.acquire_time, exp_time)
    yield from count(dets,  md = {'reason':'{} sample with grating_pitch = {} 100um vg'.format(sample, grating_pitch)})
    yield from rixscam_extra_unstage()

