# author: Fernando Paolo;
# modify: xin luo, 2021.8.10.  

"""
des: merges several HDF5 files into a single file or multiple larger files.
example
    merge.py path/to/ifiles_*.h5 -o path/to/ofile.h5
    merge.py path/to/ifiles_*.h5 -o path/to/ofile.h5 -m 5 -n 5
notes
    - The parallel option (-n) only works for multiple outputs (-m)!
    - If no 'key' is given, it merges files in the order they are passed/read.
    - If receive "Argument list too long", pass a string.
    - See complementary program: split.py
"""

import warnings

from numpy.core.fromnumeric import compress
warnings.filterwarnings("ignore")
import os
import h5py
import argparse
import numpy as np
from glob import glob


def get_args():
    """ Pass command-line arguments. """
    parser = argparse.ArgumentParser(
            description='Merges several HDF5 files.')
    parser.add_argument(
            'ifile', metavar='ifile', type=str, nargs='+',
            help='HDF5 file paths to merge')
    parser.add_argument(
            '-o', metavar='ofile', dest='ofile', type=str, nargs=1,
            help=('output file path'),
            default=[None], required=True,)
    parser.add_argument(
            '-m', metavar='nfiles', dest='nfiles', type=int, nargs=1,
            help=('number of merged files (blocks)'),
            default=[1],)
    parser.add_argument(
            '-v', metavar='var', dest='vnames', type=str, nargs='+',
            help=('only merge specific vars if given, otherwise merge all'),
            default=[],)
    parser.add_argument(
            '-z', metavar=None, dest='comp', type=str, nargs=1,
            help=('compress merged file(s)'),
            choices=('lzf', 'gzip'), default=[None],)
    parser.add_argument(
            '-k', metavar='key', dest='key', type=str, nargs=1,
            help=('sort files by numbers after `key` in file name'),
            default=[None],)
    parser.add_argument(
            '-n', metavar='njobs', dest='njobs', type=int, nargs=1,
            help=('number of jobs for parallel processing when using -m'),
            default=[1],)
    return parser.parse_args()


def get_total_len(ifiles):
    """ des: Get total output length from all input files. 
        arg:
            ifiles: preprocessed h5 file, consist of only Dataset.
        return:
            N: length of the Dataset. 
    """
    N = 0
    for fn in ifiles:
        with h5py.File(fn) as f:
            N += list(f.values())[0].shape[0]
    return N


def get_var_names(ifile):
    """ des: return all '/variable' names in the HDF5. 
        arg: 
            files: str, the h5 file name.
        return:
            vanems: list, Dataset names or the Group names in h5 file
                    if the processed h5 file consist of Dataset, 
                    the names are var names.
    """
    with h5py.File(ifile, 'r') as f:
        vnames = list(f.keys())
    return vnames


def get_multi_io(ifiles, ofile, nfiles):
    """ des: Construct multiple input/output file names in the data merging. 
            required in the parallel processing 
        arg: 
            ifiles: list, consist of paths of multiple h5 files.
            ofile: paths of output file
            nfiles: groups of the input files should be divide into.
        retrun:
            ifiles: list, consist of multiple list of which contains files in one specific group.
            ofiles: list, consist of output paths that corresponding to files in specific groups.
    """
    # List of groups of input files
    ifiles = [list(arr) for arr in np.array_split(ifiles, nfiles)]
    # List of output file names
    fname = os.path.splitext(ofile)[0] + '_%02d.h5'
    ofiles = [(fname % k) for k in range(len(ifiles))]
    return ifiles, ofiles


# Sort input files by key 
def sort_files(ifiles, key=None):
    """ des: sort files by numbers *after* the key in the file name. 
        example: file name-> ..._year_2010_....h5, the key set to year, the files will sorted by year
        arg: 
            ifiles: list, contains multiple h5 files
            key: str, the key feature for sorting  
    """
    if key:
        import re
        print('sorting input files ...')
        natkey = lambda s: int(re.findall(key+'_\d+', s)[0].split('_')[-1])
        ifiles.sort(key=natkey)


def merge(ifiles, ofile, vnames, comp):
    ''' 
    des: merge the similar files into one file
    arg:
        ifiles: list with strs, files need to be merged.
        ofile: str, the name of the merged file.     
    retrun:
        none
    '''
    # Get length of output containers (from all input files)
    print('Calculating lenght of output from all input files ...')
    N = get_total_len(ifiles)   # 

    with h5py.File(ofile, 'w') as out_f, h5py.File(ifiles[0], 'r') as in_f_0:
        for key in vnames:
            shape_var = in_f_0[key][:].shape
            if len(shape_var) == 1:                        
                out_f.create_dataset(key, (N,), dtype=None, compression=comp)
            else:
                # out_f.create_dataset(key, (N, shape_var[1]), dtype='float32', compression=comp)
                out_f.create_dataset(key, (N, shape_var[1]), dtype=None, compression=comp)

        # Iterate over the input files
            k1 = 0
            for ifile in ifiles:
                print(('reading', ifile))
                # Write next chunk (the input file)
                with h5py.File(ifile, 'r') as f2:
                    k2 = k1 + list(f2.values())[0].shape[0]  # k1, k2: the location of the var in the merged file
                    # Iterate over all variables
                    out_f[key][k1:k2] = f2[key][:]
                k1 = k2
    
    print(('merged', len(ifiles), 'files'))
    print(('output ->', ofile))


if __name__ == '__main__':

    args = get_args() 
    ifile = args.ifile[:]       # list
    ofile = args.ofile[0]       # str
    nfiles = args.nfiles[0]
    vnames = args.vnames
    comp = args.comp[0]
    key = args.key[0]
    njobs = args.njobs[0]
    if os.path.exists(ofile): os.remove(ofile)
    # In case a string is passed to avoid "argument list too long"
    if len(ifile) == 1:
        ifile = glob(ifile[0])

    # sort files before merging
    sort_files(ifile, key=key)

    # get var names from first file, if not provided
    vnames = get_var_names(ifile[0]) if not vnames else vnames

    # groups of input files -> multiple output files
    if nfiles > 1:
        ifile, ofile = get_multi_io(ifile, ofile, nfiles)
    else:
        ifile, ofile = [ifile], [ofile]

    if njobs > 1 and nfiles > 1:
        print(('Running parallel code (%d jobs) ...' % njobs))
        from joblib import Parallel, delayed
        Parallel(n_jobs=njobs, verbose=5)(
                delayed(merge)(fi, fo, vnames, comp) \
                        for fi, fo in zip(ifile, ofile))
    else:
        print('Running sequential code ...')
        [merge(fi, fo, vnames, comp) for fi, fo in zip(ifile, ofile)]


