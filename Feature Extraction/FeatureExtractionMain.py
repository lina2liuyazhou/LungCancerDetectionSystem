def FeatureExtractionMainFunction(blobs_labels,number_of_objects,ArrayDicom):
    #y = [[[] for i in range(n)] for i in range(n)]
    IntensityListExternal = []   #Setting intensity lists
    CoordinateExternal = []      #Setting Cordinates list
    '''
        IntensityListExternal[] : List which has Lists as elements and each list within in has the 
                                  intensity values of i'th object.
        CoordinateExternal[] : List which has Lists as elements and each list within in has the 
                                  Coordinates [x,y,z] of i'th object.                          
    '''
    #initializing intensity and cordinate lists(External) with Lists(List os Lists)
    for i in range(0,number_of_objects):
        IntensityList = []
        Coordinate = []
        IntensityListExternal.append(IntensityList)
        CoordinateExternal.append(Coordinate)
        
        
    '''
    Adding Coordinates and Intensities from original ArrayDicom Array into Respective objects.
    '''
    for x in range(0,ArrayDicom.shape[0]):
        for y in range(0,ArrayDicom.shape[1]):
            for z in range(0,ArrayDicom.shape[2]):
                if(blobs_labels[x][y][z]!=0):
                    IntensityListExternal[blobs_labels[x][y][z] -1].append(ArrayDicom[x][y][z])
                    CoordinateExternal[blobs_labels[x][y][z] -1].append([x,y,z])
   # print(CoordinateExternal[0]
    '''Following is the discription of 'RawDictionary' Dictionary.
        it contains following elements:
            1. NoOfObjects : It stores number of objects present in that dataset.
            2. Intensity1 , Intensity2 , . . . . IntensityN :
                Intensity1 : Intensity values of all pixels belonging to object1
                and so on....
            3. Coordinates1 , Coordinates2 , . . . . CoordinatesN :
                    Coordinates1 : Coordinate values of all pixels belonging to object1:
                               Coordinates1[i] : it has an array of x,y,z Coordinates of pixel i of object 1
                               i.e., [x,y,z]
                and so on....
    '''
    RawDictionary = {}
    RawDictionary["NoOfObjects"]=number_of_objects
    for i in range(0,number_of_objects):
        RawDictionary["Intensity"+str(i+1)] = IntensityListExternal[i]
        RawDictionary["Coordinate"+str(i+1)] = CoordinateExternal[i]
    #print(RawDictionary["Coordinate1"])
    
    '''
    Usage of RawDictionary:
        RawDictionary["NoOfObjects"] : for NoOfObjects
        RawDictionary["Intensity1"]  : Array of Intensities of object1
        RawDictionary["Coordinate1"] " Array of Coordinates of object1
        RawDictionary["Coordinate1"][i][0] : X coordinate of 1st pixel of object i
    '''
    return RawDictionary