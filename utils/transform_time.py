### ----- 
# author: luo xin, 
# creat: 2022.9.25
# des: Time formats conversions. year-month-day-hour, day-of-year, decimal year.
# -----

'''ref: https://www.cnblogs.com/maoerbao/p/11518831.html
'''

import numpy as np
from astropy.time import Time

def date2doy(year, month, day, hour=0, minute=0):
    '''
    convert year-month-day-hour-minute to doy (day-of-year)
    month:0~12
    day:0~31
    hour: 0~24
    minute:0~60
    '''
    month_leapyear=[31,29,31,30,31,30,31,31,30,31,30,31]
    month_notleap= [31,28,31,30,31,30,31,31,30,31,30,31]
    doy=0
    if month==1:
            pass
    elif year%4==0 and (year%100!=0 or year%400==0):
            for i in range(month-1):
                    doy+=month_leapyear[i]
    else:
            for i in range(month-1):
                    doy+=month_notleap[i]
    doy+=day
    doy+=(hour+minute/60)/24
    return doy

def doy2date(year, doy):
    '''
    convert doy(day-of-year) to year-month-day-hour-minute formate 
    the function returns the month and the day of the month. 
    '''
    month_leapyear=[31,29,31,30,31,30,31,31,30,31,30,31]
    month_notleap= [31,28,31,30,31,30,31,31,30,31,30,31]

    if year%4==0 and (year%100!=0 or year%400==0):
        for i in range(0,12):
            if doy>month_leapyear[i]:
                doy-=month_leapyear[i]
                continue
            if doy<=month_leapyear[i]:
                month=i+1
                day=doy
                break
    else:
        for i in range(0,12):
            if doy>month_notleap[i]:
                doy-=month_notleap[i]
                continue
            if doy<=month_notleap[i]:
                month=i+1
                day=doy
                break

    return month, day

def dt64_to_dyr(dt64):
    """
    des: convert datetime64 to decimal year format.    
    e.g., '2020-05-23T03:25:22.959373696' -> 2020.3907103825136.
    args:
        dt64: np.datetime64 format time
    """
    year = dt64.astype('M8[Y]')
    days = (dt64 - year).astype('timedelta64[D]')
    year_next = year + np.timedelta64(1, 'Y')
    days_of_year = (year_next.astype('M8[D]') - year.astype('M8[D]')).astype('timedelta64[D]')
    dt_float = 1970 + year.astype(float) + days / (days_of_year)
    return dt_float

def gps2dyr(time):
    """ Converte from GPS time to decimal years. """
    time_gps = Time(time, format="gps")
    time_dyr = Time(time_gps, format="decimalyear").value
    return time_dyr

