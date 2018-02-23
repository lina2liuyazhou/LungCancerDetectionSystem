# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:10:38 2018

@author: Koushal
"""
#import os
import numpy as np
import timeit
from importDCM import importDCM
import FeatureExtractionMain as Fmain
from Parser import getLabel
import os.path
import createNodules
from createNodules import saveNodules
start = timeit.default_timer()
print(start)
dataSet = 12
blobs_labels,number_of_objects,ArrayDicom , details , properties = importDCM(12)
#RawDictionary=Fmain.FeatureExtractionMainFunction(blobs_labels,number_of_objects,ArrayDicom , details , properties)


ObjectNo = 10
log="..\\..\\DataSets\\components\\"+str(dataSet) + str(ObjectNo) + "Log.txt"

if  not os.path.exists(log):
    saveNodules(dataSet)
f=open("..\\..\\DataSets\\components\\"+str(dataSet) + str(ObjectNo) + ".txt" , "r")
log=open("..\\..\\DataSets\\components\\"+str(dataSet) + str(ObjectNo) + "Log.txt" , "r")
    
Coordinates = np.fromfile(log,dtype = int,sep = " ")
Coordinates = Coordinates.reshape(int(Coordinates.shape[0]/3),3)
print(Coordinates,Coordinates.shape)
x , y , z = Coordinates[1,:]
#print(dataSet, z, x, y)
#print(getLabel(dataSet, z, x, y))
#print(getLabel(13,74,388,213))
for i in range(0,512):
    for j in range(0,512):
        if blobs_labels[i][j][62] != 0:
            print(blobs_labels[i][j][62])
print(blobs_labels[	:,	: ,62])



end = timeit.default_timer()

print("TIME = ",(end-start))



    
    

