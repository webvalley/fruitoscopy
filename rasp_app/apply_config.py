import os
import tarfile
from utils import time_now
from shutil import copyfile

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def apply_configuration(filename):
    tarconfig = tarfile.open(HOME_PATH + '/temp_data/' + filename, mode='r:gz')
    tarconfig.extractall(HOME_PATH + '/temp_data')
    pikol_0 = os.path.isfile(HOME_PATH + '/temp_data/model.pkl')
    pikol_1 = os.path.isfile(HOME_PATH + '/temp_data/model.pkl_01.npy')
    pikol_2 = os.path.isfile(HOME_PATH + '/temp_data/model.pkl_02.npy')
    pikol_3 = os.path.isfile(HOME_PATH + '/temp_data/model.pkl_03.npy')
    json = os.path.isfile(HOME_PATH + '/temp_data/parameters.json')
    if not (pikol_0 and pikol_1 and pikol_2 and pikol_3 and json):
        return 0
    try:
        copyfile(HOME_PATH + '/temp_data/model.pkl', HOME_PATH + '/configuration/model.pkl')
        copyfile(HOME_PATH + '/temp_data/model.pkl_01.npy', HOME_PATH + '/configuration/model.pkl_01.npy')
        copyfile(HOME_PATH + '/temp_data/model.pkl_02.npy', HOME_PATH + '/configuration/model.pkl_02.npy')
        copyfile(HOME_PATH + '/temp_data/model.pkl_03.npy', HOME_PATH + '/configuration/model.pkl_03.npy')
        copyfile(HOME_PATH + '/temp_data/parameters.json', HOME_PATH + '/configuration/parameters.json')
    except:
        return 0
    tarconfig.close()
    return 1

def save_white(array):
    #print(array)
    f = open(HOME_PATH + '/white_cal.txt', 'w')
    f.write(" ".join(map(str, array)))
    f.close()
