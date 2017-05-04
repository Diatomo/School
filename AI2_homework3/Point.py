
'''
    Point Class

'''

'''
========================================
    Author : Charles C. Stevenson (Diatomo)
    Date : February 24, 2017
    Description:
        Point
            container for weights and examples
========================================
'''

class Point:

    def __init__(self, weight, example):
        self.weight = 1 / weight
        self.example = example
        self.cls = example[-1]
