from importDCM import importDCM
import FeatureExtractionMain as Fmain
import numpy as np
import math
from numpy import mgrid, sum
from scipy.stats import kurtosis, skew
blobs_labels,number_of_objects,ArrayDicom , details , properties = importDCM(20)
RawDictionary=Fmain.FeatureExtractionMainFunction(blobs_labels,number_of_objects,ArrayDicom , details , properties)


def Area(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: area[]  --> A list of areas of all the objects of a particular dataset.
    '''
    n=RawDictionary["NoOfObjects"]
    PixelSpacingX = RawDictionary["PixelSpacingX"]
    PixelSpacingY = RawDictionary["PixelSpacingY"]
    SliceThickness = RawDictionary["SliceThickness"]
    area = []
    for i in range(1,n+1):
        area.append(len(RawDictionary["Intensity"+str(i)]) * PixelSpacingX * PixelSpacingY * SliceThickness)
    return area


def perimeter(RawDictionary,blobs_labels):
    n=RawDictionary["NoOfObjects"]
    PixelSpacingX = RawDictionary["PixelSpacingX"]
    PixelSpacingY = RawDictionary["PixelSpacingY"]
    per = []
    for i in range(1,n+1):
        count = 0
        coordinates = RawDictionary["Coordinate"+str(i)]
        for pixel in coordinates:
            x=pixel[0]
            y=pixel[1]
            z=pixel[2]
            if blobs_labels[x+1][y][z]!=i or blobs_labels[x-1][y][z]!=i :
                count = count + PixelSpacingX
            if blobs_labels[x][y+1][z]!=i or blobs_labels[x][y-1][z]!=i :
                count = count + PixelSpacingY
        per.append(count)
    return per


def MeanIntensity(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: Mean[]  --> A list of mean intensity values of all the objects of a particular dataset.
    
    mean= sum(all intensities) / (no of pixels)
    '''
    n=RawDictionary["NoOfObjects"]
    Mean = []
    for i in range(1,n+1):
        intensityI=RawDictionary["Intensity"+str(i)]
        Mean.append(np.mean(intensityI)) 
        
    return Mean
def MaxMinIntensityDifference(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: MaxMinDiff[]  --> A list of difference between maximum and minimum intensity values of
                        all the objects of a particular dataset.
    
    MaxMinDiff = maximum intensity - minimum intensity
    '''
    n=RawDictionary["NoOfObjects"]
    MaxMinDiff = []
    for i in range(1,n+1):
        intensityI=RawDictionary["Intensity"+str(i)]
        MaxMinDiff.append(max(intensityI) - min(intensityI))
    return MaxMinDiff

def Varience(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: Var[]  --> A list of Varience values of all the objects of a particular dataset.
    
    '''
    n=RawDictionary["NoOfObjects"]
    Var = []
    for i in range(1,n+1):
        intensityI=RawDictionary["Intensity"+str(i)]
        Var.append(np.var(intensityI))
    return Var

'''
def Moments(image):
     assert len(image.shape) == 2 # only for grayscale images        
     x, y = mgrid[:image.shape[0],:image.shape[1]]
     moments = {}
     moments['mean_x'] = sum(x*image)/sum(image)
     moments['mean_y'] = sum(y*image)/sum(image)
     # central moments
     # moments['mu01']= sum((y-moments['mean_y'])*image) # should be 0
     # moments['mu10']= sum((x-moments['mean_x'])*image) # should be 0
     moments['mu11'] = sum((x-moments['mean_x'])*(y-moments['mean_y'])*image)
     moments['mu02'] = sum((y-moments['mean_y'])**2*image) # variance
     moments['mu20'] = sum((x-moments['mean_x'])**2*image) # variance
     moments['mu12'] = sum((x-moments['mean_x'])*(y-moments['mean_y'])**2*image)
     moments['mu21'] = sum((x-moments['mean_x'])**2*(y-moments['mean_y'])*image) 
     moments['mu03'] = sum((y-moments['mean_y'])**3*image) 
     moments['mu30'] = sum((x-moments['mean_x'])**3*image) 
    '''

'''
def MomentOfInertia(RawDictionary):
    n=RawDictionary["NoOfObjects"]
    MOI = []
    centroid = np.array(Centroid(RawDictionary)) #It is correct
    for i in range(1,n+1):
        intensityI=RawDictionary["Intensity"+str(i)]
        coordinatesI = np.array(RawDictionary["Coordinate"+str(i)])
        distance = np.absolute(coordinatesI - centroid[i])
        print(distance)
        
        
    
    
    
def Centroid(RawDictionary):
    Properties = RawDictionary["Properties"]
    centroid = []
    EulerNo = []
    for prop in Properties:
        centroid.append(prop.centroid)
        #EulerNo.append(prop.perimeter  )
    return centroid
    

MomentOfInertia(RawDictionary)'''

def Skewness(RawDictionary):
    Skew = []
    n = RawDictionary["NoOfObjects"]
    for i in range(1,n+1): 
        intensityI=np.array(RawDictionary["Intensity"+str(i)])
        Skew.append(skew(intensityI))
    return Skew

def Kurtosis(RawDictionary):
    values = []
    n = RawDictionary["NoOfObjects"]
    for i in range(1,n+1): 
        intensityI=np.array(RawDictionary["Intensity"+str(i)])
        values.append(kurtosis(intensityI))
    return values
print(Kurtosis(RawDictionary))