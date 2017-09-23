import os,re,shutil

rootdir = '../Data Set - Others/LUNG PID LARGE'
newdir = '../Data Set - Others/PID Renamed'

listdir = os.listdir(rootdir)

for directory in listdir:
    os.mkdir( newdir + '/' + directory)
    currentdir = rootdir + '/' + directory
    listfiles = os.listdir(currentdir)
    numberlist = [ ]
    dicti = {}


    for file in listfiles:
        match = re.search(r'(\d+)\.(\d+)\.dcm$', file)
        if match:
            num1 = match.group(1)
            num2 = match.group(2)
            if num2.__len__() == 1:
                num2 = '0' + num2
            number = int(num1 + num2)
            numberlist.append(number)
            dicti[number] = file
            print(match.group(0), num1, num2, number)
            #shutil.copy(searchdir + '/' + file, newdir + '/' + str(num) + '.dcm')

    numberlist.sort()
    i = 1
    for n in numberlist:
        file = dicti.get(n)
        shutil.copy(currentdir + '/' + file, newdir + '/' + directory + '/' + str(i) + '.dcm')
        i = i + 1