
'''
    Author: Charles Stevenson
    Date: 01/21/2017
    Description: Naive Bayes Classifier
'''

import numpy as np
import random

class BayesClassifier:

	def __init__(self):
		self.attributes = {}
		self.__pPos = 0.0
		self.__pNeg = 0.0

	def fit(self, x, y):
		total = len(y)
		for i in range(len(x[0])):
			if i not in self.attributes:
				self.attributes[i] = {1: {'a': 0.0, 'b' : 0.0, 'c' : 0.0, 'd' : 0.0, 'e' : 0.0, 'f' : 0.0}, 0 : {'a' : 0.0, 'b' : 0.0, 'c' : 0.0, 'd' : 0.0, 'e' : 0.0, 'f' : 0.0}}
		for i in range(len(x)):
			for j in range(len(x[i])):
				if (x[i][j] not in self.attributes[j][y[i]]):
					self.attributes[j][y[i]].update({x[i][j] : 1.0})
				else:
					self.attributes[j][y[i]][x[i][j]] += 1.0
				if (y[i] == 1.0):
					self.__pPos += 1.0
				elif (y[1] == 0):
					self.__pNeg += 1.0
		for i in range(len(x[0])):
			for key,value in self.attributes[i][1].items():
				self.attributes[i][1][key] = self.attributes[i][1][key] / total
			for key,value in self.attributes[i][0].items():
				self.attributes[i][0][key] = self.attributes[i][0][key] / total
			self.__pPos = self.__pPos / total
			self.__pNeg = self.__pNeg / total

	def predict(self, x):
		y = []
		for i in range(len(x)):
			pos = 1
			neg = 1
			for j in range(len(x[i])):
				pos *= self.attributes[j][1][x[i][j]]
				neg *= self.attributes[j][0][x[i][j]]
			temp = random.randint(0,1)
			pos *= self.__pPos
			neg *= self.__pNeg
			if (pos > neg):
				y.append(1.0)
			else:
				y.append(0.0)
		return y

