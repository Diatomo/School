

import math

def main():
    cse = 0.80
    ece = 0.20

    cCse = 0.75
    cEce = 0.50

    print((abs(cse * cCse - ece * cEce)))
    while (abs(cse * cCse - ece*cEce) >= 0.0001 ):
        print((abs(cse * cCse - ece * cEce)))
        ece += .01
        cse -= .01

    print("CSE = " + str(cse))
    print("ECE = " + str(ece))

main()
