import dicom
import os
import numpy as np
from matplotlib import pyplot
import skimage
from skimage import data , io , color, exposure , filters , measure,morphology
from skimage.feature import hog
from scipy import ndimage
from scipy.ndimage import label, generate_binary_structure
from skimage.segmentation import relabel_sequential
#Setting the path of imagesets.
dataSet=27
path='../../DataSets/LIDC image set/Renamed/LIDC'+str(dataSet)+'/'
fileListDicom=[]

#Get all the .dcm files from a given image set directory.
for dirName, subdirList, fileList in os.walk(path):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            fileListDicom.append(os.path.join(dirName,filename))
#Read first .dcm image of a given dataSet(metadata)
RefDs = dicom.read_file(fileListDicom[0])

# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(fileListDicom))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))


#np.arange() function to build a vector containing an arithmetic progression such as [0.0 0.1 0.2 0.3]
#np.(start,stop,step)
x = np.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = np.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = np.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])

# The array is sized based on 'ConstPixelDims'
ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in fileListDicom:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, fileListDicom.index(filenameDCM)] = ds.pixel_array
# use print(ArrayDicom.shape) to get the dimentions of the 3d np array.



#import componentMask to np array.
path='../../DataSets/compmask/'+str(dataSet)+'/'
fileListMasked=[]

#Get all the .dcm files from a given image set directory.
for dirName, subdirList, fileList in os.walk(path):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            fileListMasked.append(os.path.join(dirName,filename))
ArrayDicomMasked = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in fileListMasked:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicomMasked[:, :, fileListMasked.index(filenameDCM)] = ds.pixel_array
# use print(ArrayDicom.shape) to get the dimentions of the 3d np array.
ArrayDicom = np.multiply(ArrayDicomMasked , ArrayDicom)
'''# USE this to test if it is ready for Labelling.
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, np.flipud(ArrayDicomMasked[:, :, 80]))
pyplot.show()'''

'''#use this to get individual slices
im=ArrayDicomMasked
im, number_of_objects = ndimage.label(im)
blobs = ndimage.find_objects(im)
all_labels ,  = measure.label(ArrayDicomMasked)'''


#Labelling.
# using structure=generate_binary_structure(3,3) to consider diagonal elements as linked.
blobs_labels , number_of_objects = label(ArrayDicom, structure=generate_binary_structure(3,3))
#print(blobs)
print(number_of_objects) # no of objects
#print(blobs_labels.shape) To assert
#Testing lables
'''
for xc in range(0,512):
    for yc in range(0,512):
        if blobs_labels[xc,yc, 81] !=0:
            print(xc,yc,blobs_labels[xc, yc, 81])'''
            
#To display labelling in action.                    
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, np.flipud(blobs_labels[:,:, 81]))
pyplot.show()
    
    
properties = measure.regionprops(blobs_labels)
for prop in properties :
    print(prop.area)
    
    