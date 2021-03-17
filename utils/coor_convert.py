## ref: https://blog.csdn.net/Prince999999/article/details/105843511

import numpy as np

def geo2imagexy(lon,lat,img_gdal):
    '''
    author: xin luo, date: 2021.3.16
    description: from georeferenced location (i.e., lon, lat) to image location(col,row).
    :param img_gdal: GDAL data
    :param lon: project or georeferenced x, i.e.,lon
    :param lat: project or georeferenced y, i.e., lat
    :return: image col and row corresponding to the georeferenced location.
    '''
    trans = img_gdal.GetGeoTransform()
    a = np.array([[trans[1], trans[2]], [trans[4], trans[5]]])
    b = np.array([lon - trans[0], lat - trans[3]])
    col_fps, row_fps = np.linalg.solve(a, b)
    col_fps, row_fps = np.floor(col_fps).astype('int'), np.floor(row_fps).astype('int')
    return col_fps, row_fps