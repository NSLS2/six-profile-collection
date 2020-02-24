import bluesky
from ophyd import Device, EpicsMotor
from ophyd import Component as Cpt
import datetime

class align_class():

    '''
    Defines class for alignment scans.

    Defines all attribute functions to align the beamline.

    '''


    @property
    def m3pit(self):
        '''
        Aligns mirror M3 in three scans with increasing accuracy.

        Performs M3.pit scan detected at gcdiag.grid in three scans with decreasing range and exit slits, but increasing accuracy.

        Parameters
        ----------
        position : float, output
            position of the peak found after each M3 pitch scan, and is printed to the command line.

        '''
        initial_position = m3.pit.user_readback.value
        num = [31] # all lists here should have the same length, corresponding to the number of scan performed
        start = [ -0.001]
        stop = [ 0.001]
        vertical = 30
        horizontal = [ 75]

        initial_vertical = extslt.vg.position
        initial_horizontal = extslt.hg.position
        initial_gcdiagy = gcdiag.y.position


        yield from gcdiag.grid
        yield from mv(extslt.vg,vertical)

        for i in range(0, len(start)):
            yield from mv(extslt.hg, horizontal[i])
            peaks = bluesky.callbacks.fitting.PeakStats(m3.pit.name, 'gc_diag_grid')
            uid = yield from bpp.subs_wrapper(rel_scan([gcdiag.qem], m3.pit, start[i], stop[i], num[i]), peaks)
            print(f'!!!! our peaks for m3pit: {peaks.cen}')
            if uid is not None:
                if peaks['cen'] is not None:
                    yield from mv(m3.pit, peaks.cen)
                else:
                    peaks_not_found()  # raises an exception
                print('For scan {} of {} the center is {}'.format(i+1, len(start), peaks.cen))
            else:
                print ("m3.pit -> peaks.cen")
                print("For scan {} of {} the center is peaks.cen".format(i+1, len(start)))

        #yield from mv(extslt.vg, initial_vertical, extslt.hg, initial_horizontal,gcdiag.y,initial_gcdiagy)
        yield from mv(extslt.vg, initial_vertical, extslt.hg, initial_horizontal,gcdiag.y,-1)

    @property
    def m1pit(self):
        '''
        Aligns mirror M1 in three scans with increasing accuracy.

        Performs M1.pit scan detected at m3diag.yag in three scans with decreasing range and exit slits, but increasing accuracy.

        Parameters
        ----------
        position : float, output
            position of the peak found after each M1 pitch scan, and is printed to the command line.

        '''

        initial_position = m1.pit.user_readback.value
        num = [ 89] # all lists here should have the same length, corresponding to the number of scan performed
        start = [ -110]
        stop = [ 110]
        roi1_minx = [ 604] #592
        roi1_sizex = [ 20] #44
        roi1_miny = [ 370] #592
        roi1_sizey = [ 200] #44

        initial_m3diag = m3diag.y.position


        yield from m3diag.yag
        yield from count([m3diag.cam])

        for i in range(0, len(start)):
            yield from mv(m3diag.cam.roi1_minx, roi1_minx[i], m3diag.cam.roi1_sizex, roi1_sizex[i], m3diag.cam.roi1_miny, roi1_miny[i], m3diag.cam.roi1_sizey, roi1_sizey[i])
            peaks = bluesky.callbacks.fitting.PeakStats(m1.pit.name, 'm3_diag_cam_stats1_total')
            uid = yield from bpp.subs_wrapper(rel_scan([m3diag.cam], m1.pit, start[i], stop[i], num[i]), peaks)
            print(f'!!!! our peaks for m1pit: {peaks.cen}')
            if uid is not None:
                if peaks['cen'] is not None:
                    yield from mv(m1.pit, peaks.cen)   #peaks.max['m3_diag_cam_stats1_total'][0]
                else:
                    peaks_not_found()  # raises an exception
                print('For scan {} of {} the center is {}'.format(i+1, len(start), peaks.cen))
                print('\t moved from {} to {}'.format(initial_position, peaks.cen))
            else:
                print ("m1.pit -> peaks.cen")
                print("For scan {} of {} the center is peaks.cen".format(i+1, len(start)))

        yield from count([m3diag.cam])

        yield from m3diag.out

align = align_class()
