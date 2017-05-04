import pandas as pd
import preProcess as pp
import pydotplus as pdp
import BayesClassifier as bc
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from pydotplus import graphviz
from scipy import interp
from sklearn import tree #Decision Tree
from sklearn import svm #Support Vector Machine
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier #Multi-Layer Perceptro
from sklearn.naive_bayes import GaussianNB
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

gColors = ['g','r','c','m','y','k']
iterator = 0

'''
	fxn : crossValidation
	params:
		clf = classifier from sklearn
		x = x vector
		y = y vecto
	Description:
		Runs a 10 fold cross validation test
		on the classifiers to test the correctness of each classifier
'''
def crossValidation(clf,x,y):
	crossVal = int(len(x) / 10)
	confMatrix = {'TP' : 0.0 , 'FN' : 0.0, 'FP' : 0.0, 'TN' : 0.0, 'total' : 0.0, 'accuracy' : 0.0, 'TPR' : [], 'FPR' : [], 'recall' : 0.0, 'f-measure' : 0.0, 'precision' : 0.0}
	for i in range(10):
		trainX = []
		trainY = []
		compY = []
		testX = []
		testY = []
		for j in range(crossVal):#create train portion
			trainX.append(x[i*crossVal + j])
			trainY.append(y[i*crossVal + j])
		clf.fit(trainX, trainY)
		for k in range(1, i*crossVal, 1):#create testX from beginning of list
			testX.append(x[k])
		for k in range(i*crossVal + crossVal, len(x), 1):#create testX from end of list
			testX.append(x[k])
		testY = clf.predict(testX)
		for k in range(1,i*crossVal,1):#create actualY values from beginning of list
			compY.append(y[k])
		for k in range(i*crossVal + crossVal, len(y), 1):#create actualY values from end of list
			compY.append(y[k])
		for k in range(len(compY)):#Find values and populate performance matrix or in this case dictionary
			if (testY[k] == 1 and  compY[k] == 1):
				confMatrix['TP'] += 1
			elif (testY[k] == 0 and compY[k] == 1):
				confMatrix['FN'] += 1
			elif (testY[k] == 1 and compY[k] == 0):
				confMatrix['FP'] += 1
			else:
				confMatrix['TN'] += 1
			confMatrix['total'] += 1
		confMatrix['TPR'].append(confMatrix['TP'] / (confMatrix['TP'] + confMatrix['FN']))
		confMatrix['FPR'].append(confMatrix['FP'] / (confMatrix['TN'] + confMatrix['FP']))
	confMatrix['TPR'] = sorted(confMatrix['TPR'])
	confMatrix['FPR'] = sorted(confMatrix['FPR'])
	rocCurve(testY, compY)
	confMatrix['precision'] = (confMatrix['TP'] / (confMatrix['TP'] + confMatrix['FP']))
	confMatrix['recall'] = (confMatrix['TP'] / (confMatrix['TN'] + confMatrix['FN']))
	confMatrix['f-measure'] = (2 * confMatrix['recall'] * confMatrix['precision']) / (confMatrix['recall'] + confMatrix['precision'])
	confMatrix['accuracy'] = ((confMatrix['TP'] + confMatrix['TN']) / confMatrix['total']) * 100
	return confMatrix

def rocCurve(testY, preds):
	global gColors, iterator
	y = []
	for i in range(len(testY)):
		y.append(testY[i])
	testY = y
	mean_tpr = 0.0
	mean_fpr = np.linspace(0,1,100)
	preds = np.linspace(0.0,1.0,num=len(testY))
	fpr, tpr, threshold = metrics.roc_curve(testY, preds)
	mean_tpr += interp(mean_fpr, fpr, tpr)
	mean_tpr[0] = 0.0
	roc_auc = metrics.auc(fpr, tpr)
	plt.plot(fpr, tpr, color= gColors[iterator], linestyle='-', label='MEAN ROC (area = %0.2f)' % roc_auc)
	plt.plot([0,1],[0,1], linestyle='-', lw=2, color='blue')
	plt.title('Roc Curve')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positirve Rate')
	iterator += 1
	plt.show()
		
'''
	Classifiers
		Simple Functions that feed
		the off-the-shelf classifiers
		to the 10x validation function
'''
def decisionTree(x, y):
	clf = tree.DecisionTreeClassifier()#classifier object
	return crossValidation(clf,x,y)#cross validation
def supportVectorMachine(x,y):
	clf = svm.SVC()#classifier object
	return crossValidation(clf,x,y)#cross validation
def ANN(x,y):
	clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 2), random_state=1)#classifier object
	return crossValidation(clf,x,y)#cross validation
def randomForest(x,y):
	clf = RandomForestClassifier(n_estimators=10)#classifier object
	return crossValidation(clf,x,y)#cross validation
def bayesClassifier(x,y):
	clf = bc.BayesClassifier()
	return crossValidation(clf,x,y)
def rulesBased(x,y):
	clf = GaussianNB()
	return crossValidation(clf,x,y)

#visualization of the decision tree
#This Belongs in the decision tree function
#if you want a pdf of the decision tree.
'''
clf = clf.fit(x,y)
dot_data = StringIO()
#dot_data = tree.export_graphviz(clf, outfile=dot_data)
tree.export_graphviz(clf, out_file=dot_data)
graph = pdp.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf('decisionTree.pdf')
'''


'''
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b', label = 'AUC = %0.2f' % roc_auc)
plt.legend(loc = 'lower right')
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
totFPR = sum(FPR)
totTPR = sum(TPR)
tempFPR = []
tempTPR = []
runningTotalFPR = 0
runningTotalTPR = 0
x = np.arange(0,1.1,0.1)
y = x
for i in range(len(FPR)):
runningTotalFPR += FPR[i]
runningTotalTPR += TPR[i]
tempFPR.append(runningTotalFPR / totFPR)
tempTPR.append(runningTotalTPR / totTPR)
plt.plot(tempFPR, tempTPR, 'b', x,y,'r')
plt.show()
'''
