
# coding: utf-8

# In[1]:

import dicom
import os
import logging
import timeit
import numpy as np
import re
import xml.etree.ElementTree as ET
from matplotlib import pyplot
from skimage import  measure
from scipy.ndimage import label, generate_binary_structure
if __name__ == '__main__':
    logging.basicConfig(filename='myLog.log', level=logging.DEBUG)
    logging.info('Started')
Path = 'D:/Lung/DataSets/'


# In[2]:

def saveLabelledData(DataSet , display = False,masked =False,plot =False , sliceno = 62,blobs = False):
    '''
     This function imports the Data from .Dcm files of input DataSet and saves it in .npy format
     @Input:
         DataSet    : The no of the LIDC DataSet to be processed
         display    : Boolean.if True displays analytical info
         plot , sliceno : if plot is True it plots the data in 'sliceno'
     @Output:
         Time : time taken to complete this operation
         number_of_objects : number_of_objects in data

    '''
    start = timeit.default_timer()
    if DataSet <= 0:
        raise ValueError("DataSet cant be negative")
    global Path
    #DataSetPath : the path of the Dataset which needs to be converted
    DataSetPath = Path + 'LIDC image set/Renamed/LIDC'+str(DataSet)+'/'

    #SavePath    : Path where labelled Data is supposed to be stored
    SavePath = Path + 'components/'+str(DataSet)+'/'

    #MaskedPath : path where masked input data is available
    MaskedPath = Path + 'compmask/'+str(DataSet)+'/'

    #Ensure Save Path exists
    if not os.path.exists(SavePath):
        os.makedirs(SavePath)

    if not os.path.exists(DataSetPath):
        raise ValueError("Original Files of DataSet "+str(DataSet)+" missing")

    if not os.path.exists(MaskedPath):
        raise ValueError("Masked Files of DataSet "+str(DataSet)+" missing run the MATLAB coded to generate it.")

    fileListDicom=[] #Empty list to store input .dcm filePaths
    length=len(os.listdir(DataSetPath))
    for i in range(1,length+1):
        fileListDicom.append(DataSetPath+str(i)+".dcm")

    #Read first .dcm image of a given dataSet(metadata)
    RefDs = dicom.read_file(fileListDicom[0])

    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(fileListDicom))

    # Load spacing values (in mm)
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))


    #Create an np array to store original dicom data
    ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
    # loop through all the DICOM files
    for filenameDCM in fileListDicom:
        # read the file
        ds = dicom.read_file(filenameDCM)
        # store the raw image data
        ArrayDicom[:, :, fileListDicom.index(filenameDCM)] = (ds.pixel_array).T

    logging.info('ArrayDicom Imported')
    if display:
        print("ConstPixelDims:" + str(ConstPixelDims))
        print("ConstPixelSpacing:" + str(ConstPixelSpacing))
        #print(fileListDicom)

    #np array to store Masked data
    fileListMasked=[]

    length=len(os.listdir(MaskedPath))
    for i in range(1,length+1):
        fileListMasked.append(MaskedPath+str(i)+".dcm")
    if display:
        print(length)
        #print(fileListMasked)
    ArrayDicomMasked = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
    # loop through all the DICOM files
    for filenameDCM in fileListMasked:
        # read the file
        ds = dicom.read_file(filenameDCM)
        # store the raw image data
        ArrayDicomMasked[:, :, fileListMasked.index(filenameDCM)] = (ds.pixel_array).T
    logging.info('ArrayDicomMasked Imported')
    if masked:
        return ArrayDicomMasked
    if display:
        print("Max and Min of ArrayDicomMasked",np.max(ArrayDicomMasked),np.min(ArrayDicomMasked))
        print("Max and Min of ArrayDicom",np.max(ArrayDicom),np.min(ArrayDicom))

    #for i in range(0,ConstPixelDims[0]):
     #   for j in range(0,ConstPixelDims[1]):
      #          for k in range(0,ConstPixelDims[2]):
       #             if(ArrayDicomMasked[i,j,k] != 0):
        #                ArrayDicomMasked[i,j,k] = 1
    ArrayDicomMasked = ArrayDicomMasked > 0
    ArrayDicomMasked = ArrayDicomMasked.astype(int)
    #or ArrayDicom[ArrayDicom == -2000] = 0
    ArrayDicomNew = np.multiply(ArrayDicomMasked , ArrayDicom)
    if display:
        print("Max and Min of ArrayDicomMasked after 0/1:",np.max(ArrayDicomMasked),np.min(ArrayDicomMasked),np.sum(ArrayDicomMasked))
        print("Max and Min of ArrayDicomNew",np.max(ArrayDicomNew),np.min(ArrayDicomNew))

    #Labelling
    blobs_labels , number_of_objects = label(ArrayDicomNew, structure=generate_binary_structure(3,3))
    logging.info('Labelling Done.')
    if display:
        print("No of Objects:",number_of_objects)
    if blobs:
        return blobs_labels , number_of_objects



    if plot:
        if sliceno < ConstPixelDims[2] or sliceno < 0:
            raise ValueError("sliceno not in range [0:"+str(ConstPixelDims[2])+"]")
        x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
        y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
        #for i in range(1,ConstPixelDims[2]):
        pyplot.figure(dpi=500)
        pyplot.axes().set_aspect('equal', 'datalim')
        pyplot.set_cmap(pyplot.gray())
        pyplot.pcolormesh(x, y, np.flipud(ArrayDicomNew[:,:, sliceno]))
        pyplot.rcParams["figure.figsize"] = (4,4)
        pyplot.show()

    #Saving Data To file
    if not os.path.exists(SavePath + "Labelled.npy"):
        np.save(SavePath + "Labelled", blobs_labels)
    elif display:
        print("Labelled.npy Exist")
    logging.info('blobs_labels saved')

    if not os.path.exists(SavePath + "Intensity.npy"):
        np.save(SavePath + "Intensity", ArrayDicomNew)
    elif display:
        print("Intensity.npy Exist")
    logging.info('ArrayDicomNew saved')

    #save coordinates per component
    CoordinateExternal = [] #ListOfList
    for i in range(0,number_of_objects):
        Coordinate = []
        CoordinateExternal.append(Coordinate)

    def saveCord(flag = True):
        for i in range(0,number_of_objects):
            if   os.path.exists(SavePath + str(i+1) +".npy"):
                return False
        return True
    if saveCord():
        for z in range(0,ConstPixelDims[2]):
            for x in range(0,ConstPixelDims[0]):
                for y in range(0,ConstPixelDims[1]):
                    if(blobs_labels[x][y][z]!=0):
                        CoordinateExternal[blobs_labels[x][y][z] -1].append([x,y,z])
        for i in range(0,number_of_objects):
            if not os.path.exists(SavePath + str(i+1) +".npy"):
                coordinateArray = np.array(CoordinateExternal[i])
                np.save(SavePath + str(i+1),coordinateArray)
    logging.info('coordinatesof components saved')


    end = timeit.default_timer()

    return number_of_objects , end



# In[3]:

def getSOP(dirName, sliceNo):
    filelist = (os.listdir(dirName))
    for filename in filelist:
        if os.path.isdir(dirName+'/'+filename):
            sop = getSOP(dirName+'/'+filename, sliceNo)
            if sop is not None:
                return sop
        else:
            s = re.search(r'(0+)(\d+)\.dcm$', filename)
            if s:
                dfile = dicom.read_file(dirName+'/'+filename)
                if dfile.InstanceNumber == sliceNo:
                    return dfile.SOPInstanceUID


def getNoduleData(LIDCNo, startSlice, x, y):
    global Path
    d = {}
    xmlns="{http://www.nih.gov}"
    sliceSOP = getSOP(Path+'LIDC image set/Originals/LIDC' + str(LIDCNo),startSlice)
    tree = ET.parse(Path+'LIDC image set/XML/LIDC' + str(LIDCNo) + '.xml')
    for readingSession in [child for child in tree.getroot() if child.tag == (xmlns + 'readingSession')]:
        for unblindedReadNodule in [child for child in readingSession if child.tag == (xmlns + 'unblindedReadNodule')]:
            #print(unblindedReadNodule)
            for roi in [child for child in unblindedReadNodule if child.tag == (xmlns + 'roi')]:
                found = [element for element in roi if element.text == sliceSOP]
                if len(found) > 0:
                    for edgemap in [child for child in roi if child.tag == (xmlns + 'edgeMap')]:
                        if edgemap.find(xmlns + 'xCoord').text == str(x) and edgemap.find(xmlns + 'yCoord').text == str(y):
                            characteristics = unblindedReadNodule.find(xmlns + 'characteristics')
                            print(unblindedReadNodule.find(xmlns + 'noduleID').text)
                            for characteristic in characteristics:
                                d[characteristic.tag.replace(xmlns, '')] = characteristic.text
                            d['nodule'] = True
                            return d
    d['nodule'] = False
    return d


# In[4]:

def findEdgePixels(DataSet,Component,display =False):
    '''
    @params:
    Dataset : int The no of the LIDC DataSet to be processed
    Component: Component no to which edge pixels has to be found (0-number_of_objects)
    @Output: np Array of the edge pixals
    '''
    if DataSet <= 0:
        raise ValueError("DataSet cant be negative")
    global Path
    SaveFilePath = Path + 'components/'+str(DataSet)+'/'+'Labelled.npy'
    if not os.path.exists(SaveFilePath):
        saveLabelledData(DataSet = DataSet,display=display)
    blobs_labels = np.load(SaveFilePath)
    cord = getCoordinates(DataSet = DataSet,Component = Component)
    if display:
        print(type(cord),cord.shape)
    EdgePixels = []
    for i,j,k in cord:
        if blobs_labels[i+1,j,k] != Component or blobs_labels[i-1,j,k] != Component or         blobs_labels[i,j+1,k] != Component or blobs_labels[i,j-1,k] != Component:
            EdgePixels.append([i,j,k])

    return np.array(EdgePixels)





# In[5]:

def getCoordinates(DataSet,Component,display =False):
    '''
    @params:
    Dataset : int The no of the LIDC DataSet to be processed
    Component: Component no to which edge pixels has to be found (0-number_of_objects)
    @Output: np Array of the edge pixals
    '''
    if DataSet <= 0:
        raise ValueError("DataSet cant be negative")
    global Path
    SavePath = Path + 'components/'+str(DataSet)+'/'+str(Component)
    if not os.path.exists(SavePath+".npy"):
        saveLabelledData(DataSet = DataSet,display=display)
    cord = np.load(SavePath+".npy")
    if display:
        print(type(cord),cord.shape)

    return np.array(cord)


# In[6]:

def extractIndividualBoxes(DataSet,Report = False):
    '''
    Dataset : int The no of the LIDC DataSet to be processed
    Report:   if True prints various parameters for Debugging
    @Output: Time taken to run this function

    This function acesses the Data after labelling and maps the components generated to to the truth values
    from the XML files of the LIDC image set.

    '''
    start = timeit.default_timer()
    if DataSet <= 0:
        raise ValueError("DataSet cant be negative")
    global Path
    SaveFilePath = Path + 'components/'+str(DataSet)+'/'+'Labelled.npy'
    if not os.path.exists(SaveFilePath):
        saveLabelledData(DataSet = DataSet,display=Report)

    blobs_labels = np.load(SaveFilePath)
    number_of_objects = np.max(blobs_labels)
    Path = 'D:/Lung/DataSets/'
    SavePath = Path + 'ProcessedInput/'
    #Ensure Save Path exists
    if not os.path.exists(SavePath):
        os.makedirs(SavePath)
    f= open(SavePath+str("Annotation")+"characteristic.txt","r+")
    Annotation = f.read().split('\n')
    out = f= open(SavePath+str(DataSet)+"characteristic.txt","w+")
    out2D = f= open(SavePath+"characteristic2D.txt","a+")

    Annotation = np.array(Annotation)

    for ObjectNo in range(1,number_of_objects+1):
        if Report:
            print(ObjectNo)
        EdgePixels = findEdgePixels(DataSet = DataSet,Component = ObjectNo)
        AllPixels = getCoordinates(DataSet = DataSet,Component =ObjectNo)
        Xmin,Ymin,Zmin = Min = np.min(AllPixels,axis = 0 )
        Xmax,Ymax,Zmax = Max = np.max(AllPixels,axis = 0 )
        if Report:
            print("Min = "+str(Min)+"\nMax="+str(Max))
        noduleFlag = False
        for i,j,k in EdgePixels:
            characteristic = getNoduleData(DataSet,k,i,j)
            #print(characteristic)
            if  characteristic["nodule"]:
                characteristic["nodule"] = 1
                noduleFlag = True
                if Report:
                    print("malignancy",characteristic["malignancy"])
                out.write(str(DataSet)+" "+str(ObjectNo)+" "+str(Xmin)+" "+str(Ymin)+" "+str(Zmin)+" "+str(Xmax)+" "+str(Ymax)+" "+str(Zmax)+" ")
                out2D.write(str(DataSet)+" "+str(Xmin)+" "+str(Ymin)+" "+str(Zmin)+" "+str(Xmax)+" "+str(Ymax)+" "+str(Zmax)+" ")
                malignancy = 'M' if int(characteristic["malignancy"]) > 3 else 'B'
                out2D.write(str(malignancy)+"\n")
                for Property in Annotation:
                    if Report:
                        print(Property,characteristic[Property])
                    out.write(str(characteristic[Property])+" ")
                out.write("\n")
                break
        if not noduleFlag:
            characteristic["nodule"] = 0
            out2D.write(str(DataSet)+" "+str(Xmin)+" "+str(Ymin)+" "+str(Zmin)+" "+str(Xmax)+" "+str(Ymax)+" "+str(Zmax)+" ")
            out.write(str(DataSet)+" "+str(ObjectNo)+" "+str(Xmin)+" "+str(Ymin)+" "+str(Zmin)+" "+str(Xmax)+" "+str(Ymax)+" "+str(Zmax)+" ")
            for count in range(0,10):
                out.write("0 ")
            out.write("\n")
            out2D.write("N\n")
    end = timeit.default_timer()
    out.close()
    out2D.close()
    return end


# In[9]:

for DataSet in range(1,60):
    extractIndividualBoxes(DataSet)
