

'''
    STUMP TESTER

'''
#~~~M a G i C~~~#
'''
========================================
    Author : Charles C. Stevenson (Diatomo)
    Date : February 24, 2017
    Description:
        Stump Tester
            tests my stump classifier
========================================
'''
import Stump
import Point
import math

def keyWithMaxVal(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]

def initShrine(f,examples):
    shrine = []
    attributes = 0
    weight = sum(1 for line in f)
    f.seek(0)
    for line in f:
        line = line[:-1]
        line =line.split(',')
        examples.append(Point.Point(weight, line))
        attributes = (len(line) - 1)
    f.seek(0) #reset
    print(" ")
    print("Nodes")
    #initialize shrine (collection of stumps)
    for i in range(attributes):
        shrine.append(Stump.Stump(i, examples))
        f.seek(0)
    return shrine

def outShrine(shrine):
    for i in range(len(shrine)):
        print(" ")
        print("=====================================")
        print("Question : " + str(shrine[i].question))
        print("Entropy : " + str(shrine[i].entropy))
        print("Gain : " + str(shrine[i].gain))
        print("=====================================")

def bestQuestion(shrine):
    maximum = 100
    bestQuestion = 0
    for i in range(len(shrine)):
        if (min(shrine[i].entropy) < maximum):
            maximum = min(shrine[i].entropy)
            bestQuestion = i
    return bestQuestion

def test(shrine, bQ, examples):
    accuracy = 0.0
    total = 0.0
    bStump = shrine[bQ]
    for example in examples:
        prediction = predict(shrine, example, bQ)
        if (int(prediction) == int(example.example[-1])):
            accuracy += 1.0
        total += 1.0
    return accuracy / total * 100

def normalize(examples):
    maximum = 0
    avg = 0
    for i in range(len(examples)):
        avg += examples[i].weight
    for i in range(len(examples)):
        examples[i].weight = examples[i].weight/(avg)
        #print(examples[i].weight)
    print("SUMMATION OF NORMOD WEIGHTS : " + str(avg))

def predict(shrine, example, bQ):
    pre = 1
    n = 0
    p = 0
    neg = shrine[bQ].nodes[example.example[bQ]][-1]
    for i in range(len(neg)):
        n += neg[i].weight
    pos = shrine[bQ].nodes[example.example[bQ]][1]
    for i in range(len(pos)):
        p += pos[i].weight
    if (n > p):
        pre = -1
    #print(pre)
    return pre

def adaBoost(shrine,examples,k):
    hypothesis = []
    z = []
    for i in range(5):
        pos = []
        neg = []
        p = 0
        n = 0
        bQuestion = bestQuestion(shrine)
        hypothesis.append(shrine[bQuestion])
        error = 0.0
        example = 0
        for example in examples:
            prediction = predict(shrine, example, bQuestion)
            if (prediction != int(example.example[-1])):
                neg.append(example)
                error += example.weight
                n += example.weight
        for example in examples:
            prediction = predict(shrine, example, bQuestion)
            if (prediction == int(example.example[-1])):
                pos.append(example)
                p += example.weight
                example.weight = example.weight * error / (1.0 - error)
        normalize(examples)
        print("POSITIVE =  " + str(len(pos)) + " Negative = " + str(len(neg)))
        shrine[bQuestion].weight = math.log((1.0 - error) / (error))
        z.append(shrine[bQuestion].weight)
        for j in range(len(shrine)):
            shrine[j].reEvalEntropy(n, p)
        outShrine(shrine)
    return [hypothesis, z]

def createExamples(f):
    examples = []
    weight = sum(1 for line in f)
    f.seek(0)
    for line in f:
        line = line[:-1]
        line = line.split(',')
        examples.append(Point.Point(weight, line))
    return examples

def adaPredict(shrine, example):
    pre = 1
    n = 0
    p = 0
    neg = shrine.nodes[example.example[shrine.question]][-1]
    for i in range(len(neg)):
        n += neg[i].weight
    pos = shrine.nodes[example.example[shrine.question]][1]
    for i in range(len(pos)):
        p += pos[i].weight
    if (n > p):
        pre = -1
    return pre

def testAda(hypothesis, testExamples):
    accuracy = 0.0
    total = 0.0
    for example in testExamples:
        prediction = 0
        for i in range(len(hypothesis[0])):
            prediction += hypothesis[1][i] * adaPredict(hypothesis[0][i], example)
        if (prediction > 0):
            prediction = 1
        else:
            prediction = -1
        if (prediction == int(example.example[-1])):
            accuracy += 1
            total += 1
        else:
            total += 1
    return accuracy / total * 100


def main():
    f = open('game_codedata_train.dat')
    examples = []
    shrine = initShrine(f, examples)
    f.close()
    outShrine(shrine)

    f = open('game_codedata_test.dat')
    bQuestion = bestQuestion(shrine)
    print("Best Question = " + str(bQuestion))
    testExamples = []
    testExamples = createExamples(f)
    f.close()
    accuracy = test(shrine, bQuestion, testExamples)
    f.close()
    k = 5
    hypothesis = adaBoost(shrine, examples, k)
    print("ACCURACY On Best Stump : " + str(accuracy))
    accuracy = testAda(hypothesis, testExamples)
    print("WEIGHTS = " + str(hypothesis[1]))
    print("Ada boost accuracy = " + str(accuracy))
    for i in range(len(shrine)):
        print("SHRINE WEIGHTS : " + str(shrine[i].weight))

main()
