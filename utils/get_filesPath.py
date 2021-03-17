import os

# def get_filesPath(dir, l2_product = 'enhanced_measurement.nc'):
#     '''
#     get the files name corresponding to the giving directory
#     input: 
#         dir: str, files directory
#         l2_product: product stype, e.g., enhanced_measurement.nc, 
#         standard_measurement.nc...
#     ouput:
#         f_names_filter: list, contains all the file names (string).
#     '''
#     f_paths = os.listdir(dir)
#     f_paths_filter = []
#     for i in f_paths:
#         if os.path.splitext(i)[1] == '.SEN3':
#             path = os.path.join(dir, i, l2_product)
#             f_paths_filter.append(path)
#     return f_paths_filter

def get_filesPath(base, key_words):    
    '''
    get the files path corresponding to the search directory and specific key words
    input: 
        base: str, search directory
        key_words: str, specific word in the file name, e.g., "enhanced_measurement.nc", 
    ouput:
        files_path: list, contains all the obtained file paths (string).
    '''
    file_paths = []
    for root, ds, fs in os.walk(base):
        for f in fs:
            file_path = os.path.join(root, f)
            if key_words in file_path:
                file_paths.append(file_path)
    return file_paths