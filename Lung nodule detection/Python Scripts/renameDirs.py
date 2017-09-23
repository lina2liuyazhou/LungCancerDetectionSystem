import shutil, os
import re

dirname = '../LIDC image set/Originals'
List = os.listdir(dirname)

for directory in List:
    s = re.search(r'0*(\d+)',directory)
    os.rename('../LIDC image set/Originals/' + directory, '../LIDC image set/Originals/LIDC' + s.group(1))