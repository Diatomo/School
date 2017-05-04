


import pandas as pd
import PatientOSU as pOSU
import PatientTCGA as pTCGA
import Rule

def setup(date, mutation, osu=None):
	patients = []
	dfDate = pd.read_csv(date)
	dfMutation = pd.read_csv(mutation)
	for i in range(len(dfMutation)):
		if (osu):
				patients.append(pOSU.PatientOSU(i, dfDate, dfMutation))
		else:
				patients.append(pTCGA.PatientTCGA(i, dfDate, dfMutation))
	return patients

def outputPatients(patients):
	for patient in patients:
		print('\n')
		print('Patient ID: %d' % patient.ID)
		print('Hopital Time: %d' % patient.hTime)
		print('Is the patient dead: %r' % patient.death)
		print('Mutation Format: ' + str(patient.mutations['ATRX']))
		print('\n')

def generateRules(df, patients, meta = None):
	ruleList = []
	genes = list(df)
	genes.remove('Metastatic')
	booleans = [True, False]
	for booleanA in booleans:#If true || false
		for i in range(len(genes)): #check all of genes in first list
			geneA = genes[i]
			ruleList.append(Rule.Rule(geneA, booleanA))#append single gene
			for patient in patients:#Append all patients that fit the patient
				if (patient.mutations[geneA] == booleanA and patient.metastatic == meta):
					ruleList[-1].patients.append(patient)
			for booleanB in booleans:
				for j in range(i, len(genes),1):
					geneB = genes[j]
					if (geneA != geneB):
							ruleList.append(Rule.Rule(geneA, booleanA, gene2=geneB, value2=booleanB))
							for patient in patients:
								if (patient.mutations[geneA] == booleanA and patient.mutations[geneB] == booleanB and patient.metastatic == meta):
									ruleList[-1].patients.append(patient)
	return ruleList

def cleanRules(rules):
	temp = []
	for i in range(len(rules)):
		if (len(rules[i].patients) < 3):
			temp.append(rules[i])
	for i in range(len(temp)):
			rules.remove(temp[i])
	return rules

def ruleOutput(rules):
	for i in range(len(rules)):
		print('Gene: %s :: Value: %r' % (rules[i].gene1, rules[i].val1))
		print('==============================================================')
		if (rules[i].gene2 != None):
			print('Gene: %s :: Value: %r' % (rules[i].gene2, rules[i].val2))
		print('Patients')
		print('==============================================================')
		outputPatients(rules[i].patients)				
		print('==============================================================')

def buildDf(rules):
	attributes = ['geneA', 'geneB', 'number of patients']
	df = pd.DataFrame(index = range(len(rules)), columns=attributes)
	for i in range(len(rules)):
		if (rules[i].val1 == False and rules[i].val2 == False):
			df.loc[i] = [('!' + rules[i].gene1),('!' + rules[i].gene2), len(rules[i].patients)]
		elif (rules[i].val1 == False and rules[i].val2 == True):
			df.loc[i] = [('!' + rules[i].gene1), rules[i].gene2, len(rules[i].patients)]
		elif (rules[i].val1 == True and rules[i].val2 == False):
			df.loc[i] = [rules[i].gene1,('!' + rules[i].gene2), len(rules[i].patients)]
		elif (rules[i].val1 == True and rules[i].val2 == True):
			df.loc[i] = [rules[i].gene1, rules[i].gene2, len(rules[i].patients)]
		elif ((rules[i].val1 == True or rules[i].val1 == False) and rules[i].val2 == None):
			df.loc[i] = [rules[i].gene1, 'None', len(rules[i].patients)]
	return df

def main():

	patient_OSU = setup('LMS_OSU_DATES.csv', 'LMS_OSU_MUTATION.csv', osu=True)
	patient_TCGA = setup('LMS_TCGA_DATES.csv', 'LMS_TCGA_MUTATION.csv', osu=False)

	'''
	print('OSU PATIENTS')
	#outputPatients(patient_OSU)
	print('TCGA PATIENTS')
	#outputPatients(patient_TCGA)
	'''
	'''
	print('\nGenerating Rules List for OSU Metastatic......')
	dfMutation = pd.read_csv('LMS_OSU_MUTATION.csv')
	rOSU = generateRules(dfMutation, patient_OSU, meta=True)
	print('Cleaning the Rules list for OSU METASTATIC.......')
	print('Before length: %d' % len(rOSU))
	rOSU = cleanRules(rOSU)
	print('After length: %d' % len(rOSU))
	df = buildDf(rOSU)
	df.to_csv('df_OSU_LMS_METASTATIC.csv')
	print("COMPLETED OSU RULE LIST!! METASTATIC")


	print('\n Generating Rules List for OSU Non-Metastatic')
	rOSU = generateRules(dfMutation, patient_OSU, meta=False)
	print('Cleaning the Rules list for OSU NONMETASTATIC.......')
	print('Before length: %d' % len(rOSU))
	rOSU = cleanRules(rOSU)
	print('After length: %d' % len(rOSU))
	df = buildDf(rOSU)
	df.to_csv('df_OSU_LMS_NON-METASTATIC.csv')
	print("COMPLETED OSU RULE LIST!! NON-METASTATIC")
	'''

	print('\nGenerating Rules List for TCGA Metastatic......')
	dfMutation = pd.read_csv('LMS_TCGA_MUTATION.csv')
	rTCGA = generateRules(dfMutation, patient_TCGA, meta=True)
	print('Before length: %d' % len(rTCGA))
	rTCGA = cleanRules(rTCGA)
	print('After length: %d' % len(rTCGA))
	df = buildDf(rTCGA)
	df.to_csv('df_TCGA_LMS_METASTATIC.csv')
	print("COMPLETED TCGA RULE LIST!! METASTATIC")


	print('\nGenerating Rules List for TCGA Non-Metastatic......')
	dfMutation = pd.read_csv('LMS_TCGA_MUTATION.csv')
	rTCGA = generateRules(dfMutation, patient_TCGA, meta=False)
	print('Before length: %d' % len(rTCGA))
	rTCGA = cleanRules(rTCGA)
	print('After length: %d' % len(rTCGA))
	df = buildDf(rTCGA)
	df.to_csv('df_TCGA_LMS_NON-METASTATIC.csv')
	print("COMPLETED TCGA RULE LIST!! Non-METASTATIC")

	#ruleOutput(rOSU)
	'''
	df = buildDf(rOSU)
	df.to_csv('df_OSU_LMS.csv')
	df = buildDf(rTCGA)
	df.to_csv('df_TCGA_LMS.csv')
	'''
	
	#2 time columns
	#days to death
	#days to last follow-up
			
main()
