import sys
sys.path.append("/Users/luo/OneDrive/SAR-Altimetry/sentinel3-altimetry-l2/utils")

import numpy as np
from astropy.modeling.models import Ellipse2D
from astropy.coordinates import Angle
from regions import PixCoord, EllipsePixelRegion
import matplotlib.pyplot as plt
from rsimage.imgShow import imgShow
from coor_convert import geo2imagexy

def fp_mask(img, a, b, center_row, center_col, angle):
    '''
    obtain the ellipse mask of the image
    img: 2-d numpy.array;
    a,b: the length corresponding to the semimajor axis and semiminor axis respectively.
    center_row,center_col: the center location
    '''
    if len(img.shape) == 3:
        img_row, img_col, _ = img.shape
    else: 
        img_row, img_col = img.shape
    theta = Angle(angle, 'deg')
    y, x = np.mgrid[0:img_row, 0:img_col]
    e = Ellipse2D(amplitude=1., x_0=center_col, y_0=center_row, a=a, b=b, theta=theta.radian)
    mask = e(x, y)
    ## from botton-letf coordinate to up-left(image col-row) coordinate
    mask = np.flip(mask, axis=0) 
    return mask


def fp_wat_cal(wat_map, angle, fp_row, fp_col, a=27.3, b=5, window_row=101, window_col=101):
    '''
    obtain the statistic corresponding to the footprint region of the image
    wat_map: 2-d numpy.array, water map
    angle: degree(unit), direction of the ellipse
    fp_row, fp_col: location of the footprint.
    a,b: the length corresponding to the semimajor axis and semiminor axis respectively.
    window_row,window_col: the sub-region size of water map with the centered footprint.
    '''
    row_map,col_map = wat_map.shape
    center_row = round((window_row-1)/2)
    center_col = round((window_col-1)/2)
    if col_map - fp_col < center_col+1:
        wat_map= np.pad(wat_map, ((0, 0), (0, center_col+1)), constant_values=0)
    if row_map - fp_row < center_row+1:
        wat_map= np.pad(wat_map, ((0, center_row+1), (0, 0)), constant_values=0)
    wat_map_window = wat_map[fp_row-center_row:fp_row+center_row+1, fp_col-center_col:fp_col+center_col+1]
    theta = Angle(angle, 'deg')
    y, x = np.mgrid[0:window_row, 0:window_col]
    e = Ellipse2D(amplitude=1., x_0=center_col, y_0=center_row, a=a, b=b, theta=theta.radian)
    mask = e(x, y)
    ## from botton-letf coordinate to up-left(image col-row) coordinate
    mask = np.flip(mask, axis=0)
    values = wat_map_window[mask==1]
    wat_percent = np.sum(values)/values.shape
    return wat_percent


def fp_show(img, a, b, center_row, center_col, angle):
    '''
    show the ellipse scope in the image
    img: 2-d numpy.array;
    a,b: the length corresponding to the semimajor axis and semiminor axis respectively.
    center_row, center_col: the center location of the image
    '''
    if len(img.shape) == 3:
        img_row, img_col, _ = img.shape
    else: 
        img_row, img_col = img.shape
    angle = 180-angle  # from botton-left (origin) coordinate to up-left(image col-row) coordinate
    theta = Angle(angle, 'deg')
    imgShow(img)
    center = PixCoord(x=center_col, y=center_row)
    reg = EllipsePixelRegion(center=center, width=2*a, height=2*b, angle=theta)
    patch = reg.as_artist(facecolor='none', edgecolor='red', lw=2)
    ax = plt.gca()
    ax.add_patch(patch)
    plt.plot(center_col, center_row,'ro')

def get_fp_angle(row_fps,col_fps):
    '''footprint angle (degree)'''
    dy = -(row_fps[0]-row_fps[-1])
    dx = col_fps[0]-col_fps[-1]
    angle_fp = np.degrees(np.arctan(dy/dx))
    angle_e = 90+angle_fp
    return angle_e

def get_fps_wat(wat_map,angle_e,row_fps,col_fps):
    '''get the water percentage in footprints'''
    fps_wat_per = []
    for ind in range(0,row_fps.shape[0]):
        wat_per = fp_wat_cal(wat_map=wat_map, angle=angle_e, fp_row=row_fps[ind], fp_col=col_fps[ind], a=27.3, b=5, window_row=101, window_col=101)
        fps_wat_per.append(float(wat_per))
    return fps_wat_per