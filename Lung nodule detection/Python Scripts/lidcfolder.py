import shutil, os, re, dicom

lidcdir = '../LIDC image set/Originals'
renamedir = '../LIDC image set/Renamed'
xmldir = '../LIDC image set/XML'

listdir = os.listdir(lidcdir)

for directory in listdir:
    s = re.search(r'0*(\d+)$',directory)
    dirname = 'LIDC' + s.group(1)
    #print(dirname, directory)

    currentdir = lidcdir + '/' + directory

    l = os.listdir(currentdir)
    if l.__len__() < 10:
        d1 = l[0]
        d2 = os.listdir(currentdir + '/' + d1)
        d2 = d2[0]
        if os.listdir(currentdir + '/' + d1 + '/' + d2).__len__() > 10:
            currentdir = currentdir + '/' + d1 + '/' + d2
        else:
            d1 = l[1]
            d2 = os.listdir(currentdir + '/' + d1)
            d2 = d2[0]
            currentdir = currentdir + '/' + d1 + '/' + d2

    listoffiles = os.listdir(currentdir)

    try:
        os.mkdir(renamedir + '/' + dirname)
    except:
        pass
    for file in listoffiles:
        s = re.search(r'0*(\d+)\.dcm',file)
        if s:
            dfile = dicom.read_file(currentdir + '/' + file)
            inum = dfile.InstanceNumber
            shutil.copy(currentdir + '/' + file,renamedir + '/' + dirname + '/' + str(inum) + '.dcm')
        else:
            shutil.copy(currentdir + '/' + file,xmldir + '/' + dirname + '.xml')
