import xarray as xr

def s3l2_extract(s3_l2, ind):
    '''
    extract variables with a given index.
    input:
        s3_l2: xarrayDataset, s3_l2 product
        ind: index, corresponding to the required data values
    output:
        s3l2_extract: xarrayDataset, the xarrayDataset contains the required data value
    '''
    s3l2_extract = xr.Dataset(attrs=s3_l2.attrs)
    for var_name in s3_l2.variables:
        var_value = s3_l2.variables[var_name]
        if var_value.shape[0]==s3_l2.dims['time_20_ku']: 
            s3l2_extract[var_name] = var_value[ind]
    ## coordinates
    for coord_name in s3_l2.coords:
        coord_value = s3_l2.coords[coord_name]
        if coord_value.shape[0]==s3_l2.dims['time_20_ku']:
            s3l2_extract.coords[coord_name] = s3_l2.coords[coord_name].\
                variable[ind]
        
    return s3l2_extract

