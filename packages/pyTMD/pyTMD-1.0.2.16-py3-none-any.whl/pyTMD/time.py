#!/usr/bin/env python
u"""
time.py
Written by Tyler Sutterley (09/2020)
Utilities for calculating time operations

PYTHON DEPENDENCIES:
    numpy: Scientific Computing Tools For Python
        https://numpy.org
    dateutil: powerful extensions to datetime
        https://dateutil.readthedocs.io/en/stable/
    lxml: processing XML and HTML in Python
        https://pypi.python.org/pypi/lxml

PROGRAM DEPENDENCIES:
    convert_julian.py: returns the calendar date and time given a Julian date
    convert_calendar_decimal.py: converts from calendar dates into decimal years
    utilities: download and management utilities for syncing files

UPDATE HISTORY:
    Updated 09/2020: added wrapper function for merging Bulletin-A files
        can parse date strings in form "time-units since yyyy-mm-dd hh:mm:ss"
    Updated 08/2020: added NASA Earthdata routines for downloading from CDDIS
    Written 07/2020
"""
import os
import re
import datetime
import numpy as np
import dateutil.parser
import pyTMD.convert_julian
import pyTMD.convert_calendar_decimal
import pyTMD.utilities

#-- PURPOSE: parse a date string into epoch and units scale
def parse_date_string(date_string):
    """
    parse a date string of the form time-units since yyyy-mm-dd hh:mm:ss

    Arguments
    ---------
    date_string: time-units since yyyy-mm-dd hh:mm:ss
    """
    units,epoch = split_date_string(date_string)
    conversion_factors = {'microseconds': 1e6,'microsecond': 1e6,
        'microsec': 1e6,'microsecs': 1e6,
        'milliseconds': 1e3,'millisecond': 1e3,'millisec': 1e3,
        'millisecs': 1e3,'msec': 1e3,'msecs': 1e3,'ms': 1e3,
        'seconds': 1.0,'second': 1.0,'sec': 1.0,'secs': 1.0,'s': 1.0,
        'minutes': 1.0/60.0,'minute': 1.0/60.0,'min': 1.0/60.0,'mins': 1.0/60.0,
        'hours': 1.0/3600.0,'hour': 1.0/3600.0,'hr': 1.0/3600.0,
        'hrs': 1.0/3600.0,'h': 1.0/3600.0,
        'day': 1.0/86400.0,'days': 1.0/86400.0,'d': 1.0/86400.0}
    if units not in conversion_factors.keys():
        raise ValueError('Invalid units: {0}'.format(units))
    #-- return the epoch (as list) and the time unit conversion factors
    return datetime_to_list(epoch),conversion_factors[units]

#-- PURPOSE: split a date string into units and epoch
def split_date_string(date_string):
    """
    split a date string into units and epoch

    Arguments
    ---------
    date_string: time-units since yyyy-mm-dd hh:mm:ss
    """
    try:
        units,since,epoch = date_string.split(None,2)
    except ValueError:
        raise ValueError('Invalid format: {0}'.format(date_string))
    else:
        return (units.lower(),dateutil.parser.parse(epoch))

#-- PURPOSE: convert a datetime object into a list
def datetime_to_list(date):
    """
    convert a datetime object into a list [year,month,day,hour,minute,second]

    Arguments
    ---------
    date: datetime object
    """
    return [date.year,date.month,date.day,date.hour,date.minute,date.second]

#-- PURPOSE: convert times from seconds since epoch1 to time since epoch2
def convert_delta_time(delta_time, epoch1=None, epoch2=None, scale=1.0):
    """
    Convert delta time from seconds since epoch1 to time since epoch2

    Arguments
    ---------
    delta_time: seconds since epoch1

    Keyword arguments
    -----------------
    epoch1: epoch for input delta_time
    epoch2: epoch for output delta_time
    scale: scaling factor for converting time to output units
    """
    epoch1 = datetime.datetime(*epoch1)
    epoch2 = datetime.datetime(*epoch2)
    delta_time_epochs = (epoch2 - epoch1).total_seconds()
    #-- subtract difference in time and rescale to output units
    return scale*(delta_time - delta_time_epochs)

#-- PURPOSE: calculate the delta time from calendar date
#-- http://scienceworld.wolfram.com/astronomy/JulianDate.html
def convert_calendar_dates(year, month, day, hour=0.0, minute=0.0, second=0.0,
    epoch=(1992,1,1,0,0,0), scale=1.0):
    """
    Calculate the time in time units since epoch from calendar dates

    Arguments
    ---------
    year: calendar month
    month: month of the year
    day: day of the month

    Keyword arguments
    -----------------
    hour: hour of the day
    minute: minute of the hour
    second: second of the minute
    epoch: epoch for output delta_time
    scale: scaling factor for converting time to output units

    Returns
    -------
    delta_time: days since epoch
    """
    #-- calculate date in Modified Julian Days (MJD) from calendar date
    #-- MJD: days since November 17, 1858 (1858-11-17T00:00:00)
    MJD = 367.0*year - np.floor(7.0*(year + np.floor((month+9.0)/12.0))/4.0) - \
        np.floor(3.0*(np.floor((year + (month - 9.0)/7.0)/100.0) + 1.0)/4.0) + \
        np.floor(275.0*month/9.0) + day + hour/24.0 + minute/1440.0 + \
        second/86400.0 + 1721028.5 - 2400000.5
    epoch1 = datetime.datetime(1858,11,17,0,0,0)
    epoch2 = datetime.datetime(*epoch)
    delta_time_epochs = (epoch2 - epoch1).total_seconds()
    #-- return the date in days since epoch
    return scale*np.array(MJD - delta_time_epochs/86400.0,dtype=np.float)

#-- PURPOSE: Count number of leap seconds that have passed for each GPS time
def count_leap_seconds(GPS_Time):
    """
    Counts the number of leap seconds between a given GPS time and UTC

    Arguments
    ---------
    GPS_Time: seconds since January 6, 1980 at 00:00:00

    Returns
    -------
    n_leaps: number of elapsed leap seconds
    """
    #-- get the valid leap seconds
    leaps = get_leap_seconds()
    #-- number of leap seconds prior to GPS_Time
    n_leaps = np.zeros_like(GPS_Time,dtype=np.float)
    for i,leap in enumerate(leaps):
        count = np.count_nonzero(GPS_Time >= leap)
        if (count > 0):
            indices = np.nonzero(GPS_Time >= leap)
            n_leaps[indices] += 1.0
    #-- return the number of leap seconds for converting to UTC
    return n_leaps

#-- PURPOSE: Define GPS leap seconds
def get_leap_seconds():
    """
    Gets a list of GPS times for when leap seconds occurred

    Returns
    -------
    GPS time (seconds since 1980-01-06T00:00:00) of leap seconds
    """
    leap_secs = pyTMD.utilities.get_data_path(['data','leap-seconds.list'])
    #-- find line with file expiration as delta time
    with open(leap_secs,'r') as fid:
        secs, = [re.findall(r'\d+',i).pop() for i in fid.read().splitlines()
            if re.match(r'^(?=#@)',i)]
    #-- check that leap seconds file is still valid
    expiry = datetime.datetime(1900,1,1) + datetime.timedelta(seconds=int(secs))
    today = datetime.datetime.now()
    update_leap_seconds() if (expiry < today) else None
    #-- get leap seconds
    leap_UTC,TAI_UTC = np.loadtxt(pyTMD.utilities.get_data_path(leap_secs)).T
    #-- TAI time is ahead of GPS by 19 seconds
    TAI_GPS = 19.0
    #-- convert leap second epochs from NTP to GPS
    #-- convert from time of 2nd leap second to time of 1st leap second
    leap_GPS = convert_delta_time(leap_UTC+TAI_UTC-TAI_GPS-1,
        epoch1=(1900,1,1,0,0,0), epoch2=(1980,1,6,0,0,0))
    #-- return the GPS times of leap second occurance
    return leap_GPS[leap_GPS >= 0].astype(np.float)

#-- PURPOSE: connects to servers and downloads leap second files
def update_leap_seconds(verbose=False, mode=0o775):
    """
    Connects to servers to download leap-seconds.list files from NIST servers
    https://www.nist.gov/pml/time-and-frequency-division/leap-seconds-faqs

    Servers and Mirrors
    ===================
    ftp://ftp.nist.gov/pub/time/leap-seconds.list
    https://www.ietf.org/timezones/data/leap-seconds.list

    Keyword arguments
    -----------------
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- local version of file
    FILE = 'leap-seconds.list'
    LOCAL = pyTMD.utilities.get_data_path(['data',FILE])
    HASH = pyTMD.utilities.get_hash(LOCAL)

    #-- try downloading from NIST ftp servers
    HOST = ['ftp.nist.gov','pub','time','iers',FILE]
    try:
        pyTMD.utilities.from_ftp(HOST, timeout=20, local=LOCAL,
            hash=HASH, verbose=verbose, mode=mode)
    except:
        pass
    else:
        return

    #-- try downloading from Internet Engineering Task Force (IETF) mirror
    REMOTE = ['https://www.ietf.org','timezones','data',FILE]
    try:
        pyTMD.utilities.from_http(REMOTE, timeout=5, local=LOCAL,
            hash=HASH, verbose=verbose, mode=mode)
    except:
        pass
    else:
        return

#-- PURPOSE: Download delta time files and merge into a single
def merge_delta_time(username=None, password=None, verbose=False, mode=0o775):
    """
    Connects to servers to download historic_deltat.data and deltat.data files
    Reads IERS Bulletin-A produced iers_deltat.data files
    Creates a merged file combining the historic, monthly and daily files

    Long-term Delta T:
    https://www.usno.navy.mil/USNO/earth-orientation/eo-products/long-term

    Keyword arguments
    -----------------
    username: NASA Earthdata username
    password: NASA Earthdata password
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- retrieve history delta time files
    pull_deltat_file('historic_deltat.data',username=username,password=password,
        verbose=verbose,mode=mode)
    #-- read historic delta time file
    historic_file=pyTMD.utilities.get_data_path(['data','historic_deltat.data'])
    historic = np.loadtxt(historic_file, skiprows=2)
    HY = np.floor(historic[:,0])
    HM = 12.0*np.mod(historic[:,0],1.0) + 1.0
    HD = np.ones_like(historic[:,0])
    #-- retrieve monthly delta time files
    pull_deltat_file('deltat.data',username=username,password=password,
        verbose=verbose,mode=mode)
    #-- read modern monthly delta time file
    monthly_file = pyTMD.utilities.get_data_path(['data','deltat.data'])
    monthly = np.loadtxt(monthly_file)
    monthly_time = pyTMD.convert_calendar_decimal(monthly[:,0],monthly[:,1],
        DAY=monthly[:,2])
    #-- retrieve daily delta time files
    merge_bulletin_a_files(username=username,password=password,
        verbose=verbose,mode=mode)
    #-- read modern daily delta time file from IERS Bulletin A files
    daily_file = pyTMD.utilities.get_data_path(['data','iers_deltat.data'])
    daily = np.loadtxt(daily_file)
    daily_time = pyTMD.convert_calendar_decimal(daily[:,0],daily[:,1],
        DAY=daily[:,2])
    #-- write to new merged file
    merged_file = pyTMD.utilities.get_data_path(['data','merged_deltat.data'])
    fid = open(merged_file,'w')
    print(merged_file) if verbose else None
    file_format = ' {0:4.0f} {1:2.0f} {2:2.0f} {3:7.4f}'
    #-- use historical values for times prior to monthly
    ind1, = np.nonzero(historic[:,0] < monthly_time[0])
    for i in ind1:
        args = (HY[i],HM[i],HD[i],historic[i,1])
        print(file_format.format(*args),file=fid)
    #-- use monthly values for times prior to daily
    ind2, = np.nonzero(monthly_time < daily_time[0])
    for i in ind2:
        args = (monthly[i,0],monthly[i,1],monthly[i,2],monthly[i,3])
        print(file_format.format(*args),file=fid)
    #-- use daily values for all times available
    for i,dt in enumerate(daily_time):
        args = (daily[i,0],daily[i,1],daily[i,2],daily[i,3])
        print(file_format.format(*args),file=fid)
    #-- close the merged file and change the permissions mode
    fid.close()
    os.chmod(merged_file,mode)

#-- PURPOSE: connect to IERS or CDDIS server and merge Bulletin-A files
def merge_bulletin_a_files(username=None,password=None,
    verbose=False,mode=0o775):
    """
    Attempt to connects to the IERS server and the CDDIS Earthdata server
        to download and merge Bulletin-A files
    Reads the IERS Bulletin-A files and calculates the daily delta times
    Delta times are the difference between universal time and dynamical time

    Servers and Mirrors
    -------------------
    ftp://ftp.iers.org/products/eop/rapid/bulletina/
    https://cddis.nasa.gov/archive/products/iers/iers_bulletins/bulletin_a/

    Keyword arguments
    -----------------
    username: NASA Earthdata username
    password: NASA Earthdata password
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- if complete: replace previous version of file
    LOCAL = pyTMD.utilities.get_data_path(['data','iers_deltat.data'])
    COPY = pyTMD.utilities.get_data_path(['data','iers_deltat.temp'])
    #-- try connecting to IERS ftp servers and merge Bulletin-A files
    try:
        iers_delta_time(COPY, verbose=verbose, mode=mode)
    except:
        os.remove(COPY) if os.access(COPY, os.F_OK) else None
        pass
    else:
        pyTMD.utilities.copy(COPY, LOCAL, move=True)
        return

    #-- try connecting to CDDIS https servers and merge Bulletin-A files
    try:
        cddis_delta_time(COPY, username=username, password=password,
            verbose=verbose, mode=mode)
    except:
        os.remove(COPY) if os.access(COPY, os.F_OK) else None
        pass
    else:
        pyTMD.utilities.copy(COPY, LOCAL, move=True)
        return

#-- PURPOSE: connects to IERS servers and finds Bulletin-A files
def iers_delta_time(daily_file, verbose=False, mode=0o775):
    """
    Connects to the IERS server to download Bulletin-A files
        https://datacenter.iers.org/productMetadata.php?id=6
    Reads the IERS Bulletin-A files and calculates the daily delta times
    Delta times are the difference between universal time and dynamical time

    Servers and Mirrors
    -------------------
    ftp://ftp.iers.org/products/eop/rapid/bulletina/

    Arguments
    ---------
    daily_file: output daily delta time file from merged Bulletin-A files

    Keyword arguments
    -----------------
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- connect to ftp host for IERS bulletins
    HOST = ['ftp.iers.org','products','eop','rapid','bulletina']
    #-- regular expression pattern for finding files
    rx = re.compile(r'bulletina-(.*?)-(\d+).txt$',re.VERBOSE)
    #-- open output daily delta time file
    fid = open(daily_file,'w')
    #-- output file format
    file_format = ' {0:4.0f} {1:2.0f} {2:2.0f} {3:7.4f}'
    #-- for each subdirectory
    subdirectory,mtimes = pyTMD.utilities.ftp_list(HOST,basename=True,sort=True)
    for SUB in subdirectory:
        #-- find Bulletin-A files in ftp subdirectory
        HOST.append(SUB)
        bulletin_files,mtimes = pyTMD.utilities.ftp_list(HOST,basename=True,
            sort=True,pattern=rx)
        #-- for each Bulletin-A file
        for f in sorted(bulletin_files):
            print(f) if verbose else None
            #-- copy remote file contents to BytesIO object
            HOST.append(f)
            remote_buffer = pyTMD.utilities.from_ftp(HOST,timeout=20)
            #-- read Bulletin-A file from BytesIO object
            YY,MM,DD,DELTAT = read_iers_bulletin_a(remote_buffer)
            #-- print delta time for week to output file
            for Y,M,D,T in zip(YY,MM,DD,DELTAT):
                print(file_format.format(Y,M,D,T),file=fid)
            #-- close the bytesIO object
            remote_buffer.close()
            #-- remove the file from the list
            HOST.remove(f)
        #-- remove the subdirectory from the list
        HOST.remove(SUB)
    #-- close the output file
    fid.close()
    #-- change the permissions mode
    os.chmod(daily_file,mode)

#-- PURPOSE: connects to CDDIS Earthdata https server and finds Bulletin-A files
def cddis_delta_time(daily_file, username=None, password=None,
    verbose=False, mode=0o775):
    """
    Connects to the CDDIS Earthdata server to download Bulletin-A files
    Reads the IERS Bulletin-A files and calculates the daily delta times
    Delta times are the difference between universal time and dynamical time

    Servers and Mirrors
    -------------------
    https://cddis.nasa.gov/archive/products/iers/iers_bulletins/bulletin_a/

    Arguments
    ---------
    daily_file: output daily delta time file from merged Bulletin-A files

    Keyword arguments
    -----------------
    username: NASA Earthdata username
    password: NASA Earthdata password
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- connect to CDDIS Earthdata host for IERS bulletins
    HOST = ['https://cddis.nasa.gov','archive','products','iers',
        'iers_bulletins','bulletin_a']
    #-- build NASA Earthdata opener for CDDIS and check credentials
    pyTMD.utilities.build_opener(username, password)
    pyTMD.utilities.check_credentials()
    #-- regular expression pattern for finding directories
    R1 = re.compile(r'volume_(.*?)$',re.VERBOSE)
    #-- regular expression pattern for finding files
    R2 = re.compile(r'iers_bulletina\.(.*?)_(\d+)$',re.VERBOSE)
    #-- open output daily delta time file
    fid = open(daily_file,'w')
    file_format = ' {0:4.0f} {1:2.0f} {2:2.0f} {3:7.4f}'
    #-- for each subdirectory
    subdirectory,mtimes=pyTMD.utilities.cddis_list(HOST,build=False,pattern=R1)
    #-- extract roman numerals from subdirectories
    roman = [R1.findall(s).pop() for s in subdirectory]
    #-- sort the list of Roman numerals
    subdirectory = [subdirectory[i] for i,j in sorted(enumerate(roman),
        key=lambda i: pyTMD.utilities.roman_to_int(i[1]))]
    #-- output file format
    for SUB in subdirectory:
        #-- find Bulletin-A files in https subdirectory
        HOST.append(SUB)
        bulletin_files,mtimes = pyTMD.utilities.cddis_list(HOST,build=False,
            sort=True,pattern=R2)
        #-- for each Bulletin-A file
        for f in sorted(bulletin_files):
            print(f) if verbose else None
            #-- copy remote file contents to BytesIO object
            HOST.append(f)
            remote_buffer = pyTMD.utilities.from_cddis(HOST,
                build=False,timeout=20)
            #-- read Bulletin-A file from BytesIO object
            YY,MM,DD,DELTAT = read_iers_bulletin_a(remote_buffer)
            #-- print delta time for week to output file
            for Y,M,D,T in zip(YY,MM,DD,DELTAT):
                print(file_format.format(Y,M,D,T),file=fid)
            #-- close the bytesIO object
            remote_buffer.close()
            #-- remove the file from the list
            HOST.remove(f)
        #-- remove the subdirectory from the list
        HOST.remove(SUB)
    #-- close the output file
    fid.close()
    #-- change the permissions mode
    os.chmod(daily_file,mode)

#-- PURPOSE: reads IERS Bulletin-A and calculates the delta times
def read_iers_bulletin_a(fileID):
    """
    Read a weekly IERS Bulletin-A file and calculate the delta times (TT - UT1)

    Arguments
    ---------
    fileID: open file object for Bulletin-A file

    Returns
    -------
    Y: calendar year
    M: calendar month
    D: day of the month
    DELTAT: difference between universal time and dynamical time
    """
    #-- read contents from input file object
    file_contents = fileID.read().decode('utf-8').splitlines()

    #-- parse header text to find time offsets
    #-- TT-TAI
    TT_TAI = 0
    #-- TAI-UTC
    TAI_UTC = 0
    #-- counts the number of lines in the header
    count = 0
    HEADER = False
    #-- Reading over header text
    while not HEADER:
        #-- file line at count
        l = file_contents[count]
        #-- check if line contains time offsets
        if re.search(r'TT\s\=\sTAI',l):
            TT_TAI = np.float(re.findall(r'(\d+\.\d+)',l).pop())
        if re.search(r'TAI-UTC',l):
            TAI_UTC = np.float(re.findall(r'=\s(\d+\.\d+)',l).pop())
        #-- find line to set HEADER flag to True
        HEADER = bool(re.search(r'COMBINED\sEARTH\sORIENTATION\sPARAMETERS:',l))
        #-- add 1 to counter
        count += 1

    #-- convert variables to numpy arrays
    MJD = np.zeros((7))
    UT1_UTC = np.zeros((7))
    valid = 0
    #-- for each day in the week
    for i in range(7):
        try:
            #-- split numerical instances from data line
            line_contents = file_contents[count+i+4].split()
            #-- years are not always complete in the bulletin file
            #-- Modified Julian Day (days since 1858-11-17T00:00:00)
            MJD[i] = np.float(line_contents[3])
            #-- difference between UT1 and UTC times
            UT1_UTC[i] = np.float(line_contents[8])
        except (IndexError,ValueError):
            pass
        else:
            valid += 1

    #-- calculate components for delta time
    #-- TAI time is ahead of GPS by 19 seconds
    TAI_GPS = 19.0
    #-- calculate calendar dates from Modified Julian days
    Y,M,D,h,m,s = pyTMD.convert_julian(MJD[:valid]+2400000.5,FORMAT='tuple')
    #-- calculate GPS Time (seconds since 1980-01-06T00:00:00)
    #-- by converting the Modified Julian days (days since 1858-11-17T00:00:00)
    GPS_Time = convert_delta_time(MJD[:valid]*8.64e4, epoch1=(1858,11,17,0,0,0),
        epoch2=(1980,1,6,0,0,0), scale=1.0) + TAI_UTC - TAI_GPS
    #-- number of leap seconds between GPS and UTC
    #-- this finds the daily correction for weeks with leap seconds
    GPS_UTC = count_leap_seconds(GPS_Time)
    #-- calculate delta time (TT - UT1) -->
    #-- (TT-TAI) + (TAI-GPS) + (GPS-UTC) - (UT1-UTC)
    DELTAT = TT_TAI + TAI_GPS + GPS_UTC - UT1_UTC[:valid]

    #-- return dates and delta times
    return (Y,M,D,DELTAT)

#-- PURPOSE: connects to servers and downloads delta time files
def pull_deltat_file(FILE,username=None,password=None,verbose=False,mode=0o775):
    """
    Connects to servers and downloads delta time files

    Servers and Mirrors
    ===================
    http://maia.usno.navy.mil/ser7/
    https://cddis.nasa.gov/archive/products/iers/
    ftp://cddis.nasa.gov/products/iers/
    ftp://cddis.gsfc.nasa.gov/pub/products/iers/

    Arguments
    ---------
    FILE: delta time file to download from remote servers
        deltat.data: monthly deltat file
        historic_deltat.data: historic deltat file

    Keyword arguments
    -----------------
    username: NASA Earthdata username
    password: NASA Earthdata password
    verbose: print file information about output file
    mode: permissions mode of output file
    """
    #-- local version of file
    LOCAL = pyTMD.utilities.get_data_path(['data',FILE])
    HASH = pyTMD.utilities.get_hash(LOCAL)

    #-- try downloading from US Naval Oceanography Portal
    HOST = ['http://maia.usno.navy.mil','ser7',FILE]
    try:
        pyTMD.utilities.from_http(HOST,timeout=5,local=LOCAL,hash=HASH,
            verbose=verbose,mode=mode)
    except:
        pass
    else:
        return

    #-- try downloading from NASA Crustal Dynamics Data Information System
    #-- note: anonymous ftp access will be discontinued on 2020-10-31
    #-- will require using the following https Earthdata server after that date
    server = []
    server.append(['cddis.nasa.gov','pub','products','iers',FILE])
    server.append(['cddis.gsfc.nasa.gov','products','iers',FILE])
    for HOST in server:
        try:
            pyTMD.utilities.from_ftp(HOST,timeout=20,local=LOCAL,hash=HASH,
                verbose=verbose,mode=mode)
        except:
            pass
        else:
            return

    #-- try downloading from NASA Crustal Dynamics Data Information System
    #-- using NASA Earthdata credentials stored in netrc file
    HOST = ['https://cddis.nasa.gov','archive','products','iers',FILE]
    try:
        pyTMD.utilities.from_cddis(HOST,username=username,password=password,
            timeout=20,local=LOCAL,hash=HASH,verbose=verbose,mode=mode)
    except:
        pass
    else:
        return
