


import random as r
import statistics
import numpy as np

def main():
    choices = ['bar','bell','orange','lemon','cherry']

    selection = [['bar','bar','bar'],
                 ['bell','bell','bell'],
                 ['orange','orange','orange'],
                 ['lemon','lemon','lemon'],
                 ['cherry','cherry','cherry']]
    rewards = [25,10,5,4,3]

    plays = []

    for i in range(10000):
        if (i != 0):
            plays.append(play)
        coins = 10
        play = 0
        while (coins > 0):
            coins -= 1
            results = []
            found = False
            for i in range(3):
                rand = r.randint(0,4)
                results.append(choices[rand])
            for i in range(len(selection)):
                if (not found and results == selection[i]):
                    found = True
                    coins += rewards[i]
            if (not found):
                if (results[0] == 'cherry' and results[1] == 'cherry' and results[2] == 'cherry'):
                    coins += 3
                elif (results[0] == 'cherry' and results[1] == 'cherry'):
                    coins += 2
                elif (results[0] == 'cherry'):
                    coins += 1
            play += 1
            #print("Play: " + str(play))
            #print("Results: " + str(results) + "Coins: " + str(coins))

    plays.sort()
    print(plays)
    print("MEDIAN: " + str(statistics.median(plays)))
    print("MEAN: " + str(np.mean(plays)))

main()
