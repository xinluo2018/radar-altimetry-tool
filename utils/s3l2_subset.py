import xarray as xr
import numpy as np

def s3l2_subset(s3_l2, region):
    '''
    input:
        s3_l2: xarray.Dataset, one pass SRAL L2 data
        region: list, [lon_min, lon_max, lat_min, lat_max]
    output:
        s3_l2_subs: xarray.Dataset, SARL L2 data corresponding to the give region.
    '''
    # initialize a xarray.Dataset.
    s3_l2_subs = xr.Dataset(attrs=s3_l2.attrs)
    # read the footprints location
    lat_20_ku,lon_20_ku = s3_l2.variables["lat_20_ku"], s3_l2.variables["lon_20_ku"]
    lat_20_c, lon_20_c = s3_l2.variables["lat_20_c"], s3_l2.variables["lon_20_c"]
    lat_01, lon_01 = s3_l2.variables["lat_01"], s3_l2.variables["lon_01"]
    # select the footprints location corresponding to the given region
    ind_20_ku = np.where((lat_20_ku>region[2]) & (lat_20_ku<region[3]) & \
        (lon_20_ku>region[0]) & (lon_20_ku<region[1]))
    ind_20_c = np.where((lat_20_c>region[2]) & (lat_20_c<region[3]) & \
        (lon_20_c>region[0]) & (lon_20_c<region[1]))
    ind_01 = np.where((lat_01>region[2]) & (lat_01<region[3]) & \
        (lon_01>region[0]) & (lon_01<region[1]))
    # select the data corresponding to the given region
    ## variables
    for var_name in s3_l2.variables:
        var_value = s3_l2.variables[var_name]
        if var_value.shape[0]==s3_l2.dims['time_01']: 
            s3_l2_subs[var_name] = var_value[ind_01]
        if var_value.shape[0]==s3_l2.dims['time_20_ku']: 
            s3_l2_subs[var_name] = var_value[ind_20_ku]
        if var_value.shape[0]==s3_l2.dims['time_20_c']: 
            s3_l2_subs[var_name] = var_value[ind_20_c]

    ## coordinates 
    for coord_name in s3_l2.coords:
        coord_value = s3_l2.coords[coord_name]
        if coord_value.shape[0]==s3_l2.dims['time_01']: 
            s3_l2_subs.coords[coord_name] = s3_l2.coords[coord_name].\
                variable[ind_01]
        if coord_value.shape[0]==s3_l2.dims['time_20_ku']: 
            s3_l2_subs.coords[coord_name] = s3_l2.coords[coord_name].\
                variable[ind_20_ku]
        if coord_value.shape[0]==s3_l2.dims['time_20_c']: 
            s3_l2_subs.coords[coord_name] = s3_l2.coords[coord_name].\
                variable[ind_20_c]

    return s3_l2_subs
