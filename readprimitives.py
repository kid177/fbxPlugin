# -*- coding:gbk -*-
import struct
import binsec
import dirHandle as dh
import os


temppath = 'temp'
DEBUG = False
def GetAllPrimitives(DirName):
    PrimitivesList = []
    pathlist = os.listdir(DirName)
    for path in pathlist:
        #print path
        path = os.path.join(DirName, path)
        if os.path.isfile(path) and path[-11:] != '.primitives':
            continue
        if os.path.isfile(path):
            PrimitivesList.append(path)
        else:
            PrimitivesList.extend(GetAllPrimitives(path))
    return PrimitivesList

def getIntByStr(bstr):
    op = bstr[0]
    bstr = bstr[1:]
    #positive
    if op == '0':
        return int(bstr, 2)
   
    #negative
    curPos = len(bstr) - 1

    while curPos > -1:
        if bstr[curPos] == '0':
            bstr = bstr[:curPos] + '1' + bstr[curPos + 1:]
        else:
            bstr = bstr[:curPos] + '0' + bstr[curPos + 1:]
            break
        curPos -= 1

    curPos = len(bstr) - 1

    while curPos > -1:
        if bstr[curPos] == '0':
            bstr = bstr[:curPos] + '1' + bstr[curPos + 1:]
        else:
            bstr = bstr[:curPos] + '0' + bstr[curPos + 1:]
        curPos -= 1
    return -int(bstr, 2)

def unpackIntToFloat(packed):

    strPacked = bin(packed)[2:]

    while len(strPacked) < 32:
        strPacked = '0' + strPacked
    
    z = getIntByStr(strPacked[:10])
    y = getIntByStr(strPacked[10:21])
    x = getIntByStr(strPacked[21:32])

    return (float(x) / 1023.0, float(y) / 1023.0, float(z) / 511.0)


def GetInfoFromPrimitives(filename):
    indexList = []
    vertexList = []
    vertexs = []
    index = []
    groupList = []
    indexFormat = ''

    dh.cleanDir(temppath)

    if os.path.isdir(temppath):
        os.rmdir(temppath)
    
    binsec.extract(filename, temppath)
    listItems = os.listdir(temppath)
    for listItem in listItems:
        if listItem.find('vertices') != -1:
            vertexList.append(listItem)
        elif listItem.find('indices') != -1:
            indexList.append(listItem)

    #read vertex information
    for vertex in vertexList:
        f = open(temppath + "\\" + vertex, 'rb')

        dataInfo = f.read(64 + 4)
        dataValue = struct.unpack('64s1i', dataInfo)
        vertexFormat = dataValue[0]
        vertexNumber = dataValue[1]
        
        vertexFormatEnd = ''
        
        for char in vertexFormat:
            if char >= 'a' and char <= 'z':
                vertexFormatEnd += char
            else:
                break
        
        for i in xrange(0, vertexNumber):
            vertexInfo = f.read(32)

            vertexValue = struct.unpack('3f1I2f1I1I', vertexInfo)
            vPos = (vertexValue[0], vertexValue[1], vertexValue[2])
            vUV = (vertexValue[4], vertexValue[5])
            vNormal = unpackIntToFloat(vertexValue[3])
            vT = unpackIntToFloat(vertexValue[6])
            vB = unpackIntToFloat(vertexValue[7])
            vertexs.append((vPos, vUV, vNormal, vT, vB))
        
        f.close()

    for indice in indexList:
        f = open(temppath + '\\' + indice, 'rb')
        indiceInfo = f.read(64 + 4 + 4)

        indiceValue = struct.unpack('64s2i', indiceInfo)
        indiceFormat = indiceValue[0]
        indiceNumber = indiceValue[1]
        groupNumber = indiceValue[2]
        for indicenumber in xrange(0, indiceNumber):
            DataInfo = f.read(2)
            DataValue = struct.unpack('H', DataInfo)[0]

            index.append(DataValue)
        
        for groupnumber in xrange(0, groupNumber):
            groupInfo = []
            for i in xrange(0, 4):
                groupData = f.read(4)
                groupValue = struct.unpack('i', groupData)[0]
                groupInfo.append(groupValue)
            groupList.append(groupInfo)

        f.close()

    if not DEBUG:
        dh.cleanDir(temppath)
        if os.path.isdir(temppath):
            os.rmdir(temppath)

    return (vertexs, index, groupList, vertexFormat, vertexFormatEnd, indexFormat)


if __name__ == '__main__':
    print len(GetAllPrimitives('scene'))
    #print GetInfoFromPrimitives(GetAllPrimitives()[0])[0] 
