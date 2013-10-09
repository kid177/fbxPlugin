# -*- coding:gbk -*-
import os
import sys
import FbxCommon
import xmlparse as xp 
import readprimitives as rp
import readvisual as rv
import threading
from math import asin, acos, atan, degrees, sqrt, sin, cos, radians, fabs, pi
from fbx import *


lDiffuseTextureName = []
lNormalTextureName = []
lSpecularTextureName = []
def PrintHint(pString, pFlag = False):
    Hint = '#'
    if pFlag:
        Hint = '*'
    print Hint * 15 + '\n' + pString + '\n' + Hint * 15

def PrintMeshInfomation(pMeshNode):
    print '#' * 15
    translation = pMeshNode.LclTranslation.Get()
    rotation = pMeshNode.LclRotation.Get()
    scaling = pMeshNode.LclScaling.Get()
    pMesh = pMeshNode.GetNodeAttributeByIndex(0)
    meshName = pMesh.GetName()
    TriangleCount = pMesh.GetPolygonCount()
    VertexCount = pMesh.GetPolygonVertexCount()
    print 'Mesh Name: %s\nMesh VertexCount: %d\nMesh TriangleCount: %d\n' %(meshName, VertexCount, TriangleCount)

def CreateScene(pSdkManager, pScene, pModeInfo, pFileName):
    lSceneInfo = FbxDocumentInfo.Create(pScene, 'SceneInfo')
    lSceneInfo.mTitle = 'Demo scene'
    lSceneInfo.mSubject = 'Demo'
    lSceneInfo.mAuthor = 'kid177'
    lSceneInfo.mRevision = 'rev. x.x'

    pScene.SetSceneInfo(lSceneInfo)

    lMeshList = CreateMesh(pSdkManager, pScene, pFileName, pModeInfo, pFileName)
    
    for lMeshNode in lMeshList:
        pScene.GetRootNode().AddChild(lMeshNode)

def InitNormal(pMesh):
    lLayer = pMesh.GetLayer(0)
    if lLayer == None:
        pMesh.CreateLayer()
        lLayer = pMesh.GetLayer(0)
    lLayerElementNormal = FbxLayerElementNormal.Create(pMesh, 'MeshNormal')
    
    lLayerElementNormal.SetMappingMode(FbxLayerElement.eByControlPoint)

    lLayerElementNormal.SetReferenceMode(FbxLayerElement.eDirect)

    return lLayerElementNormal, lLayer

def InitUV(pMesh):
    lLayer = pMesh.GetLayer(0)

    lLayerElementUV = FbxLayerElementUV.Create(pMesh, 'MeshUV')

    lLayerElementUV.SetMappingMode(FbxLayerElement.eByControlPoint)

    lLayerElementUV.SetReferenceMode(FbxLayerElementUV.eDirect)

    return lLayerElementUV


def CreateTexturef(pScene, pFileName):
    lTexture = FbxFileTexture.Create(pScene, 'hehe')
    #print dir(lTexture)
    lTexture.SetFileName(pFileName) # Resource file is in current directory.
    lTexture.SetTextureUse(FbxTexture.eStandard)
    lTexture.SetMappingType(FbxTexture.eUV)
    lTexture.SetMaterialUse(FbxFileTexture.eModelMaterial)
    lTexture.SetSwapUV(False)
    lTexture.SetTranslation(0.0, 0.0)
    lTexture.SetScale(1.0, 1.0)
    lTexture.SetRotation(0.0, 0.0)

    return lTexture

def CreateMesh(pSdkManager, pScene, pName, pModeInfo, pFileName):
    
    #print pFileName, pName
    #raw_input()
    #print pScene.GetGlobalSettings().GetSystemUnit() == FbxSystemUnit.Inch
    lVertexs = pModeInfo[0]
    lIndex = pModeInfo[1]
    lGroup = pModeInfo[2] 
    lVertexList = []
    lNormalList = []
    lVuvList = []
    lIndexList = []
    lNormalPoint = []
    lDividePoint = []
    lStartPoint = 0
    lMeshList = []
    for i in xrange(0, len(lGroup)):
        lStartPoint += lGroup[i][1]
        lDividePoint.append(lStartPoint)

    #read vertex information
    for vertex in lVertexs:
        lVertex = [vertex[0][0], vertex[0][1], vertex[0][2], 1]
        lVuv = (vertex[1][0], vertex[1][1])
        lNormal = (vertex[2][0], vertex[2][1], vertex[2][2])
        lVertexList.append(lVertex)
        lVuvList.append(lVuv)
        lNormalList.append(lNormal)


    #read indice information
    primitivenumber = len(lIndex) / 3
    lGroupIndex = []
    idx = 0
    for index in xrange(0, primitivenumber):
        if index == lDividePoint[idx]:
            idx += 1
            lGroupIndex.append(lIndexList)
            lIndexList = []
        lOneIndice = []
        for i in xrange(0, 3):
            lOneVertex = []
            temp = lIndex[3 * index + i]
            lOneVertex.append(temp)
            lOneVertex.append(temp)
            lOneVertex.append(temp)
            lOneIndice.append(lOneVertex)
        lIndexList.append(lOneIndice)
    lGroupIndex.append(lIndexList)
   



    modelNumber = 1 
    for model in xrange(0, modelNumber):

        start = 0
        #lNormalTextureName = ['slj_wicz0042_1n_2502.tga', 'slj_wicz0042_17n_wb.tga', 'slj_wicz0042_3n_2502.tga', 'slj_wicz0042_2n_2502.tga', 'slj_wicz0042_7n_wb.tga']
        #lDiffuseTextureName = ['slj_wicz0042_1d_2502.tga', 'slj_wicz0042_17d_wb.tga', 'slj_wicz0042_3d_2502.tga', 'slj_wicz0042_2d_2502.tga', 'slj_wicz0042_7d_a_wb.tga']
        #lSpecularTextureName = ['slj_wicz0042_1s_2502.tga', 'slj_wicz0042_17s_wb.tga', 'slj_wicz0042_3s_2502.tga', 'slj_wicz0042_2s_2502.tga', 'slj_wicz0042_7s_wb.tga']
        #
        for lGroupIdx in xrange(0, len(lGroupIndex)):
            lMeshNode = FbxNode.Create(pScene, pName + '_' + str(lGroupIdx))
            

            lMesh = FbxMesh.Create(pScene, pName + str(lGroupIdx) + str(model))
            
            lVertexCount = lGroup[lGroupIdx][3]

            lMesh.InitControlPoints(lVertexCount)


            lControlPoints = lMesh.GetControlPoints()
            lNormalPoint = lMesh.GetControlPoints()
            lUVPoint = lMesh.GetControlPoints() 
            #add pos
            lLayerElementNormal, lLayer = InitNormal(lMesh)
            #lLayerElementUV = InitUV(lMesh)
            
            # Diffuse
            lTexture = CreateTexturef(pScene, lDiffuseTextureName[lGroupIdx])
            lTextureDiffuseLayer = FbxLayerElementTexture.Create(lMesh, 'Diffuse Texture')
            lTextureDiffuseLayer.SetMappingMode(FbxLayerElement.eByPolygon)
            lTextureDiffuseLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lTextureDiffuseLayer.GetDirectArray().Add(lTexture)
            lLayer.SetTextures(FbxLayerElement.eTextureDiffuse, lTextureDiffuseLayer)

            lUVDiffuseLayer = FbxLayerElementUV.Create(lMesh, "DiffuseUV")
            lUVDiffuseLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
            lUVDiffuseLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lLayer.SetUVs(lUVDiffuseLayer, FbxLayerElement.eTextureDiffuse)

            
            # NormalMap
            lTexture = CreateTexturef(pScene, lNormalTextureName[lGroupIdx])
            lTextureNormalLayer = FbxLayerElementTexture.Create(lMesh, 'Normal Texture')
            lTextureNormalLayer.SetMappingMode(FbxLayerElement.eByPolygon)
            lTextureNormalLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lTextureNormalLayer.GetDirectArray().Add(lTexture)
            lLayer.SetTextures(FbxLayerElement.eTextureNormalMap, lTextureNormalLayer)

            lUVNormalLayer = FbxLayerElementUV.Create(lMesh, "NormalUV")
            lUVNormalLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
            lUVNormalLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lLayer.SetUVs(lUVNormalLayer, FbxLayerElement.eTextureNormalMap)

            # Sepcular
            lTexture = CreateTexturef(pScene, lSpecularTextureName[lGroupIdx])
            lTextureSpecularLayer = FbxLayerElementTexture.Create(lMesh, 'Specular Texture')
            lTextureSpecularLayer.SetMappingMode(FbxLayerElement.eByPolygon)
            lTextureSpecularLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lTextureSpecularLayer.GetDirectArray().Add(lTexture)
            lLayer.SetTextures(FbxLayerElement.eTextureSpecular, lTextureSpecularLayer)

            lUVSpecularLayer = FbxLayerElementUV.Create(lMesh, "SpecularUV")
            lUVSpecularLayer.SetMappingMode(FbxLayerElement.eByPolygonVertex)
            lUVSpecularLayer.SetReferenceMode(FbxLayerElement.eIndexToDirect)
            lLayer.SetUVs(lUVSpecularLayer, FbxLayerElement.eTextureSpecular)
            for cnt in xrange(0, lVertexCount):
                x1, y1, z1, w= lVertexList[cnt + start]
                x2, y2, z2 = lNormalList[cnt + start]
                x3, y3 = lVuvList[cnt + start]

                z1 = -z1

                #x1 = -x1
                #x2 = -x2

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
                #lLayerElementUV.GetDirectArray().Add(lUVPoint[cnt])
                lUVDiffuseLayer.GetDirectArray().Add(lUVPoint[cnt])
                lUVNormalLayer.GetDirectArray().Add(lUVPoint[cnt])
                lUVSpecularLayer.GetDirectArray().Add(lUVPoint[cnt])
                #map pos point to index
                lMesh.SetControlPointAt(lControlPoints[cnt], cnt)
            
            lLayer.SetNormals(lLayerElementNormal)
            #lLayer.SetUVs(lLayerElementUV)

           
            lCount = 0
            
            lIndexTemp = lGroupIndex[lGroupIdx]
            lUVDiffuseLayer.GetIndexArray().SetCount(len(lIndexTemp) * 3)
            lUVNormalLayer.GetIndexArray().SetCount(len(lIndexTemp) * 3)
            lUVSpecularLayer.GetIndexArray().SetCount(len(lIndexTemp) * 3)

            lTextureDiffuseLayer.GetIndexArray().SetCount(len(lIndexTemp))
            lTextureNormalLayer.GetIndexArray().SetCount(len(lIndexTemp))
            lTextureSpecularLayer.GetIndexArray().SetCount(len(lIndexTemp))
            for i in xrange(0, len(lIndexTemp)):
                lMesh.BeginPolygon(-1, -1, False)

                lTextureDiffuseLayer.GetIndexArray().SetAt(i, 0)
                lTextureNormalLayer.GetIndexArray().SetAt(i, 0)
                lTextureSpecularLayer.GetIndexArray().SetAt(i, 0)
                for j in xrange(0, 3):
                    lMesh.AddPolygon(lIndexTemp[i][2 - j][0] - start)

                    lUVDiffuseLayer.GetIndexArray().SetAt(i*3 + j, lIndexTemp[i][2 - j][0] - start)
                    lUVNormalLayer.GetIndexArray().SetAt(i*3 + j, lIndexTemp[i][2 - j][0] - start)
                    lUVSpecularLayer.GetIndexArray().SetAt(i*3 + j, lIndexTemp[i][2 - j][0] - start)
                lMesh.EndPolygon()

            start += lVertexCount
            lMeshNode.SetNodeAttribute(lMesh)
            lMeshList.append(lMeshNode)
            
            PrintMeshInfomation(lMeshNode)
    return lMeshList

def CreateFbx(lPrimitivesList):

    for lPrimitive in lPrimitivesList:
        lFileName = lPrimitive.split('\\')[-1].replace('.primitives', '') 
        #try:
        lModeInfo = rp.GetInfoFromPrimitives(lPrimitive)
        #except:
        #    PrintHint('Read' + lPrimitive +  'Error', True)
        #    raw_input('press enter to exit...')
        #    sys.exit(-1)
        global lDiffuseTextureName
        global lNormalTextureName
        global lSpecularTextureName
        lDiffuseTextureName = []
        lNormalTextureName = []
        lSpecularTextureName = []
        #try:
        lDiffuseTextureName, lNormalTextureName, lSpecularTextureName = rv.GetInfoFromVisual(lPrimitive.replace('.primitives', '.visual'))
        #except:
        #    PrintHint('Read' + lPrimitive.replace('.primitives', '.visual') + 'Error', True)
        #    raw_input('press enter to exit')
        #    sys.exit(-1)
        #print lDiffuseTextureName
        #raw_input()
        (lSdkManager, lScene) = FbxCommon.InitializeSdkObjects()
        FbxSystemUnit.Inch.ConvertScene(lScene)
        FbxAxisSystem.DirectX.ConvertScene(lScene)
        CreateScene(lSdkManager, lScene, lModeInfo, lFileName)

        #FbxSystemUnit.Inch.ConvertScene(lScene)
        
        #SceneAxisSystem = lScene.GetGlobalSettings().GetAxisSystem().GetCoorSystem()
        #print '~~~~'
        #print SceneAxisSystem
        #print dir(FbxAxisSystem)
        FbxCommon.SaveScene(lSdkManager, lScene, lPrimitive.replace('.primitives', ''))
        
        lSdkManager.Destroy()

def main(PrimitivesList):
    
    pPrimitivesList = []
    for path in PrimitivesList:
        if path not in pPrimitivesList and os.path.isfile(path):
            if not path.endswith('.primitives'):
                continue
            pPrimitivesList.append(path)
        elif os.path.isdir(path):
            pPrimitivesList.extend(rp.GetAllPrimitives(path))
    pPrimitivesList = list(set(pPrimitivesList))
    print 'FileList:'
    for pPrimitives in pPrimitivesList:
        print pPrimitives

    PrintHint('Begin Primitives To Fbx')
    raw_input('press enter to work...')

    CreateFbx(pPrimitivesList)
if __name__ == '__main__':
    try:
        main()
        raw_input('#' * 15 + '\nsuccessfully!~\n' + '#' * 15 + '\npress enter to exit')
    except Exception, info:
        print Exception, ':', info
        raw_input('press enter to exit...')
    sys.exit(0)


