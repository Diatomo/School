from sys import argv

script, filename1, filename2 = argv
target = open(filename1, 'w')
for j in range(15):
    for i in range(1508):
        target.write("0.001,")
    target.write("0.001\n")
target.close()

target = open(filename2, 'w')
for j in range(15):
    for i in range(126):
        target.write("2,")
    target.write("2\n")
target.close()
