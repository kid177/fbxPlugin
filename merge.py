# -*- coding:gbk -*-
import os
import FbxCommon
import matrixhandle as mh
import primitives2fbx as p2f
import time
from fbx import *

nowpath = ''
hash_map = []
startX = 0
startZ = 0
DEBUG = True
month = {
        "Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12,}
def PrintHint(pString, pFlag = False):
    Hint = '#'
    if pFlag:
        Hint = '*'
    print Hint * 15 + '\n' + pString + '\n' + Hint * 15

def FindSceneDir(filename):
    global nowpath
    pardir = os.path.dirname(filename)
    lastname = pardir.split('\\')[-1]
    pathlist = os.listdir(pardir)
    for path in pathlist:
        if path == 'universes' and lastname == 'res':
            #print pardir
            #raw_input('~~~')
            nowpath = pardir
            return
    FindSceneDir(pardir)

def Compare(x, y):
    x = x.split()
    y = y.split()
    if int(x[-1]) < int(y[-1]):
        return True
    if int(x[-1]) > int(y[-1]):
        return False
    if month[x[1]] < month[y[1]]:
        return True
    if month[x[1]] > month[y[1]]:
        return False
    if int(x[2]) < int(y[2]):
        return True
    if int(x[2]) > int(y[2]):
        return False
    hh1, mm1, ss1 = x[3].split(':')
    hh2, mm2, ss2 = y[3].split(':')

    if int(hh1) < int(hh2):
        return True
    if int(hh1) > int(hh2):
        return False
    if int(mm1) < int(mm2):
        return True
    if int(mm1) > int(mm2):
        return False
    if int(ss1) < int(ss2):
        return True
    if int(ss1) > int(ss2):
        return False

def Check(pFileName):
    lPriName = pFileName + '.primitives'
    lFbxName = pFileName + '.fbx'
    if os.path.isfile(lPriName) and (not os.path.isfile(lFbxName)):
        return False
    lTimePri = time.ctime(os.path.getmtime(lPriName))
    lTimeFbx = time.ctime(os.path.getmtime(lFbxName))
    
    return Compare(lTimePri, lTimeFbx)

def main(pChunkInfo, pTempFile, pFlag):
    global nowpath
    global startX
    global startZ
    if pFlag:
        startX = startZ = 4
    else:
        startX = startZ = 2
    #try:
    FindSceneDir(pTempFile)
    #except:
    #    PrintHint("Can't Find The Root Please Check Your DirPath", True)
    #    raw_input('press enter to exit...')
    #    sys.exit(-1)
    keys = []
    for key in pChunkInfo.keys():
        keys.append([nowpath + '\\' + key, key])


    lSdkManager = FbxManager.Create()
    ios = FbxIOSettings.Create(lSdkManager, IOSROOT)
    lSdkManager.SetIOSettings(ios)

    lMyRefScene = FbxScene.Create(lSdkManager, 'My Reference Scene')
    FbxSystemUnit.Inch.ConvertScene(lMyRefScene) 
    FbxAxisSystem.DirectX.ConvertScene(lMyRefScene)

    lCurrentScene = FbxScene.Create(lSdkManager, 'My scene')
    FbxSystemUnit.Inch.ConvertScene(lCurrentScene) 
    FbxAxisSystem.DirectX.ConvertScene(lCurrentScene) 
    #load the first scene
    lResult = FbxCommon.LoadScene(lSdkManager, lMyRefScene, 'terrain.fbx')
    #load the second scene
    if os.path.isfile('scene.fbx'):
        os.remove('scene.fbx')
    if DEBUG:
        allcount = 0
        f = open('save.txt','w')
        for key in keys:
            if os.path.isfile(key[0] + '.primitives'):
                allcount += 1
                f.write('id = %d, name = %s\n' %(allcount, key[0] + '.primitives'))
        f.close()
        nowcount = 0
        f = open('log.txt','w')
    for key in keys:
        #print key
        #raw_input('key name')
        if not os.path.isfile(key[0] + '.primitives'):
                continue
        
        if key[0].find('nos_block002') != -1:
            continue
        #if not Check(key[0]):
        print 'Create:' + key[0] + '.fbx'
        try:
            p2f.CreateFbx([key[0] + '.primitives', ])
        except:
            print key[0] + '.fbx'
            raw_input('error???')
        if DEBUG:
            nowcount += 1
            f.write('write fbx id = %d, sum = %d, name = %s\n' %(nowcount, allcount, key[0] + '.primitives'))
        lMatrix = pChunkInfo.get(key[1])
        #print lMatrix
        #raw_input('matrix')
        lModelNumber = len(lMatrix) 
        for model in xrange(0, lModelNumber):
            
            lMatrixA = lMatrix[model][0]
            lMatrixB = lMatrix[model][1]
            
            lScaling = mh.GetScalingFromMatrix(lMatrixB)
            lRotation = mh.GetRotaionFromMatirx(lMatrixB)
            
            result = FbxCommon.LoadScene(lSdkManager, lCurrentScene, key[0] + '.fbx')
            if not result:
                print 'no such fbx??? error?? what ?? !!~~'
                continue
            #print result
            while lCurrentScene.GetRootNode().GetChildCount() <> 0:
                #print '~~~~~~'
                #raw_input()
                for i in xrange(0, lCurrentScene.GetRootNode().GetChildCount()):
                    lChildNode = lCurrentScene.GetRootNode().GetChild(i)
                    if lChildNode == None:
                        continue
                    lChildNode.SetRotationOrder(FbxNode.eSourcePivot, eEulerZXY)
                    lChildNode.LclTranslation.Set(FbxDouble3(float(lMatrixA[3][0] + lMatrixB[3][0] + startX) * 10, float(lMatrixA[3][1] + lMatrixB[3][1]) * 10,
                        float(-(lMatrixA[3][2] + lMatrixB[3][2] + startZ) * 10)))
                    lChildNode.LclScaling.Set(FbxDouble3(float(lScaling[0]) * 10, float(lScaling[1]) * 10, float(lScaling[2] * 10)))
                    lChildNode.LclRotation.Set(FbxDouble3(float(lRotation[0]), float(lRotation[1]), float(lRotation[2])))
                    lMyRefScene.GetRootNode().AddChild(lChildNode)

            lCurrentScene.GetRootNode().DisconnectAllSrcObject()

            for i in xrange(0, lCurrentScene.GetSrcObjectCount()):
                lObj = lCurrentScene.GetSrcObject(i)
                if lObj == lCurrentScene.GetRootNode() or lObj == lCurrentScene.GetGlobalSettings():
                    continue

                lObj.ConnectDstObject(lMyRefScene)
            lCurrentScene.DisconnectAllSrcObject()
        if DEBUG:
            f.write('now fbx write successful!~\n')
    if DEBUG:
        f.write('all fbx write successful and begin to save scene\n')
        f.close()
    FbxCommon.SaveScene(lSdkManager, lMyRefScene, 'scene.fbx')
    
   # print dir(FbxSystemUnit)
   # print lMyRefScene.GetGlobalSettings().GetSystemUnit() == FbxSystemUnit.cm
   # raw_input()
    lSdkManager.Destroy()

if __name__ == '__main__':
    main()
