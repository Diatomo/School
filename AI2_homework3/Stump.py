

'''
    STUMP CLASSIFIER

'''

'''
========================================
    Author : Charles C. Stevenson (Diatomo)
    Date : February 24, 2017
    Description:
        Stump Classifier
            (1st-Q in decision tree)
========================================
'''
import math as m

class Stump:

    def __init__(self,question,examples):
        self.total = 0
        self.question = question
        self.weight = 0
        self.nodes = self.__initNode__(examples)
        self.gain = []
        self.entropy = self.__initEntropy__()

    def __initNode__(self, examples):
        nodes = {}
        for example in examples:
            self.total += 1.0
            if (example.example[self.question] not in nodes):
                nodes[example.example[self.question]] = {1 : [], -1 : []}
                nodes[example.example[self.question]][int(example.example[-1])].append(example)
            else:
                nodes[example.example[self.question]][int(example.example[-1])].append(example)
        return nodes

    def __initEntropy__(self):
        entropy = []
        print(self.nodes)
        for i in range(len(self.nodes)):
            positive = len(self.nodes[str(i)][1])
            negative = len(self.nodes[str(i)][-1])
            total = positive + negative
            #entropy.append((-positive/total * m.log(positive/total,2) - negative/total * m.log(negative / total,2)))
            entropy.append((-positive/total * m.log(positive/total,2) -
                             negative/total * m.log(negative / total,2)))
            self.gain.append((total/self.total) * entropy[i])
        return entropy

    def reEvalEntropy(self,n,p):
        entropy = []
        self.gain = []
        tPos = 0
        tNeg = 0
        for i in range(len(self.nodes)):
            positive = self.nodes[str(i)][1]
            for j in range(len(positive)):
                tPos += positive[j].weight
            negative = self.nodes[str(i)][-1]
            for j in range(len(negative)):
                tNeg += negative[j].weight
        for i in range(len(self.nodes)):
            pos = 0
            neg = 0
            positive = self.nodes[str(i)][1]
            for j in range(len(positive)):
                pos += positive[j].weight
            negative = self.nodes[str(i)][-1]
            for j in range(len(negative)):
                neg += negative[j].weight
            total = len(positive) + len(negative)
            entropy.append((p/n * -pos/tPos * m.log(p/n * pos/tPos,2) - p/n * neg/tNeg * m.log(p/n * neg/tNeg,2)))
            self.gain.append((total/self.total) * entropy[i])
        self.entropy = entropy
        #[sum(entropy)/len(entropy)]
