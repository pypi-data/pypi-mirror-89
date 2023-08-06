"""
Methods for importing data from the Cassini spacecraft.
"""
import datetime
import os
import pathlib
import pandas as pd
import calendar
import astropy.units as u

from collections import OrderedDict
from heliopy.data import util
from heliopy import config

data_dir = pathlib.Path(config['download_dir'])
use_hdf = config['use_hdf']
cassini_dir = data_dir / 'cassini'

# These mappings from months to strings are used in directory names
month2str = {1: '001_031_JAN',
             2: '032_059_FEB',
             3: '060_090_MAR',
             4: '091_120_APR',
             5: '121_151_MAY',
             6: '152_181_JUN',
             7: '182_212_JUL',
             8: '213_243_AUG',
             9: '244_273_SEP',
             10: '274_304_OCT',
             11: '305_334_NOV',
             12: '335_365_DEC'}
leapmonth2str = {1: '001_031_JAN',
                 2: '032_060_FEB',
                 3: '061_091_MAR',
                 4: '092_121_APR',
                 5: '122_152_MAY',
                 6: '153_182_JUN',
                 7: '183_213_JUL',
                 8: '214_244_AUG',
                 9: '245_274_SEP',
                 10: '275_305_OCT',
                 11: '306_335_NOV',
                 12: '336_366_DEC'}


class _mag1minDownloader(util.Downloader):
    def __init__(self, coords):
        valid_coords = ['KRTP', 'KSM', 'KSO', 'RTN']
        if coords not in valid_coords:
            raise ValueError('coords must be one of {}'.format(valid_coords))
        self.coords = coords

        Rs = u.def_unit('saturnRad', 60268 * u.km)
        if (coords == 'KRTP'):
            self.units = OrderedDict([('Bx', u.nT), ('By', u.nT), ('Bz', u.nT),
                                      ('X', Rs), ('|B|', u.nT),
                                      ('Y', u.deg),
                                      ('Z', u.deg),
                                      ('Local hour', u.dimensionless_unscaled),
                                      ('n points', u.dimensionless_unscaled)])
        if (coords == 'RTN'):
            self.units = OrderedDict([('Bx', u.nT), ('By', u.nT), ('Bz', u.nT),
                                      ('X', u.AU), ('Y', u.AU), ('Z', u.AU),
                                      ('|B|', u.nT),
                                      ('Local hour', u.dimensionless_unscaled),
                                      ('n points', u.dimensionless_unscaled)])
        if (coords == 'KSM' or coords == 'KSO'):
            self.units = OrderedDict([('Bx', u.nT), ('By', u.nT), ('Bz', u.nT),
                                      ('X', Rs), ('Y', Rs), ('Z', Rs),
                                      ('|B|', u.nT),
                                      ('Local hour', u.dimensionless_unscaled),
                                      ('n points', u.dimensionless_unscaled)])

    def intervals(self, starttime, endtime):
        return self.intervals_yearly(starttime, endtime)

    def fname(self, interval):
        year = interval.start.strftime('%Y')
        return f'{year}_FGM_{self.coords}_1M.TAB'

    def local_dir(self, interval):
        return pathlib.Path('cassini') / 'mag' / '1min'

    def download(self, interval):
        local_dir = self.local_path(interval).parent
        local_dir.mkdir(parents=True, exist_ok=True)
        year = interval.start.strftime('%Y')
        base_url = ('http://pds-ppi.igpp.ucla.edu/ditdos/download?'
                    'id=pds://PPI/CO-E_SW_J_S-MAG-4-SUMM-1MINAVG-V2.0/DATA')
        url = '{}/{}'.format(base_url, year)
        util._download_remote(url,
                              self.fname(interval),
                              local_dir)

    def load_local_file(self, interval):
        f = open(self.local_path(interval))
        if 'error_message' in f.readline():
            f.close()
            os.remove(f.name)
            raise util.NoDataError()
        data = pd.read_csv(f,
                           names=['Time', 'Bx', 'By', 'Bz', '|B|',
                                  'X', 'Y', 'Z', 'Local hour', 'n points'],
                           delim_whitespace=True,
                           parse_dates=[0], index_col=0)
        f.close()
        return data


def mag_1min(starttime, endtime, coords):
    """
    Import 1 minute magnetic field from Cassini.

    See http://pds-ppi.igpp.ucla.edu/search/view/?f=yes&id=pds://PPI/CO-E_SW_J_S-MAG-4-SUMM-1MINAVG-V1.0
    for more information.

    Cassini Orbiter Magnetometer Calibrated MAG data in 1 minute averages
    available covering the period 1999-08-16 (DOY 228) to 2016-12-31 (DOY 366).
    The data are provided in RTN coordinates throughout the mission, with
    Earth, Jupiter, and Saturn centered coordinates for the respective
    flybys of those planets.

    Parameters
    ----------
    starttime : datetime.datetime
        Interval start time.
    endtime : datetime.datetime
        Interval end time.
    coords : str
        Requested coordinate system. Must be one of
        ``['KRTP', 'KSM', 'KSO', 'RTN']``

    Returns
    -------
    data : :class:`~sunpy.timeseries.GenericTimeSeries`
        Requested data
    """
    dl = _mag1minDownloader(coords)
    return dl.load(starttime, endtime)


def mag_hires(starttime, endtime, try_download=True):
    """
    Import high resolution magnetic field from Cassini.

    See http://pds-ppi.igpp.ucla.edu/search/view/?f=yes&id=pds://PPI/CO-E_SW_J_S-MAG-3-RDR-FULL-RES-V1.0
    for more information.

    Cassini Orbiter Magnetometer Calibrated MAG data at the highest time
    resolution available covering the period 1999-08-16 (DOY 228) to
    2016-12-31 (DOY 366).

    The data are in RTN coordinates prior Cassini's arrival at Saturn, and
    Kronographic (KRTP) coordinates at Saturn (beginning 2004-05-14, DOY 135).

    Parameters
    ----------
    starttime : datetime.datetime
        Interval start time.
    endtime : datetime.datetime
        Interval end time.

    Returns
    -------
    data : :class:`~sunpy.timeseries.GenericTimeSeries`
        Requested data
    """
    remote_base_url = ('http://pds-ppi.igpp.ucla.edu/ditdos/download?id='
                       'pds://PPI/CO-E_SW_J_S-MAG-3-RDR-FULL-RES-V2.0/DATA')
    dirs = []
    fnames = []
    extension = '.TAB'
    units = OrderedDict([('Bx', u.nT), ('By', u.nT), ('Bz', u.nT),
                         ('coords', u.dimensionless_unscaled)])
    local_base_dir = cassini_dir / 'mag' / 'hires'

    for [day, _, _] in util._daysplitinterval(starttime, endtime):
        year = day.year
        if calendar.isleap(year):
            monthstr = leapmonth2str[day.month]
        else:
            monthstr = month2str[day.month]

        if day < datetime.date(2004, 5, 14):
            coords = 'RTN'
        else:
            coords = 'KRTP'
        doy = day.strftime('%j')
        dirs.append(pathlib.Path(str(year)) / monthstr)
        fnames.append(str(year)[2:] + doy + '_FGM_{}'.format(coords))

    def download_func(remote_base_url, local_base_dir,
                      directory, fname, remote_fname, extension):
        url = remote_base_url + '/' + str(directory)
        util._download_remote(url, fname + extension,
                              local_base_dir / directory)

    def processing_func(f):
        if 'error_message' in f.readline():
            f.close()
            os.remove(f.name)
            raise util.NoDataError()
        df = pd.read_csv(f, names=['Time', 'Bx', 'By', 'Bz'],
                         delim_whitespace=True,
                         parse_dates=[0], index_col=0)
        return df

    return util.process(dirs, fnames, extension, local_base_dir,
                        remote_base_url, download_func, processing_func,
                        starttime, endtime, units=units,
                        try_download=try_download)
