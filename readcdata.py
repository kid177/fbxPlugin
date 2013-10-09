# -*- coding:gb18030 -*-
import xmlparse as xp
import os
import dirHandle as dh
import binsec
import rotate_height
import sys
reload(sys)
sys.setdefaultencoding('gb18030')
from xml.dom.minidom import parse, parseString, Document

mVertRows = 0
mVertCols = 0
heights = 0


mDX = 0
mDZ = 0

def GenTriGrid(numVertRows, numVertCols, dx, dz):

    verts = []
    indices = []
    numCellRows = numVertRows - 1
    numCellCols = numVertCols - 1
    for i in xrange(0, numVertRows):
        for j in xrange(0, numVertCols):
            height = heights[j * mVertRows + (numVertRows - i - 1)]
            vertex = (j * dx , height, i * dz )
            verts.append(vertex)

    for i in xrange(0, numCellRows):
        for j in xrange(0, numCellCols):
            indices.append(i * numVertCols + j)
            indices.append(i * numVertCols + j + 1)
            indices.append((i + 1) * numVertCols + j)

            indices.append((i + 1) * numVertCols + j)
            indices.append(i * numVertCols + j + 1)
            indices.append((i + 1) * numVertCols + j + 1)

    return verts, indices

def BuildGeometry(matrix):
    newPos = matrix[0][3]

    if mVertRows == 28:
        mDX, mDZ = 4, 4
    else:
        mDX, mDZ = 2, 2

    verts, indices = GenTriGrid(mVertRows, mVertCols, mDX, mDZ)
    vertexPoses = []
    vertexTcs = []
    vertexNormals = []
    indexs = []

    for vertex in verts:
        #pos
        temp = []
        for i in xrange(0, 3):
            temp.append(vertex[i] + newPos[i])
        vertexPoses.append(temp)
        #vt
        temp = []
        for i in xrange(0, 2):
            temp.append(0)
        vertexTcs.append(temp)

        #vn
        temp = []
        for i in xrange(0, 3):
            temp.append(0)
        vertexNormals.append(temp)

    triangleNumber = len(indices) / 3

    for index in xrange(0, triangleNumber):
        tempindex = []
        for i in xrange(0, 3):
            tempindex.append(indices[3 * index + i])
        indexs.append(tempindex)
    return vertexPoses, vertexTcs, vertexNormals, indexs

def GetCorrectDir(fileName) :
    correctName = ''
    pardir = os.path.dirname(fileName)
    lastname = pardir.split('\\')[-1]
    pathlist = os.listdir(pardir)
    for path in pathlist:
        if path == 'universes' and lastname == 'res':
            return pardir
    correctName = GetCorrectDir(pardir)
    return correctName
    
def GetTerrain(chunklist):
    global mVertRows
    global mVertCols
    global heights
    
    nowPath = os.getcwd()
    temppath = nowPath + '\\' + 'temp\\'
    terrainpath = temppath + 'terrain'

    
    vertexPoseslist = []
    vertexTcslist = []
    vertexNormalslist = []
    indexslist = []
    fileName = []

    hash_map = []
    resultdict = {}
    for chunk in chunklist:
        if chunk[:-6] in hash_map:
            continue
        hash_map.append(chunk[:-6])
        filepath = chunk.replace('.chunk', '.cdata') 
        chunkfilepath = chunk.replace('.cdata', '.chunk')
        CorrectDir = GetCorrectDir(chunkfilepath)
        idx = chunkfilepath.find(GetCorrectDir(chunkfilepath))
        fileName.append(chunk[idx + len(CorrectDir) + 1:-6])
        
        tempdict = xp.ParseChunkXml(chunkfilepath)
        resultdict.update(tempdict)
        matrix = tempdict.get(chunkfilepath)
        binsec.extract(filepath, temppath)

        terrainInfo = rotate_height.rotate(terrainpath)

        dh.cleanDir(temppath)
        os.rmdir(temppath)

        mVertRows = terrainInfo[0]
        mVertCols = terrainInfo[1]
        

        heights = terrainInfo[2]
        
        assert mVertRows == mVertCols and (mVertRows == 28 or mVertRows == 53)  
        
        Pos, Tcs, Normal, Index = BuildGeometry(matrix)

        vertexPoseslist.append(Pos)
        vertexTcslist.append(Tcs)
        vertexNormalslist.append(Normal)
        indexslist.append(Index)

    return vertexPoseslist, vertexTcslist, vertexNormalslist, indexslist, fileName, mVertRows == 28, resultdict

if __name__ == '__main__':
    GetTerrain()


