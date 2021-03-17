import matplotlib.pyplot as plt
import numpy as np

def imgShow(img, col_bands=(2,1,0), clip_percent=2, per_band_clip='False'):
    '''
    Arguments:
        img: (row, col, band) or (row, col)
        num_bands: a list/tuple, [red_band,green_band,blue_band]
        clip_percent: for linear strech, value within the range of 0-100. 
        per_band: if 'True', the band values will be clipped by each band respectively. 
    '''
    img = img/(np.amax(img)+0.00001)
    img = np.squeeze(img)
    if np.isnan(np.sum(img)) == True:
        where_are_NaNs = np.isnan(img)
        img[where_are_NaNs] = 0
    elif np.min(img) == np.max(img):
        if len(img.shape) == 2:
            plt.imshow(np.clip(img, 0, 1),vmin=0,vmax=1) 
        else:
            plt.imshow(np.clip(img[:,:,0], 0, 1),vmin=0,vmax=1)
    else:
        if len(img.shape) == 2:
            img_color = img
        else:
            img_color = img[:,:,[col_bands[0], col_bands[1], col_bands[2]]]    
        img_color_clip = np.zeros_like(img_color)
        if per_band_clip == 'True':
            for i in range(3):
                img_color_hist = np.percentile(img_color[:,:,i], [clip_percent, 100-clip_percent])
                img_color_clip[:,:,i] = (img_color[:,:,i]-img_color_hist[0])\
                                    /(img_color_hist[1]-img_color_hist[0])
        else:
            img_color_hist = np.percentile(img_color, [clip_percent, 100-clip_percent])
            img_color_clip = (img_color-img_color_hist[0])\
                                    /(img_color_hist[1]-img_color_hist[0])
        plt.imshow(np.clip(img_color_clip, 0, 1),vmin=0,vmax=1)