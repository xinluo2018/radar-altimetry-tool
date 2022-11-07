# author: xin luo
# create: 2022.10.19
# des: subset file with given extent, or mask image, or time range.

'''
example:
    python subset_s3l2.py ./input/path/*.h5 -r 90 91 30 31 -t 2008.1 2008.4
    python subset_s3l2.py ./input/path/*.h5 -m ./data/mask.tif -t 2008.1 2008.4
'''

import os
import h5py 
import argparse
import numpy as np
from osgeo import gdal
from osgeo import osr
from glob import glob

def get_args():

    """ Get command-line arguments. """
    parser = argparse.ArgumentParser(
            description='subset sentinle-3 l2 data by extent or time')
    parser.add_argument(
            'ifile', metavar='ifile', type=str, nargs='+',
            help='single or multiple file(s) (HDF5)')
    parser.add_argument(
            '-r', metavar=('w','e','s','n'), dest='extent', type=float, nargs=4,
            help=('region for data subset (km)'),
            default=[None, None, None, None])
    parser.add_argument(
            '-t', metavar=('time_range'), dest='time_range', type=float, nargs=2,
            help=('time for data subset'),
            default=[None, None])
    parser.add_argument(
            '-m', metavar=('mask_file'), dest='mask_file', type=str, nargs='+',
            help=('mask for data subset'),
            default=[None])
    parser.add_argument(
            '-c', metavar=('lon','lat'), dest='coord_name', type=str, nargs=2,
            help=('name of x/y variables'),
            default=['lon', 'lat'])
    parser.add_argument(
            '-tn', metavar=('time_name'), dest='time_name', type=str, nargs=1,
            help=('name of time variables'),
            default=['t_dyr'])

    return parser.parse_args()


def geo2imagexy(x, y, gdal_trans):
    '''
    des: from georeferenced location (i.e., lon, lat) to image location(col,row).
    input:
        gdal_proj: obtained by gdal.Open() and .GetGeoTransform(), or by geotif_io.readTiff()['geotrans']
        x: project or georeferenced x, i.e.,lon
        y: project or georeferenced y, i.e., lat
    return: 
        image col and row corresponding to the georeferenced location.
    '''
    a = np.array([[gdal_trans[1], gdal_trans[2]], [gdal_trans[4], gdal_trans[5]]])
    b = np.array([x - gdal_trans[0], y - gdal_trans[3]])
    col_img, row_img = np.linalg.solve(a, b)
    col_img, row_img = np.floor(col_img).astype('int'), np.floor(row_img).astype('int')
    return row_img, col_img

### tiff image reading
def readTiff(path_in):
    '''
    return: 
        img: numpy array, exent: tuple, (x_min, x_max, y_min, y_max) 
        proj info, and dimentions: (row, col, band)
    '''
    RS_Data=gdal.Open(path_in)
    im_col = RS_Data.RasterXSize  # 
    im_row = RS_Data.RasterYSize  # 
    im_bands =RS_Data.RasterCount  # 
    im_geotrans = RS_Data.GetGeoTransform()  # 
    im_proj = RS_Data.GetProjection()  # 
    img_array = RS_Data.ReadAsArray(0, 0, im_col, im_row)  # 
    left = im_geotrans[0]
    up = im_geotrans[3]
    right = left + im_geotrans[1] * im_col + im_geotrans[2] * im_row
    bottom = up + im_geotrans[5] * im_row + im_geotrans[4] * im_col
    extent = (left, right, bottom, up)
    espg_code = osr.SpatialReference(wkt=im_proj).GetAttrValue('AUTHORITY',1)

    img_info = {'geoextent': extent, 'geotrans':im_geotrans, \
                'geosrs': espg_code, 'row': im_row, 'col': im_col,\
                    'bands': im_bands}

    if im_bands > 1:
        img_array = np.transpose(img_array, (1, 2, 0)).astype(np.float)  # 
        return img_array, img_info 
    else:
        return img_array, img_info

def subset(ifile, extent=[None,None,None,None], time_range=[None, None], \
                            extent_mask=[None, None], time_name=None, coord_name=['lon', 'lat']):
    '''args:
        ifile: input file path
        extent: [lon_min, lon_max, lat_min, lat_max], the extent points should be wgs84 coordinate.
        time_range: [time_start, time_end]
        extent_mask: [raster_mask, geotrans_gdal]
        time_name: attribute name for time in h5 file
        coord_name: [cooridinates name for lon, attribute name for lat]
      '''

    print(('input -> ', ifile))
    lon_name, lat_name = coord_name
    path, ext = os.path.splitext(ifile)
    ofile = path+'_subs'+ ext
    ## read in data
    with h5py.File(ifile, 'r') as fi:
        vnames = list(fi.keys())
        vars = [fi[vname][:] for vname in vnames ]
    vars_dict = [[] for vname in vnames]
    vars_dict = dict(zip(vnames, vars))
    ## 1) if extent is given
    if extent[0]:
        lonmin, lonmax, latmin, latmax = extent   # given region
        idx_extent = np.where( (vars_dict[lon_name] >= lonmin) & (vars_dict[lon_name] <= lonmax) & 
                            (vars_dict[lat_name] >= latmin) & (vars_dict[lat_name] <= latmax) )
        for vname in vnames:
            #### -- subset by specific extent
            vars_dict[vname] = vars_dict[vname][idx_extent]

    ## 2) if extent_mask is given
    if extent_mask[0] is not None:     
        #### -- subset by extent_mask
        raster_mask, geotrans_mask = extent_mask
        row, col = geo2imagexy(x=vars_dict[lon_name], \
                            y=vars_dict[lat_name], gdal_trans=geotrans_mask)
        ## ensure the row, col fall in the image
        row[row >= raster_mask.shape[0]] = raster_mask.shape[0]-1
        col[col >= raster_mask.shape[1]] = raster_mask.shape[1]-1
        row[row < 0] = 0; col[col < 0] = 0  
        photon_mask = raster_mask[row, col]
        photon_sel = photon_mask == 1
        for vname in vnames:
            vars_dict[vname] = vars_dict[vname][photon_sel]

    ## 3) if time_range is given
    if time_range[0] and vars_dict[lon_name].any():        
        #### -- subset by specific time
        time_start, time_end = time_range
        idx_time = np.where( (vars_dict[time_name] >= time_start) & (vars_dict[time_name] <= time_end) )
        for vname in vnames:
            vars_dict[vname] = vars_dict[vname][idx_time]

    #### ----- write out file
    if vars_dict[lon_name].any():
        with h5py.File(ofile, 'w') as fo:
            for vname in vnames:
                fo[vname] = vars_dict[vname]
            print(('output ->', ofile))
    else:
        print('output -> None')


if __name__ == '__main__':

    # Pass arguments 
    args = get_args()
    ifiles = args.ifile[:]           # input file(s)
    extent = args.extent[:]          # lon/lat variable names
    mask_path = args.mask_file[:]
    coord_name = args.coord_name[:]
    time_range = args.time_range     # bounding box EPSG (m) or geographical (deg)
    time_name = args.time_name[0]   

    print('Input arguments:')
    for arg in list(vars(args).items()):
        print(arg)
    if mask_path[0]:
        mask_raster, mask_info = readTiff(mask_path[0])
        extent_mask = [mask_raster, mask_info['geotrans']]
    else:
        extent_mask = [None, None]

    [subset(f, extent, time_range, \
                    extent_mask, time_name, coord_name) for f in ifiles]


