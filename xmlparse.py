# -*- coding:gb18030 -*-

import sys
import os
from xml.dom.minidom import parseString

#从path文件夹里找出所有的chunk信息
#chunkdict里 {key->value} value:(chunk transform), (model transforms)
chunkdict = {}

def GetAllChunk(DirName):
    allfilesInfo = []
    if os.path.isdir(DirName):
        paths = os.listdir(DirName)
        for path in paths:
            filePath = os.path.join(DirName, path)
            if os.path.isfile(filePath) and filePath.find('.chunk') != -1:
                allfilesInfo.append(filePath)
            elif os.path.isdir(filePath):
                allfilesInfo.extend(GetAllChunk(filePath))
    return allfilesInfo

def ParseChunkXml(fileName):
    content = open(fileName, 'r+').read()
    content = unicode(content, 'cp936').encode('utf-8')
    doc = parseString(content)
    root = doc.documentElement
    
    chunk_transform = root.getElementsByTagName('transform')[-1]
    chunk_matrix = []
    for i in xrange(0, 4):
        row = chunk_transform.getElementsByTagName('row' + str(i))[0]
        row = row.childNodes[0].nodeValue.split()
        chunk_matrix.append([float(row[0]), float(row[1]), float(row[2])])

    modellist = root.getElementsByTagName('model')
    for model in modellist:
        resource = model.getElementsByTagName('resource')[0]
        resName = resource.childNodes[0].nodeValue

        resName = resName.replace('.model', '')
        resName = resName.replace('\t', '')
        resName = resName.decode('utf-8').encode('gbk')

        matrix = []
        transform = model.getElementsByTagName('transform')[0]
        for i in xrange(0, 4):
            row = transform.getElementsByTagName('row' + str(i))[0]
            row = row.childNodes[0].nodeValue.split()
            matrix.append([float(row[0]), float(row[1]), float(row[2])])
        chunkdict.setdefault(resName, []).append([chunk_matrix, matrix])
    chunkdict.setdefault(fileName, []).append(chunk_matrix)
    return chunkdict

def GetInfoFromChunk(chunklist):
    for chunk in chunklist:
        ParseChunkXml(chunk)

def GetChunkList(nowPath):
    chunklist = GetAllChunk(nowPath)
    GetInfoFromChunk(chunklist)
    return chunkdict

if __name__ == '__main__':
    GetChunkList()
