
'''
    Author: Charles Stevenson
    Date: 01/21/2017
    Description: Naive Bayes Classifier
'''

'''
    params
        @f = file
        @poison = poison dictionary
        @edible = edible dictionary
'''
def bayes(f, poison, edible):
    predictT = 0.0
    predictF = 0.0
    for record in f:
        #print(record)
        record = record[:-1]
        record = record.split(',')
        pP = 1#probability of poison
        pE = 1#probability of edible
        #dot product of the evidence
        for i in range(1,len(record),1):
            if (i == 1):
                pP *= poison['p'][i][record[i]]+1
            else:
                pP *= poison['p'][i][record[i]]
        for i in range(1,len(record),1):
            if (i == 1):
                pE *= edible['e'][i][record[i]]+1
            else:
                pE *= edible['e'][i][record[i]]

        #compare poison and edible probability after dot product
        if (pP > pE):
            if (record[0] == 'p'):
                predictT += 1
            else:
                predictF += 1
        elif (pP < pE):
            if (record[0] == 'e'):
                predictT += 1
            else:
                predictF += 1
        else:
             print("VALUES ARE EQUAL!!")

    #return prediction rating
    return (predictT / (predictF + predictT))
'''
    Params
    @classifier = poison or edible dictionary
    @record = line in the file
'''
def count(classifier, record):
    #counts the value for each descriptor of each attribute of each record
    #count descriptors per attribute
    for i in range(1,len(record),1):
            classifier[record[0]][i][record[i]] += 1
'''
    Params
        @f = file
        @poison = poison dictionary
        @edible = edible dictionary
        @totals = totals dictionary
'''
def tally(f, poison, edible, totals):
    #tallies count for each classification: poison && edible
    for record in f:
        record = record[:-1]
        record = record.split(',')
        for i in range(1,len(record),1):
            if (record[i] not in poison['p'][i]):
                poison['p'][i].update({record[i] : 0})
            if (record[i] not in edible['e'][i]):
                edible['e'][i].update({record[i] : 0})
        if (record[0] == 'p'):
            count(poison, record)
            totals['poison'] += 1.0
        else:
            count(edible, record)
            totals['edible'] += 1.0
'''
    Params
        @f = file
        @poison = poison dictionary
        @edible = edible dictionary
        @totals = totals dictionary
'''
def calcProbabilities(f, poison, edible, totals):
    #iterates through the dictionaries
    #and calculates the probabilities
    tally(f,poison,edible,totals)
    for i in range(1,23,1):
        for key, value in poison['p'][i].items():
             poison['p'][i][key] = poison['p'][i][key] / totals['poison']
    for i in range(1,23,1):
        for key, value in edible['e'][i].items():
             edible['e'][i][key] = edible['e'][i][key] / totals['edible']
'''
    Params
        @f = file
        @poison = poison dictionary
        @edible = edible dictionary
'''
def setup(f, poison, edible):
    #setup for the edible and poison dictionary for each attribute
    #occurding to the amount of attributes in a line of the file
    attributes = {}
    counter = 1
    for attribute in f:#setup a lookup table; && populates poison and edible dicts
        attribute = attribute[:-1]
        attributes.update({attribute : counter})
        poison['p'].update({attributes[attribute] : {}})
        edible['e'].update({attributes[attribute] : {}})
        counter += 1
    return attributes

def main():
    mushrooms = open('agaricus-lepiota.data.train.txt', 'r+')
    tMushrooms = open('agaricus-lepiota.data.test1.txt', 'r+')
    fAttributes = open('attributes.txt', 'r+')

    totals = {'poison' : 0, 'edible' : 0}
    poison = {'p' : {}}
    edible = {'e' : {}}
    attributes = setup(fAttributes, poison, edible)
    fAttributes.close()

    calcProbabilities(mushrooms, poison, edible, totals)
    mushrooms.close()

    prediction = bayes(tMushrooms, poison, edible)
    tMushrooms.close()
    print("Prediction Efficiency = " + str(prediction*100))


main()

