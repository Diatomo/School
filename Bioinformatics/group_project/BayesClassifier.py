
'''
    Author: Charles Stevenson
    Date: 01/21/2017
    Description: Naive Bayes Classifier
'''

import numpy as np
import random

class BayesClassifier:

	def __init__(self):
		self.attributes = {1 : {'RB1' : 0, '!RB1' : 0, 'Non' : 0}, 0: {'RB1' : 0, '!RB1' : 0, 'Non' : 0}}
		self.__pPos = 0.0
		self.__pNeg = 0.0

	def fit(self, netA, netB, osu):
		for i in range(len(osu)):
			satisfy = True
			if (osu.loc[i]['Metastatic'] == 'yes'):
				if (osu.loc[i]['RB1'] == True):
					for j in netA:
						if ((j[0] == '!' and osu.loc[i][j[1:]] == True) or (j[0] != '!' and osu.loc[i][j[1:]] == False)):
							satisfy = False
							self.attributes[1]['Non'] += 1.0
					if (satisfy):
						self.attributes[1]['RB1'] += 1.0
				else:
					for j in netB:
						if ((j[0] == '!' and osu.loc[i][j[1:]] == True) or (j[0] != '!' and osu.loc[i][j[1:]] == False)):
							satisfy = False
							self.attributes[1]['Non'] += 1.0
					if (satisfy):
						self.attributes[1]['!RB1'] += 1.0
			elif (osu.loc[i]['Metastatic'] == 'no'):
				if (osu.loc[i]['RB1'] == True):
					for j in netA:
						if ((j[0] == '!' and osu.loc[i][j[1:]] == True) or (j[0] != '!' and osu.loc[i][j[1:]] == False)):
							satisfy = False
							self.attributes[0]['Non'] += 1.0
					if (satisfy):
						self.attributes[0]['RB1'] += 1.0
				else:
					for j in netB:
						if ((j[0] == '!' and osu.loc[i][j[1:]] == True) or (j[0] != '!' and osu.loc[i][j[1:]] == False)):
							satisfy = False
							self.attributes[0]['Non'] += 1.0
					if (satisfy):
						self.attributes[0]['!RB1'] += 1.0

		totalA = (self.attributes[1]['RB1'] + self.attributes[1]['!RB1'])
		totalB = (self.attributes[0]['RB1'] + self.attributes[0]['!RB1'])
		self.attributes[1]['RB1'] = self.attributes[1]['RB1'] / totalA
		self.attributes[1]['!RB1'] = self.attributes[1]['!RB1'] / totalA
		self.attributes[0]['RB1'] = self.attributes[0]['RB1'] / totalB
		self.attributes[0]['!RB1'] = self.attributes[0]['!RB1'] / totalB
						
	def predict(self, netA, netB, tcga):
		pMeta = 45.0 
		pNonMeta = 15.0 
		correct = 0
		incorrect = 0
		predict = []
		for i in range(len(tcga)):
			satisfy = True
			probClassMeta = 0
			probClassNMeta = 0
			if (tcga.loc[i]['RB1'] == True):
					for j in netA:
						if ((j[0] == '!' and tcga.loc[i][j[1:]] == True) or (j[0] != '!' and tcga.loc[i][j[1:]] == False)):
							satisfy = False
							print('Non-conform')
			elif(tcga.loc[i]['RB1'] == False):
					for j in netB:
						if ((j[0] == '!' and tcga.loc[i][j[1:]] == True) or (j[0] != '!' and tcga.loc[i][j[1:]] == False)):
							satisfy = False
							print('Non-conform')
			if (satisfy):
				if (tcga.loc[i]['RB1'] == True):
					probClassMeta = self.attributes[1]['RB1']
					probClassNMeta = self.attributes[0]['RB1']
				elif (tcga.loc[i]['RB1'] == False):
					probClassMeta = self.attributes[1]['!RB1']
					probClassNMeta = self.attributes[0]['!RB1']
				if (probClassMeta > probClassNMeta):
					predict.append(1)
				elif (probClassMeta < probClassNMeta):
					predict.append(0)

		for i in range(len(predict)):
			if (tcga.loc[i]['Metastatic'] == 'yes' and predict[i] == 1 or tcga.loc[i]['Metastatic'] == 'no' and predict[i] == 0):
				correct += 1.0
			else:
				incorrect += 1.0

		print('ACCURACY = ' + str(correct / (correct + incorrect)))





				

