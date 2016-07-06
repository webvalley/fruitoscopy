from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from scipy import stats
from sklearn import svm
from sklearn.externals import joblib
import json

#MODULO 1
#LABELS SEPARATED FROM THE MATRIX
def get_label(array):

    with open(HOME_PATH + '/configuration/parameters.json') as data_file:
        dic = json.load(data_file)
    bin_num = dic['num_bins']

    # get spectra data from RaspberryPi
    test = array

    # bin the data
    test_data,bin_edges_ts,binnum_ts=stats.binned_statistic(range(test.shape[1]), test, 'median', bins=int(bin_num))

    # load model from pkl file
    a_result=joblib.load(HOME_PATH + '/configuration/model.pkl')

    # apply model to RaspberryPi spectra data
    for i in test_data:
        print("RESULT: %d" % int(a_result.predict(i.reshape(1,-1))))
