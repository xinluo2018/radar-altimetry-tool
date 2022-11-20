
## workplace
cd /Users/luo/OneDrive/GitHub/radar-altimetry-tool

# ## 1) wgs84 to utm projection
# path_in=data/rs_img/dianchi_s2_20200511_wat.tif
# path_out=data/rs_img/dianchi_s2_20200511_wat_wgs84.tif
# gdalwarp -overwrite -s_srs EPSG:32648 -t_srs EPSG:4326 -r cubic -co COMPRESS=LZW -co TILED=YES $path_in $path_out 

## 2) utm to wgs84
path_in=data/rs-img/yangzonghai_s2_20200511.tif
path_out=data/rs-img/yangzonghai_s2_20200511_wgs84.tif 
gdalwarp -overwrite -s_srs EPSG:32648 -t_srs EPSG:4326 -r cubic -co COMPRESS=LZW -co TILED=YES $path_in $path_out

