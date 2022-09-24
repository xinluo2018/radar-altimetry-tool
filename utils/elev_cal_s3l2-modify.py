
import numpy as np

def ssha_cal_s3l2(s3l2, retracker='ocean', tide_cor = False):
    '''
    calculate the ssha variable (ku_20) from sentinel-3 SRAR l2 product.
    ref: https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-3-altimetry/level-2/ssh-anomaly-equation
    ssha = ssh - mean sea surface
    input:
        s3l2: xarray.Dataset sentinel3 SRAR l2 data
        retracker: str, 'ocean', 'ocog', 'sea_ice', or 'ice_sheet'
    output:
        ssha values, and ssh values
    '''
    retracker = 'range_'+retracker+'_20_ku'
    alt = s3l2['alt_20_ku']
    range_retraker = s3l2[retracker]
    ## correction variables
    iono_corr_alt_ku_20 = s3l2['iono_cor_alt_20_ku']
    dry_tropo_corr_01 = s3l2['mod_dry_tropo_cor_zero_altitude_01']
    wet_tropo_corr_01 = s3l2['rad_wet_tropo_cor_01_ku']
    sea_state_bias_ku_01 = s3l2['sea_state_bias_01_ku']  #
    solid_earth_tide_01 = s3l2['solid_earth_tide_01']
    ocean_tide_sol1_01 = s3l2['ocean_tide_sol1_01']
    pole_tide_01 = s3l2['pole_tide_01']
    inv_bar_corr_01 = s3l2['inv_bar_cor_01']    #
    hf_fluct_corr_01 = s3l2['hf_fluct_cor_01']  #
    mss_sol1_ku_20 = s3l2['mean_sea_surf_sol1_20_ku']  #for ssha calculation
    ## upsample the 01 variables to ku_20 variables
    times_20 = s3l2.variables['UTC_sec_20_ku']
    times_01 = s3l2.variables['UTC_sec_01']
    dif_time = abs(times_20 - times_01)
    ind_min = dif_time.argmin(dim='time_01')
    ### upsampling for the correction parameter
    dry_tropo_corr_01to20 = dry_tropo_corr_01[ind_min]
    wet_tropo_corr_01to20 = wet_tropo_corr_01[ind_min]
    ocean_tide_sol1_01to20 = ocean_tide_sol1_01[ind_min]
    solid_earth_tide_01to20 = solid_earth_tide_01[ind_min]
    pole_tide_01to20 = pole_tide_01[ind_min]
    sea_state_bias_ku_01to20 = sea_state_bias_ku_01[ind_min]
    hf_fluct_corr_01to20 = hf_fluct_corr_01[ind_min]
    inv_bar_corr_01to20 = inv_bar_corr_01[ind_min]
    # ## with ocean tide correction
    if tide_cor:
        corrections = dry_tropo_corr_01to20 + wet_tropo_corr_01to20 + \
        iono_corr_alt_ku_20 + ocean_tide_sol1_01to20 + solid_earth_tide_01to20 + \
        pole_tide_01to20 + sea_state_bias_ku_01to20 + hf_fluct_corr_01to20 + \
        inv_bar_corr_01to20
    ## without ocean tide correction
    else:
        corrections = dry_tropo_corr_01to20 + wet_tropo_corr_01to20 + \
        iono_corr_alt_ku_20 + solid_earth_tide_01to20 + \
        pole_tide_01to20 + sea_state_bias_ku_01to20 + hf_fluct_corr_01to20 + \
        inv_bar_corr_01to20
    # calculation
    ssh_sol1_ku_20 = alt - range_retraker  - corrections
    ssha_sol1_ku_20 = ssh_sol1_ku_20 - mss_sol1_ku_20
    return ssha_sol1_ku_20,  ssh_sol1_ku_20
