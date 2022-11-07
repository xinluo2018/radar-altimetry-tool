### ----- 
# author: luo xin 
# creat: 2022.10.12
# des: read the sentinel-3 altimetry l2 data, and write out the selected variables to h5 file.
# usage: python read_s3l2.py data/s3-altimetry/s3a-orbit-289/*/enhanced_measurement.nc
# -----

import os
import xarray as xr
import numpy as np
import h5py
import argparse
from joblib import Parallel, delayed

def dt64_to_dyr(dt64):
    year = dt64.astype('M8[Y]')
    days = (dt64 - year).astype('timedelta64[s]')
    year_next = year + np.timedelta64(1, 'Y')
    days_of_year = (year_next.astype('M8[D]') - year.astype('M8[D]')).astype('timedelta64[D]')
    dt_float = 1970 + year.astype(float) + days / (days_of_year)
    return dt_float

def get_args():
    description = "read Sentinel-3 Level-2 data and write out the selected variables."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(         
            "ifiles", metavar="files_in", type=str, nargs="+",
            help="input files to read (.nc).")
    parser.add_argument(
            "-n", metavar=("njobs"), dest="njobs", type=int, nargs=1,
            help="number of cores to use for parallel processing", 
            default=[1])
    return parser.parse_args()


def read_s3l2(file_in, file_out=None):
    '''
    des:
        read in and write out sentinel-3 altimetry data.
        users can add or select the interested variables by themself.
    arg:
        file_in: sentinel-3 level-2 altimetry file, .nc format
        dir_out: directory to save the write out sentinel-2 level-2 data
    return:
        selected variables of the sentinel-2 level-2 data
    '''
    # Create dictionary for saving output variables
    out_keys = ['lat_20_ku', 'lon_20_ku', 'time_20_ku', 'elevation_ocog_20_ku', \
                                        'waveform_20_ku', 'cycle', 'pass']   ## output variables
    d = {}      
    for key in out_keys: 
        d[key]=np.array([]); 

    print(('input -> ', file_in))
    s3_l2 = xr.open_dataset(file_in)  ## read the data

    #-----------------------------------#
    # 1) Read variables from .nc data   #
    #-----------------------------------#
    ## group varibales:
    d['lat_20_ku'] = s3_l2.coords["lat_20_ku"].values
    d['lon_20_ku'] = s3_l2.coords["lon_20_ku"].values
    d['time_20_ku'] = dt64_to_dyr(s3_l2.coords['time_20_ku'].values)
    d['elevation_ocog_20_ku'] = s3_l2.variables["elevation_ocog_20_ku"].values
    d['waveform_20_ku'] = s3_l2.variables["waveform_20_ku"].values.astype("float32")
    d['cycle'] = s3_l2.attrs['cycle_number']*np.ones(d['lat_20_ku'].shape)
    d['pass'] = s3_l2.attrs['pass_number']*np.ones(d['lat_20_ku'].shape)

    #------------------------------------------#
    # 2) Writting out the selected data        #
    #------------------------------------------#
    if file_out is None:
        path, ext = os.path.splitext(file_in)
        file_out = path+'_readout'+ '.h5'
    if os.path.exists(file_out): os.remove(file_out)
    if d['lat_20_ku'].size != 0:

        with h5py.File(file_out, "w") as f_out:
            [f_out.create_dataset(key, data=d[key]) for key in out_keys]
        print('Written file ->', file_out)
    else:
        print('Written file ->', 'Null')


if __name__ == '__main__':

    ### ---- read input from command line
    args = get_args()
    files_in = args.ifiles
    njobs = args.njobs[0]

    if njobs == 1:
        print("running in serial ...")
        [read_s3l2(f) for f in files_in]
    else:
        print(("running in parallel (%d jobs) ..." % njobs))
        Parallel(n_jobs=njobs, verbose=5)(
                delayed(read_s3l2)(f) for f in files_in)

