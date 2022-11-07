import numpy as np
from sklearn import linear_model

def ransac_filter(x, y, thre):
    '''
    input:
        x,y: xarray.Variable, longitude and altimetry varibale (e.g.,ssha)
        thre: float, filter threshold corresponding to the difference between y            and y_ransac 
    ouput: 
        the filtered y, and ransac fitting y
    '''
    x_new = x[~np.isnan(y)]
    y_new = y[~np.isnan(y)]
    ransac = linear_model.RANSACRegressor(random_state=42)
    x = np.array(x)[:, np.newaxis]
    x_new = np.array(x_new)[:, np.newaxis]
    # y = np.nan_to_num(ssha_sol2_ku_20)
    ransac.fit(x_new, y_new)
    y_ransac_fit = ransac.predict(x)
    dif_y = np.array(abs(np.nan_to_num(y) - y_ransac_fit))
    y_filter = np.where(dif_y>thre, np.nan, y)
    return y_filter, y_ransac_fit