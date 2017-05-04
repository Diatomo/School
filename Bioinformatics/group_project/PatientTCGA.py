
'''
	Author: Charles C. Stevenson
	Date: 04/16/107
	Description:
		Patient attributes in the TCGA db
'''

import re
from datetime import date

class PatientTCGA:

	def __init__(self, ID, dfDate, dfMutation):
		self.ID = ID
		self.hTime = self.__initDays(dfDate)
		self.death = False if dfDate.loc[ID, 'days to death'] != 0 else True #Dead or Not
		self.mutations = self.__initMutations(dfMutation)#Dictionary of Genes and If mutates {gene : mutation::boolean}
		self.metastatic = self.__initMetastatic(dfMutation)
	'''
		fxn : initDays
		params :
			dfDate = pandas dataframe
		Description:
			extract time span between diagnosis
			and last day or date of death.
	'''
	def __initDays(self, dfDate):
		dDate = dfDate.loc[self.ID, 'follow up']
		deathDate = dfDate.loc[self.ID, 'days to death']
		return dDate + deathDate

	'''
		fxn : initMutations
		params :
			dfMutation = pandas dataframe
				contains genes and whether or not they are mutated (True or False)
		Description:
			builds a dictionary of {gene : boolean}
	'''
	def __initMutations(self, dfMutation):
		mutations = {}
		labels = list(dfMutation)
		for label in labels:
			if (dfMutation.loc[self.ID, label] == False):
				mutations[label] = False
			else:
				mutations[label] = True
		return mutations


	def __initMetastatic(self, dfMutation):
		metastatic = dfMutation.loc[self.ID,'Metastatic'] 
		if (metastatic == 'YES'):
			metastatic = True
		elif (metastatic == 'NO'):
			metastatic = False
		else:
			metastatic = None
		return metastatic
