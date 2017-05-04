



import random
def randomNumber(unit):
    return random.randint(0,unit)

def loop(h,w,p,z,itr,fileName):
    f = open(fileName, 'w')
    f.write("DIMENSIONS " + str(h) + " " + str(w) + "\n")
    f.write("ITERATIONS " + str(itr) + "\n")
    for j in range(h):
        for i in range(w):
            if (j == 0 or j == h-1):
                if (i == 0 or i == w-1):
                    f.write('+')
                else:
                    f.write('-')
            else:
                if (i == 0 or i == w-1):
                    f.write("|")
                elif (randomNumber(p) == 0):
                    f.write('p')
                elif (randomNumber(z) == 0):
                    f.write('z')
                else:
                    f.write(" ")
        f.write("\n")

    f.close()


def main():

    h = input("Height: ")
    w = input("Width: ")
    p = input("frequency of puppy (int) {0-inf}: ")
    z = input("frequency of zombie (int) {0-inf}: ")
    itr = input("iterations: ")
    fileName = raw_input("Name of File: ")
    loop(h,w,p,z,itr,fileName)

main()
