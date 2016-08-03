import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from scipy import stats
from sklearn import svm
from sklearn.externals import joblib
import json

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

#MODULO 1
#LABELS SEPARATED FROM THE MATRIX
def get_label(array):

    with open(HOME_PATH + '/configuration/parameters.json') as data_file:
        dic = json.load(data_file)
    try:
        bin_num = dic['num_bins']
    except:
        print("Error with json reading")
        bin_num = 130
    # get spectra data from RaspberryPi
    test = array

    # bin the data
    test_data,bin_edges_ts,binnum_ts=stats.binned_statistic(range(len(test)), test, 'median', bins=int(bin_num))

    # load model from pkl file
    a_result=joblib.load(HOME_PATH + '/configuration/model.pkl')

    #print((test_data))
    # apply model to RaspberryPi spectra data
    result = int(a_result.predict(test_data.reshape(1,-1)))

    return result
