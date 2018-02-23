import os, re, dicom
import xml.etree.ElementTree as ET


def getSOP(dirName, sliceNo):
    filelist = (os.listdir(dirName))
    for filename in filelist:
        if os.path.isdir(dirName+'/'+filename):
            return getSOP(dirName+'/'+filename, sliceNo)
        else:
            s = re.search(r'(0+)(\d+)\.dcm$', filename)
            if s:
                dfile = dicom.read_file(dirName+'/'+filename)
                if dfile.InstanceNumber == sliceNo:
                    return dfile.SOPInstanceUID


def getNoduleData(LIDCNo, startSlice, x, y):
    d = {}
    xmlns="{http://www.nih.gov}"
    sliceSOP = getSOP('..\\..\\DataSets\\LIDC image set\\Originals\\LIDC'+ str(LIDCNo),startSlice)
    tree = ET.parse('..\\..\\DataSets\\\\LIDC image set\\XML\\LIDC' + str(LIDCNo) + '.xml')
    for readingSession in [child for child in tree.getroot() if child.tag == (xmlns + 'readingSession')]:
        for unblindedReadNodule in [child for child in readingSession if child.tag == (xmlns + 'unblindedReadNodule')]:
            #print(unblindedReadNodule)
            for roi in [child for child in unblindedReadNodule if child.tag == (xmlns + 'roi')]:
                found = [element for element in roi if element.text == sliceSOP]
                if len(found) > 0:
                    for edgemap in [child for child in roi if child.tag == (xmlns + 'edgeMap')]:
                        if edgemap.find(xmlns + 'xCoord').text == str(x) and edgemap.find(xmlns + 'yCoord').text == str(y):
                            characteristics = unblindedReadNodule.find(xmlns + 'characteristics')
                            for characteristic in characteristics:
                                d[characteristic.tag.replace(xmlns, '')] = characteristic.text
                            d['nodule'] = True
                            return d
    d['nodule'] = False
    return d

print(getNoduleData(12,74,388,213))
print(getNoduleData(1,71,396,216))