# -*- coding: utf-8 -*-
import dicom
import os
import numpy as np
import timeit
from scipy.ndimage import label, generate_binary_structure
start = timeit.default_timer()
if __name__ == "__saveNodules__":
    #Do nothing
    a = 5
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
    
    
    # The array is sized based on 'ConstPixelDims'
    ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
   
    # loop through all the DICOM files
    for filenameDCM in fileListDicom:
        # read the file
        ds = dicom.read_file(filenameDCM)
        # store the raw image data
        ArrayDicom[:, :, fileListDicom.index(filenameDCM)] = ds.pixel_array
    
    path='../../DataSets/compmask/'+str(dataSet)+'/'
    fileListMasked=[]
    
    length=len(os.listdir(path))
    for i in range(1,length+1):
        fileListMasked.append(path+str(i)+".dcm")            
                
    ArrayDicomMasked = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
   # loop through all the DICOM files
    for filenameDCM in fileListMasked:
       # read the file
       ds = dicom.read_file(filenameDCM)
       # store the raw image data
       ArrayDicomMasked[:, :, fileListMasked.index(filenameDCM)] = ds.pixel_array
   # use print(ArrayDicom.shape) to get the dimentions of the 3d np array.
   
    for i in range(0,ConstPixelDims[0]):
        for j in range(0,ConstPixelDims[1]):
                for k in range(0,ConstPixelDims[2]):
                    if(ArrayDicomMasked[i,j,k] != 0):
                        ArrayDicomMasked[i,j,k] = 1
    
   
   
    temp=ArrayDicom
    #print(np.max(ArrayDicomMasked))
    #print(np.max(ArrayDicom))
    ArrayDicom = np.multiply(ArrayDicomMasked , ArrayDicom)
   #Labelling.
   # using structure=generate_binary_structure(3,3) to consider diagonal elements as linked.
    blobs_labels , number_of_objects = label(ArrayDicom, structure=generate_binary_structure(3,3))
   #print(blobs)
    print("No Of Objects:",number_of_objects) # no of objects
    print(temp.min())
    print(temp.max())
    print(ArrayDicom.shape)
   #print(blobs_labels.shape) To assert
   #Testing lables
  #create files
    
    for fileIndex in range(1,number_of_objects+1):
        count = 0
        f=open("..\\..\\DataSets\\components\\"+str(dataSet) + str(fileIndex) + ".txt" , "w+")
        log=open("..\\..\\DataSets\\components\\"+str(dataSet) + str(fileIndex) + "Log.txt" , "w+")
        f.write(str(ConstPixelDims[0])+" "+str(ConstPixelDims[1])+" "+str(ConstPixelDims[2])+"\n")
        f.write(str(ConstPixelSpacing[0])+" "+str(ConstPixelSpacing[1])+" "+str(ConstPixelSpacing[2])+"\n")
        for k in range(0,ConstPixelDims[2]):
            def inFrame(flag = True):
                for i in range(0,ConstPixelDims[0]):
                    for j in range(0,ConstPixelDims[1]):
                        if blobs_labels[i][j][k] == fileIndex:
                            flag = False
                            return flag
            flag = inFrame()
                            
            if flag == False :
                count = count + 1
                print(fileIndex,k)
                for i in range(0,ConstPixelDims[0]):
                    for j in range(0,ConstPixelDims[1]):
                        if blobs_labels[i][j][k] == fileIndex:
                            log.write(str(i)+" "+str(j)+" "+str(k)+"\n")
                            f.write(str(temp[i][j][k]) + " ")
                        else:
                            f.write("0 ")
                    f.write("\n")
        print(count)
    f.close()
                        
    return blobs_labels,number_of_objects
#saveNodules()
end = timeit.default_timer()

print("TIME = ",(end-start))