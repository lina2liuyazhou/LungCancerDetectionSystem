import os

rootDir = '..\\LIDC image set\\Renamed\\LIDC'
x = [ ]

for i in range(1,58):
    curDir = rootDir + str(i)
    x.append(os.listdir(curDir).__len__())
print(x)