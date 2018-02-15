from kinet import *


def setupFixtures(pds,numFix):
    for fix in xrange(numFix):
        fixA = FixtureRGB(0)
        pds.append(fixA)

def setup(numFix):
    pds = PowerSupply("10.0.0.2")
    setupFixtures(pds, numFix)
    return pds


def rainbow_cycle(pds, pause=5, steps=1000):
    div = steps/len(pds)
    for step in range(steps):
        ratio = 0
        for idx, fixture in enumerate(pds):
            ratio += (step + idx * div) % steps / float(steps)
            fixture.hsv = (ratio, 1.0, 1.0)
        print pds
        pds.go()
        time.sleep(pause)


if __name__ == '__main__':
    pds = setup(1)
    print(pds.host)
    print(pds.socket)
    rainbow_cycle(pds)
    rainbow_cycle(pds)
    rainbow_cycle(pds)
    rainbow_cycle(pds)
    rainbow_cycle(pds)
    #pds = PowerSupply("10.071.139.175")
    #pds.append(FixtureRGB(3))
    #pds[0].rgb = (255,0,0)
    #pds.go()
