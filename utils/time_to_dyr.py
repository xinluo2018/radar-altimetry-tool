from astropy.time import Time

### convert time to decimal year
def time_to_dyr(time_jason):
    ''' this function suitable for the jason data, sentinel-3 data,
        and the cryosat2 data for time conversion
    '''
    start_jason = Time('2000-01-01 00:00:00.0')
    time_start_jason = Time(start_jason, format="gps").value  ## Difference between gps time and cryo2 time
    time_jason = time_jason + time_start_jason   ## Convert cryo2 time to gps time
    time_jason_gps = Time(time_jason, format="gps")
    jason_time_dyr = Time(time_jason_gps, format="decimalyear").value
    return jason_time_dyr
