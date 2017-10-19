def FeatureExtractionMainFunction(blobs_labels,number_of_objects,ArrayDicom):
    #y = [[[] for i in range(n)] for i in range(n)]
    IntensityListExternal = []
    CoordinateExternal = []
    for i in range(0,number_of_objects):
        IntensityList = []
        Coordinate = []
        IntensityListExternal.append(IntensityList)
        CoordinateExternal.append(Coordinate)
    for x in range(0,ArrayDicom.shape[0]):
        for y in range(0,ArrayDicom.shape[1]):
            for z in range(0,ArrayDicom.shape[2]):
                if(blobs_labels[x][y][z]!=0):
                    IntensityListExternal[blobs_labels[x][y][z] -1].append(ArrayDicom[x][y][z])
                    CoordinateExternal[blobs_labels[x][y][z] -1].append([x,y,z])
   # print(CoordinateExternal[0]
    
    RawDictionary = {}
    RawDictionary["NoOfObjects"]=number_of_objects
    for i in range(0,number_of_objects):
        RawDictionary["Intensity"+str(i+1)] = IntensityListExternal[i]
        RawDictionary["Coordinate"+str(i+1)] = CoordinateExternal[i]
    #print(RawDictionary["Coordinate1"])
    return RawDictionary