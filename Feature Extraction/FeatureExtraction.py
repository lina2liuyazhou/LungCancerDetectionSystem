from importDCM import importDCM
import FeatureExtractionMain as Fmain
import numpy as np
import math
from numpy import mgrid, sum
from scipy.stats import kurtosis, skew
import timeit
from radiomics import featureextractor
start = timeit.default_timer()
print(start)
blobs_labels,number_of_objects,ArrayDicom , details , properties = importDCM(12)
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
        area.append(len(RawDictionary["Intensity"+str(i)]) * PixelSpacingX * PixelSpacingY * (SliceThickness/2.0))
    return area


def perimeter(RawDictionary,blobs_labels):
    n=RawDictionary["NoOfObjects"]
    PixelSpacingX = RawDictionary["PixelSpacingX"]
    SliceThickness = RawDictionary["SliceThickness"]
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
        per.append(count*SliceThickness)
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
     moments['mu30'] = sum((x-moments['mean_x'])**3*image) '''



def MomentOfInertia(RawDictionary):
    n=RawDictionary["NoOfObjects"]
    MOI = []
    PixelSpacingX = RawDictionary["PixelSpacingX"]
    SliceThickness = RawDictionary["SliceThickness"]
    PixelSpacingY = RawDictionary["PixelSpacingY"]
    Pixy = np.array([PixelSpacingX,PixelSpacingY,SliceThickness])
    centroid = np.array(Centroid(RawDictionary)) #It is correct
    for i in range(1,n+1):
        intensityI=np.array(RawDictionary["Intensity"+str(i)])
        coordinatesI = np.array(RawDictionary["Coordinate"+str(i)])
        sum = 0
        for j in range(1,coordinatesI.shape[0]):
            distance = np.sum(np.square(np.multiply(np.absolute(coordinatesI[j-1] - centroid[i-1]),Pixy)))
            print(distance) 
            sum = sum + distance * intensityI[j - 1]
        MOI.append(sum)
    return np.array(MOI)
        
        
    
    
def Centroid(RawDictionary):
    Properties = RawDictionary["Properties"]
    centroid = []
    for prop in Properties:
        centroid.append(prop.centroid)
    return centroid
    



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
def sphericity(RawDictionary):
    vol=Area(RawDictionary)
    Sa = perimeter(RawDictionary,blobs_labels)
    spher=[]
    n=RawDictionary["NoOfObjects"]
    for i in range(1,n+1):
        spher.append(math.pow(math.pi,(1/3.0))*(math.pow(6*vol[i-1],2/3.0))/Sa[i-1])
        if(spher[i-1]>1):
            print(vol[i-1],Sa[i-1],i)
    return spher

def mu(p,q,r,RawDictionary,centroid):
    muu = []
    n = RawDictionary["NoOfObjects"]
    for j in range(1,n+1):
        coordinateI = RawDictionary["Coordinate"+str(j)]
        muval = 0
        for i in range(1,len(coordinateI)):
            muval = muval + (math.pow((coordinateI[i-1][0] - centroid[j-1][0]),p) * math.pow((coordinateI[i-1][1] - centroid[j-1][1]),q) * math.pow((coordinateI[i-1][2] - centroid[j-1][2]),r))
        muu.append(muval)
    return muu
    

def moment(RawDictionary):
    centroid = Centroid(RawDictionary)
    mu200 = np.array(mu(2,0,0,RawDictionary,centroid))
    mu020 = np.array(mu(0,2,0,RawDictionary,centroid))  
    mu002 = np.array(mu(0,0,2,RawDictionary,centroid))
    mu110 = np.array(mu(1,1,0,RawDictionary,centroid))
    mu101 = np.array(mu(1,0,1,RawDictionary,centroid))
    mu011 = np.array(mu(0,1,1,RawDictionary,centroid))
    J1 = np.add(mu200, np.add(mu020, mu002))
    J2a = np.add(np.multiply(mu200,mu020),np.add(np.multiply(mu200,mu002),np.multiply(mu020,mu002)))
    J2b = np.add(np.multiply(mu110,mu110),np.add(np.multiply(mu101,mu101),np.multiply(mu011,mu011)))
    J2 = np.subtract(J2a,J2b)
    J3a = np.add(np.multiply(mu200,np.multiply(mu020,mu002)),2*np.multiply(mu110,np.multiply(mu101,mu011)))
    J3b = np.add(np.multiply(mu002,np.multiply(mu110,mu110)),np.add(np.multiply(mu020,np.multiply(mu101,mu101)),np.multiply(mu200,np.multiply(mu011,mu011))))
    J3 = np.subtract(J3a,J3b)
    return np.log10(J1), np.log10(J2), np.log10(J3)

#print("Moment is ",moment(RawDictionary))
'''
n = RawDictionary["NoOfObjects"]
for i in range(1,n+1):
     coordinateI = RawDictionary["Coordinate"+str(i)]
     #for j in range(1,len(coordinateI)):
     print(coordinateI) '''

def perimeter2(RawDictionary,blobs_labels):
    n=RawDictionary["NoOfObjects"]
    PixelSpacingX = RawDictionary["PixelSpacingX"]
    SliceThickness = RawDictionary["SliceThickness"]
    PixelSpacingY = RawDictionary["PixelSpacingY"]
    per = []
    for i in range(1,n+1):
        countXY = 0
        countYZ = 0
        countZX = 0
        SurfaceAreaI = 0
        coordinates = RawDictionary["Coordinate"+str(i)]
        for pixel in coordinates:
            x=pixel[0]
            y=pixel[1]
            z=pixel[2]
            #if x==o or x== n:
        
            if blobs_labels[x+1][y][z]!=i or blobs_labels[x-1][y][z]!=i :
                count = count + PixelSpacingX
            if blobs_labels[x][y+1][z]!=i or blobs_labels[x][y-1][z]!=i :
                count = count + PixelSpacingY
        per.append(count*SliceThickness)
    return per

'''
for i in range(1,RawDictionary["NoOfObjects"]):
    print(max(RawDictionary["Intensity"+str(i)])) '''

print(Kurtosis(RawDictionary))
end = timeit.default_timer()

print("TIME = ",(end-start))