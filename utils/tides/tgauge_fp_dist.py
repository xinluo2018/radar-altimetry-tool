from geopy.distance import geodesic

def tgauge_fp_dist(s3_l2, tgauge_data, record_id=0):
    '''
    Calculate the distance between footprint and tide gauge station
     '''
    dis_fp_tgauge = []
    for i in range(s3_l2.dims['time_20_ku']):
        dis = geodesic((s3_l2['lat_20_ku'][i], s3_l2['lon_20_ku'][i]), \
                (tgauge_data['lat'][record_id], tgauge_data['lon'][record_id])).km
        dis_fp_tgauge.append(round(dis,3))
    return dis_fp_tgauge
