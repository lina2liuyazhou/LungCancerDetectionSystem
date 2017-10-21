from importDCM import importDCM
import FeatureExtractionMain as Fmain
import numpy as np
blobs_labels,number_of_objects,ArrayDicom = importDCM(60)
RawDictionary=Fmain.FeatureExtractionMainFunction(blobs_labels,number_of_objects,ArrayDicom)


def Area(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: area[]  --> A list of areas of all the objects of a particular dataset.
    '''
    n=RawDictionary["NoOfObjects"]
    area = []
    for i in range(1,n+1):
        area.append(len(RawDictionary["Intensity"+str(i)]))
    return area

'''
def perimeter(RawDictionary,ArrayDicom):
    n=RawDictionary["NoOfObjects"]
    for i in range(1,n+1):
        count = 0
        coordinates = RawDictionary["Coordinate"+str(i)]
        for pixel in coordinates:
            x=pixel[0]
            y=pixel[1]
            z=pixel[2]
            if ArrayDicom[x][y][z]!=1 && ArrayDicom[x][y][z]!=1 && ArrayDicom[x][y][z]!=1 && ArrayDicom[x][y][z]!=1:
                print(x,y,z)

'''
def MeanIntensity(RawDictionary):
    '''
    input: RawDictionary --> A dictionary storing required values for calculating area of a particular dataset.
    
    output: area[]  --> A list of mean intensity values of all the objects of a particular dataset.
    
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
    
    output: area[]  --> A list of difference between maximum and minimum intensity values of
                        all the objects of a particular dataset.
    
    MaxMinDiff = maximum intensity - minimum intensity
    '''
    n=RawDictionary["NoOfObjects"]
    MaxMinDiff = []
    for i in range(1,n+1):
        intensityI=RawDictionary["Intensity"+str(i)]
        MaxMinDiff.append(max(intensityI) - min(intensityI))
    return MaxMinDiff


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    