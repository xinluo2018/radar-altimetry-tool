import numpy as np


def tgauge_data_interp(tgauge_values, tgauge_times, target_time):
    '''
    obtain the interpolation value of the tgauge values
    input: 
        tgauge_values, tgauge_times: 1D np.array
        target_time: np.datetime64
    ouput:
        interpolation value of the tgauge values
    '''
    delta_times = np.array(target_time - tgauge_times, dtype=float)
    ind_start = np.where(delta_times>=0)[0][-1]
    delta_time =  target_time - tgauge_times[ind_start]
    delta_time = float(delta_time)/(1e9*3600)
    sealevel_interp = tgauge_values[ind_start] + (tgauge_values[ind_start+1]-tgauge_values[ind_start])*delta_time
    return sealevel_interp, ind_start