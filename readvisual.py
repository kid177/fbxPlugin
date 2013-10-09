# -*- coding:gb18030 -*-

import sys
import os
from xml.dom.minidom import parseString

#从path文件夹里找出所有的chunk信息
#chunkdict里 {key->value} value:(chunk transform), (model transforms)
nowpath = ''
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

def FindSceneDir(filename):
    global nowpath
    nowpath += '..//'
   

    pardir = os.path.dirname(filename)
    lastname = pardir.split('\\')[-1]
    pathlist = os.listdir(pardir)
    #print nowpath
    #print pardir
    #raw_input()
    for path in pathlist:
        if path == 'universes' and lastname == 'res':
            #print pardir
            #raw_input('~~~')
            nowpath = nowpath[:-6] 
            return
    FindSceneDir(pardir)

def ParseVisualXml(fileName):
    content = open(fileName, 'r+').read()
    content = unicode(content, 'cp936').encode('utf-8')
    doc = parseString(content)
    root = doc.documentElement
    
    GroupTextures = root.getElementsByTagName('material')
    lDiffuseTex = []
    lNormalTex = []
    lSpecularTex = []
    #print len(GroupTextures)
    for i in xrange(0, len(GroupTextures)):
        TextureList = GroupTextures[i].getElementsByTagName('Texture')
        TextureSize = len(TextureList)
        #print TextureList[0].childNodes[0].nodeValue
        #print TextureList[0].childNodes[0].nodeValue.replace('\t', '').split("/")[-1]
        DiffuseName = ''
        NormalName = ''
        SpecularName = ''
        if TextureSize >= 1:
            DiffuseName = nowpath + '\\' + TextureList[0].childNodes[0].nodeValue.replace('\t', '')
        if TextureSize >= 2:
            NormalName = nowpath + '\\' + TextureList[1].childNodes[0].nodeValue.replace('\t', '')
        if TextureSize >= 3:
            SpecularName = nowpath + '\\' + TextureList[2].childNodes[0].nodeValue.replace('\t', '')
        #print DiffuseName
        lDiffuseTex.append(DiffuseName)
        lNormalTex.append(NormalName)
        lSpecularTex.append(SpecularName)
        #print len(TextureList)
        #raw_input()
        #row = chunk_transform.getElementsByTagName('row' + str(i))[0]
        #row = row.childNodes[0].nodeValue.split()
        #chunk_matrix.append([float(row[0]), float(row[1]), float(row[2])])
    
    return lDiffuseTex, lNormalTex, lSpecularTex

def GetInfoFromVisual(fileName):
    FindSceneDir(fileName) 
    return ParseVisualXml(fileName)

FileName = 'E:\\code\\python\\samples\\Texture\\ExportScene03\\wjmy\\slj_wicz0042_2502.visual'
if __name__ == '__main__':
    GetInfoFromVisual(FileName)

