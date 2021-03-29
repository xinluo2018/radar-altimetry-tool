import numpy as np

def tgauge_time_search(tgauge_data, s3_l2):
    '''
    get the tgauge times which match to time of s3_l2 data
    input: .nc file
    return: start index and end index of the tgauge_data, and the times of the tgauge_data
    '''
    dif_time_start = s3_l2['time_20_ku'][0] - tgauge_data['time']
    dif_time_end = tgauge_data['time'] - s3_l2['time_20_ku'][-1]
    dif_time_start = np.array(dif_time_start, dtype=float)
    ind_start  = np.where(dif_time_start>=0)[0][-1]
    dif_time_end = np.array(dif_time_end, dtype=float)
    ind_end  = np.where(dif_time_end>=0)[0][0]
    tgauge_time = tgauge_data['time'][ind_start:ind_end+1]
    return ind_start, ind_end, tgauge_time
