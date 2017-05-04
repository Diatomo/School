

'''
	Author: Charles C. Stevenson
	Date: 03/17/2017
	Description:
		Some algorithms to try to predict the feauture
		selection of the red_wine dataset
'''


from sklearn import datasets
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier


def recursiveFeatureElimination(x,y):
	model = LogisticRegression()
	rfe = RFE(model, 10)
	rfe = rfe.fit(x, y)
	print(rfe.support_)
	print(rfe.ranking_)

def featureImportance(x,y):
	model = ExtraTreesClassifier()
	model.fit(x, y)
	print(model.feature_importances_)
