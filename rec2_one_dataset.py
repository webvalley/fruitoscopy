from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


#MODULO 1
#LABELS SEPARATED FROM THE MATRIX


#loading data
data_tr=np.genfromtxt("arcene_train.data", dtype=bytes, delimiter=' ')
#remove column and row names and convert into float
x_tr=data_tr.astype(np.int)
#check if it work
print(x_tr.shape)

#load training set label
y_tr = np.genfromtxt("arcene_train.labels", dtype=bytes)
y_tr =y_tr.astype(np.int)



#implement the label in the matrix(x_tr)
#x_tr = np.concatenate((x_tr, y_tr.reshape((-1,1))), axis=1)


#do the binning for x_tr

#define window lenght
wl=100
#result of the binning, stat 
stat, bin_edges, binnum = stats.binned_statistic(range(x_tr.shape[1]), x_tr, 'median', bins=100)
#print the graphs
for i in range(stat.shape[0]):
	plt.plot(stat[i])
#really print the graphs	
plt.show()



feat_tr = data_tr[1]
samp_tr= data_tr[1]
#load test set data and labels

data_ts = np.genfromtxt("arcene_valid.data",dtype=bytes, delimiter=' ')
x_ts=data_ts.astype(np.int)    #[1].astype(bytes)
y_ts=np.genfromtxt("arcene_valid.labels",dtype=bytes, delimiter=' ')
y_ts = y_ts.astype(np.int)

 
stat_ts, bin_edges_ts, binnum_ts = stats.binned_statistic(range(x_ts.shape[1]), x_ts, 'median', bins=100)
#print the graphs
for i in range(stat_ts.shape[0]):
	plt.plot(stat_ts[i])
#really print the graphs	
plt.show()



clf=RandomForestClassifier()
clf.fit(stat,y_tr)#x_tr
y_pred = clf.predict(stat_ts)#x_ts

mcc=metrics.matthews_corrcoef(y_ts, y_pred)

ml_models = {}
print(mcc)



