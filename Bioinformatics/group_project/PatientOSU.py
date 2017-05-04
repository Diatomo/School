

'''
	Author: Charles C. Stevenson
	Date: 04/16/107
	Description:
		Patient attributes in the LMS db
'''

import re
from datetime import date

class PatientOSU:

	def __init__(self, ID, dfDate, dfMutation):
		self.ID = ID
		self.hTime = self.__initDays(dfDate)
		self.death = False if dfDate.loc[ID, 'Date of death'] == '-1' else True #Dead or Not
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
		dDate = dfDate.loc[self.ID, 'Date of diagnosis']
		lastFollowUpDate = dfDate.loc[self.ID, 'followUp']
		deathDate = dfDate.loc[self.ID, 'Date of death']
		if (deathDate != '-1'):
			pDate = deathDate
		else:
			pDate = lastFollowUpDate
		dDate = re.split('/', dDate)
		pDate = re.split('/', pDate)
		dDate[2] = (int(dDate[2]) + 2000)
		pDate[2] = (int(pDate[2]) + 2000)
		d0 = date(int(dDate[2]), int(dDate[0]), int(dDate[1]))
		d1 = date(int(pDate[2]), int(pDate[0]), int(pDate[1]))
		delta = d1 - d0 #calculate time.
		return delta.days

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
		if (metastatic == 'yes'):
			metastatic = True
		else:
			metastatic = False
		return metastatic
