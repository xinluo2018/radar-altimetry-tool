#! /bin/bash
## author: xin luo; xxxx
## create: 2022.09.25;
## des: preprocessing for the sentinel-3 l2 data. 
## include 1) read out; 2) subset; 3) merge.


## workplace
cd /Users/luo/OneDrive/GitHub/sentinel3-altimetry-l2
dir_s3l2=data/s3-altimetry/s3a-orbit-289

# ## -- 1.readout
# path_in=$dir_s3l2/*/enhanced_measurement.nc
# python utils/read_s3l2.py $path_in

# ## -- 2.subset
# path_mask=data/water_mask/dianchi_s2_20200511_wat_wgs84.tif
# path_in=$dir_s3l2/*/enhanced_measurement_readout.h5
# python utils/subset_h5dict.py $path_in -m $path_mask -t 2020 2021 -c lon_20_ku lat_20_ku -tn time_20_ku

# # ## -- 3.merge
# path_in=$dir_s3l2/*/enhanced_measurement_readout_subs.h5
# path_out=$dir_s3l2/enhanced_measurement_readout_subs_merge.h5
# python utils/merge_files.py $path_in -o $path_out
