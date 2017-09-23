import os
import re
import sys, dicom, shutil

renamedDir = ''

def changeName(dirName):

    global renamedDir,newdir

    l = (os.listdir(dirName))
    num = l.__len__()

    numbers = []
    numbers.clear()

    for fname in l:
        if os.path.isdir(dirName+'/'+fname):
            changeName(dirName+'/'+fname)
        else:
            if num < 10 :
                return
            s = re.search(r'(0+)(\d+)\.dcm$',fname)
            if s:
                dfile = dicom.read_file(dirName+ '/' + fname)
                inum = dfile.InstanceNumber
                #print(fname,inum)
                shutil.copy(dirName+ '/' + fname,renamedDir + '/' + str(inum) + '.dcm')
                numbers.append(int(inum))
    numbers.sort()
    x = 1
    for i in numbers:
        shutil.copy(renamedDir + '/' + str(i) + '.dcm', newdir + '/' + str(x) +'.dcm')
        x = x +1


rootdir = "../LIDC image set/Originals"
filelist = os.listdir(rootdir)
for d in filelist:
    renamedDir = "../LIDC image set/RenamedTemp/" + d
    newdir = "../LIDC image set/Renamed/" + d

    try:
        os.mkdir(renamedDir)
    except:
        pass

    try:
        os.mkdir(newdir)
    except:
        pass

    searchdir = rootdir + '/' + d
    changeName(searchdir)

# renamedDir = "../LIDC image set/Renamed/LIDC5"
# newdir = "../LIDC image set/Renamed1/LIDC5"
# os.mkdir(renamedDir)
# os.mkdir(newdir)
# changeName('../LIDC image set/Originals/LIDC5')