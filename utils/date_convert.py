'''ref: https://www.cnblogs.com/maoerbao/p/11518831.html
'''

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