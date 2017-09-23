import dicom,os,re,sys

rootDir = '..\\LIDC image set\\Originals\\LIDC'

while True:

    print('Enter LIDC Number : ')
    dirname = str(input())

    if dirname == '0':
        exit()

    dirname.replace('\\','\\\\')

    flag = True

    while flag:

        print('Enter SOP UID : ')
        key = input()

        def search(dirName):
            global key
            filelist = (os.listdir(dirName))
            for filename in filelist:
                if os.path.isdir(dirName+'/'+filename):
                    search(dirName+'/'+filename)
                else:
                    s = re.search(r'(0+)(\d+)\.dcm$',filename)
                    if s:
                        dfile = dicom.read_file(dirName+'/'+filename)
                        if dfile.SOPInstanceUID == key:
                            print(dfile.InstanceNumber)

        if key == '0':
            flag = False
        else:
            search(rootDir + dirname)
            print('Done')