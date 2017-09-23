import os,re,shutil

searchdir = '../Data Set - Others/W0001/DICOMDIR'
newdir = '../Data Set - Others/W1Renamed'
os.mkdir(newdir)

listdir = os.listdir(searchdir)

for file in listdir:
    match = re.search(r'(\d+)\.dcm$', file)
    if match:
        num = match.group(1)
        print(match.group(0), match.group(1))
        shutil.copy(searchdir + '/' + file, newdir + '/' + str(num) + '.dcm')
