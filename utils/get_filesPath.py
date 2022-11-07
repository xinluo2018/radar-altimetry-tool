## author: xin luo 
# creat: 2022.9.26
# des: get specific files in the given directory.


import os

def get_filesPath(base, key_words):
    '''
    get the files path corresponding to the search directory and specific key words
    input: 
        base: str, search directory
        key_words: str, specific word in the file name, e.g., "enhanced_measurement.nc", 
    ouput:
        files_path: list, contains all the obtained file paths (string).
    '''
    if base == '':
        base = os.getcwd()
    file_paths = []
    for root, ds, fs in os.walk(base):
        for f in fs:
            file_path = os.path.join(root, f)
            if key_words in file_path:
                file_paths.append(file_path)
    return file_paths


