# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:27:15 2018

@author: Koushal
"""
import dicom
import os
import numpy as np
import timeit
from scipy.ndimage import label, generate_binary_structure
start = timeit.default_timer()
dataset = 1
def saveNodules(DataSet=12):
    #Setting the path of imagesets.
    dataSet=DataSet
    path='../../DataSets/LIDC image set/Renamed/LIDC'+str(dataSet)+'/'
    fileListDicom=[]
    #Get all the .dcm files from a given image set directory.
    length=len(os.listdir(path))
    for i in range(1,length+1):
        fileListDicom.append(path+str(i)+".dcm")
    #Read first .dcm image of a given dataSet(metadata)
    RefDs = dicom.read_file(fileListDicom[0])
    
    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(fileListDicom))
    
    # Load spacing values (in mm)
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
    
   

    
    return ConstPixelDims , ConstPixelSpacing
d = {}
s = {}
for dataset in range(1,60):
    print(dataset)
    end = timeit.default_timer()

    print("TIME = ",(end-start))

    dims , space = saveNodules(dataset)
    try:
        d[str(dims)] = d[str(dims)] + 1
    except:
        d[str(dims)] = 1
    try:
        s[str(space)] = d[str(space)] + 1
    except:
        s[str(space)] = 1
print(d)
print(s)
end = timeit.default_timer()

print("TIME = ",(end-start))
