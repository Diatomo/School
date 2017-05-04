##
##HOMEWORK # 1
##
## NAME = CHARLES STEVENSON
## DATE = AUGUST 25, 2016
## CLASS = Artificial Intelligence TR 8 - 9:20
##
##
## Description:
##   This is the first homework assignment
##   where I read a file into a priority queue
##   and then outputed to the console by sorting
##   the integers using the priority queue
##
##

from Queue import PriorityQueue

def readLines(f, q):
    #Extract name
    name = f.readline()
    name = name[:-1]#get rid of /n character
    for line in f:
        num = int (line[:-1])
        q.put(num)#put number into priority queue
    return name

def main():
    #get && open file
    fileName = "priority.txt"
    f = open(fileName, 'r+')
    #create queue
    q = PriorityQueue()
    #Load Queue
    name = readLines(f, q)
    #Output Queue && Name
    print("Hello " +  name + "!")
    while not q.empty():
        print(q.get())

#execute
main()
