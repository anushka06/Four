import sys
from sklearn.cluster import KMeans
import numpy as np
import scipy
import matplotlib.pyplot as plt
import sklearn
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import ShuffleSplit
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error


def loadData(filename):
	X = []
	Y = []
	with open(filename) as f:
		content = f.readlines()
	for item in content:
		X.append(item.split()[1:])
		Y.append(item.split()[0])
	return X, Y

if __name__=="__main__":
	X_, y = loadData(sys.argv[1])
	X_new = preprocessing.scale(X_)
	cluster_no = sys.argv[1]
	if cluster_no==1:
		num_features = 3
		feel_dict = {"neutral":2,"disgust":0,"panic":0,"anxiety":2,"hot":1,"cold":2,"despair":2,"sadness":0,"elation":1,"happy":1,"interest":1,"boredom":2,"shame":2,"pride":2,"contempt":0}
	if cluster_no==2:
		num_features = 3
		feel_dict = {"anxiety":1,"boredom":2,"cold":1,"contempt":2,"despair":2,"disgust":1,"elation":1,"happy":2,"hot":1,"interest":0,"neutral":0,"panic":1,"pride":1,"sadness":2,"shame":1}
	if cluster_no==3:
		num_features = 2
		feel_dict = {"anxiety":1,"boredom":0,"cold":1,"contempt":1,"despair":0,"disgust":0,"elation":0,"happy":0,"hot":0,"interest":1,"neutral":1,"panic":0,"pride":1,"sadness":0,"shame":1}
	if cluster_no==4:
		feel_dict = {"anxiety":2,"boredom":2,"cold":0,"contempt":2,"despair":2,"disgust":0,"elation":1,"happy":0,"hot":1,"interest":0,"neutral":2,"panic":2,"pride":1,"sadness":2,"shame":0}
	if cluster_no==5:
		num_features = 3
		feel_dict = {"anxiety":1,"boredom":1,"cold":1,"contempt":1,"despair":0,"disgust":1,"elation":1,"happy":1,"hot":1,"interest":1,"neutral":2,"panic":2,"pride":1,"sadness":1,"shame":1}

	Y_new = []
	for item in y:
		Y_new.append(feel_dict[item])

	rs = ShuffleSplit(n_splits=10, test_size=.10, random_state=0)
	lis = []
	for train_index, test_index in rs.split(X_new):
		lis.append([train_index, test_index])
	acc = []
	for item in lis:
		X = []
		x_test = []
		Y = []
		y_test = []
		train_in = item[0]
		test_in = item[1]
		for i in train_in:
			X.append(X_new[i])
			Y.append(Y_new[i])
		for i in test_in:
			x_test.append(X_new[i])
			y_test.append(Y_new[i])

		p = np.zeros(28)
		#cluster_mean_list = [[] for i in range(num_features)]
		cluster_mean_list = [p, p, p]
		count_list = np.zeros(num_features)
		for i in range(0,num_features):
			for j in range(0,len(Y)):
				if Y[j] == i:
					count_list[i] = count_list[i] + 1
					cluster_mean_list[i] = cluster_mean_list[i] + np.asarray(X[j])
						
		for i in range(0,len(cluster_mean_list)):
			#print count_list[i]
			cluster_mean_list[i][:] = [x / count_list[i] for x in cluster_mean_list[i]]
		
		no_change = False
		cluster_assign = np.zeros(len(Y))
		iteration = 0
		while no_change == False:
			# recluster
			iteration = iteration + 1
			no_change = True
			for i in range(0, len(X)):
				feature = np.asarray(X[i])
				dis = float('inf')
				for j in range(0,len(cluster_mean_list)):
					cluster_dist = scipy.spatial.distance.euclidean(np.asarray(cluster_mean_list[j]), feature)
					#print j, "cluster == >", cluster_dist
					if cluster_dist < dis:
						assign = j
						dis = cluster_dist
				if iteration == 1:
					cluster_assign[i] = assign
					no_change = False
				else:
					if assign != cluster_assign[i] :
						cluster_assign[i] = assign
						no_change = False
			#print cluster_assign
			#recalculate mean
			if no_change == False:
				p = np.zeros(28)
				cluster_mean_list = [p, p, p]
				count_list = np.zeros(num_features)
				for i in range(0,num_features):
					for j in range(0,len(cluster_assign)):
						if cluster_assign[j] == i:
							count_list[i] = count_list[i] + 1
							cluster_mean_list[i] = cluster_mean_list[i] + np.asarray(X[j])

				for i in range(0,len(cluster_mean_list)):
					cluster_mean_list[i][:] = [x / count_list[i] for x in cluster_mean_list[i]]
			


		pred = []
		for i in range(0,len(x_test)):
			feature = x_test[i]
			dis = float('inf')
			for j in range(0,len(cluster_mean_list)):
				cluster_dist = scipy.spatial.distance.euclidean(np.asarray(cluster_mean_list[j]), feature)
				if cluster_dist < dis:
					assign = j
					dis = cluster_dist
			pred.append(assign)
		pred = np.asarray(pred)
		count = 0
		missclass = 0
		acc.append(accuracy_score(pred, y_test))
	print np.mean(acc)
	

			
			


		



