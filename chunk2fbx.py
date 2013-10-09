# -*- coding:gbk -*-
import readcdata as rc
import os
import sys
import FbxCommon
import xmlparse as xp
import binsec
import rotate_height
import dirHandle as dh
from fbx import *
import merge
from xml.dom.minidom import parse, parseString, Document

mVertRows = 0
mVertCols = 0
heghts = 0

def PrintHint(pString, pFlag = False):
    Hint = '#'
    if pFlag:
        Hint = '*'
    print Hint * 15 + '\n' + pString + '\n' + Hint * 15

def CreateScene(pSdkManager, pScene, pModeInfo):
    lSceneInfo = FbxDocumentInfo.Create(pScene, 'SceneInfo')
    lSceneInfo.mTitle = 'Demo cdata'
    lSceneInfo.mSubject = 'Demo'
    lSceneInfo.mAuthor = 'kid177'
    lSceneInfo.mRevision = 'rev. x.x + 1'

    pScene.SetSceneInfo(lSceneInfo)
    
    lInfoSize = len(pModeInfo[0])
    for i in xrange(0, lInfoSize):
        lMeshNode = CreateMesh(pSdkManager, pScene, pModeInfo[-3][i],
                [pModeInfo[0][i], pModeInfo[1][i], pModeInfo[2][i], pModeInfo[3][i]])
        pScene.GetRootNode().AddChild(lMeshNode)
    

def InitNormal(pMesh):
    lLayer = pMesh.GetLayer(0)
    if lLayer == None:
        pMesh.CreateLayer()
        lLayer = pMesh.GetLayer(0)
    lLayerElementNormal = FbxLayerElementNormal.Create(pMesh, '')
    
    lLayerElementNormal.SetMappingMode(FbxLayerElement.eByControlPoint)

    lLayerElementNormal.SetReferenceMode(FbxLayerElement.eDirect)

    return lLayerElementNormal, lLayer

def InitUV(pMesh):
    lLayer = pMesh.GetLayer(0)

    lLayerElementUV = FbxLayerElementUV.Create(pMesh, '')

    lLayerElementUV.SetMappingMode(FbxLayerElement.eByControlPoint)

    lLayerElementUV.SetReferenceMode(FbxLayerElementUV.eDirect)

    return lLayerElementUV

def CreateMesh(pSdkManager, pScene, pName, pModeInfo):
    
    lVertexList = pModeInfo[0]
    lVuvList = pModeInfo[1]
    lNormalList = pModeInfo[2]
    lIndexList = pModeInfo[3]
    lNormalPoint = []
    lDividePoint = []
    lStartPoint = 0



    lMeshNode = FbxNode.Create(pScene, pName)
    #print pName
        
        

    lMesh = FbxMesh.Create(pScene, pName)
        
    lVertexCount = len(lVertexList)

    lMesh.InitControlPoints(lVertexCount)


    lControlPoints = lMesh.GetControlPoints()
    lNormalPoint = lMesh.GetControlPoints()
    lUVPoint = lMesh.GetControlPoints() 

    lLayerElementNormal, lLayer = InitNormal(lMesh)
    lLayerElementUV = InitUV(lMesh)

    for cnt in xrange(0, lVertexCount):
        x1, y1, z1 = lVertexList[cnt]
        x2, y2, z2 = lNormalList[cnt]
        x3, y3 = lVuvList[cnt]

        #x1 = -x1
        z1 = -z1
        y3 = 1 - y3

        #set pos point
        lControlPoints[cnt] = FbxVector4(x1, y1, z1)
        #set normal point
        lNormalPoint[cnt] = FbxVector4(x2, y2, z2)
        #set uv point
        lUVPoint[cnt] = FbxVector2(x3, y3)
        #map normal point to pos point
        lLayerElementNormal.GetDirectArray().Add(lNormalPoint[cnt])
        #map uv point to pos point
        lLayerElementUV.GetDirectArray().Add(lUVPoint[cnt])
        #map pos point to index
        lMesh.SetControlPointAt(lControlPoints[cnt], cnt)
        
    lLayer.SetUVs(lLayerElementUV)

       
    lCount = 0
    for i in xrange(0, len(lIndexList)):
        lMesh.BeginPolygon(lCount)
        lCount += 1
        for j in xrange(0, 3):
            lMesh.AddPolygon(lIndexList[i][j])
        lMesh.EndPolygon()

    #set normal point
    lMesh.ComputeVertexNormals(False)

    #set mesh to meshnode
    lMeshNode.SetNodeAttribute(lMesh)
    lMeshNode.LclScaling.Set(FbxDouble3(10, 10, 10)) 
    return lMeshNode

def CreateFbx(pFileName, pChunkList):
    #try:
    lModelInfoList = rc.GetTerrain(pChunkList)
    #except:
    #    PrintHint('Read Chunk Error', True)
    #    raw_input('press enter to exit...')
    #    sys.exit(-1)
    
    (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()
    FbxSystemUnit.Inch.ConvertScene(lScene)
    CreateScene(lSdkManager, lScene, lModelInfoList) 
    lRsult = FbxCommon.SaveScene(lSdkManager, lScene, pFileName)

    FbxAxisSystem.DirectX.ConvertScene(lScene)
    if lRsult == False:
        PrintHint('Save Scene Error', True)
        raw_input('press enter to exit...')
        lSdkManager.Destroy()
        sys.exit(-1)
    
    lSdkManager.Destroy()
    return lModelInfoList[-1], lModelInfoList[-2]

def main(pChunkList):
    
    print 'ChunkList:'
    for pChunk in pChunkList:
        print pChunk

    PrintHint('Begin Export Scene')
    raw_input('press enter to work...')

    lChunkInfo, lFlag = CreateFbx('terrain', pChunkList)
    PrintHint('Export Scene Finish') 
    
    PrintHint('Begin Merge')
    raw_input('press enter to work...')

    merge.main(lChunkInfo, pChunkList[0], lFlag)

if __name__ == '__main__':
    try:
        main()
        raw_input('#' * 15 + '\nsuccessfully!~\n' + '#' * 15 + '\npress enter to exit')
    except Exception, info:
        print Exception, ':', info
        raw_input('press enter to exit...')
    sys.exit(0)


