from radiomics import featureextractor
p1 = '../../DataSets/nrrdfiles/01.nrrd'
p2 ='../../DataSets/nrrdfiles/02.nrrd'
extractor = featureextractor.RadiomicsFeaturesExtractor()
result = extractor.execute(p1,p2)
print("Result is ",result)