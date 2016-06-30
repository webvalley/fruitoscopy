from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import metrics
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.lda import LDA

#MODULO 1
#LABELS SEPARATED FROM THE MATRIX


#loading data
X = np.genfromtxt("arcene.data", dtype=np.int, delimiter=' ')
#remove column and row names and convert into float

#load training set label
y = np.genfromtxt("arcene.labels", dtype=np.int)



#implement the label in the matrix(x_tr)
#x_tr = np.concatenate((x_tr, y_tr.reshape((-1,1))), axis=1)


#do the binning for x_tr

#define window length
ml_models = {'Random Forest': [RandomForestClassifier(n_estimators=500)],
             'Support Vector Classifier': [SVC(C=i) for i in np.arange(5,1000,10)]
            }

bin_number=100
window_length=X.shape[1]/bin_number

#result of the binning, stat 
stat, bin_edges, binnum = stats.binned_statistic(range(X.shape[1]), X, 'median', bins=bin_number)
#print the graphs
#for i in range(stat.shape[0]):
#	plt.plot(stat[i])
#really print the graphs	
#plt.show()

for keys, models in ml_models.items():
    for model in models:
        scores = cross_validation.cross_val_score(model, X, y, cv=5)
        print(keys, scores.mean())

'''
clf.fit(stat,y_tr)#x_tr
y_pred = clf.predict(stat_ts)#x_ts

mcc=metrics.matthews_corrcoef(y_ts, y_pred)

ml_models = {}
print(mcc)
'''


