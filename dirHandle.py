#author @liyy hzliyangyang@corp.netease.com
#coding=gbk
import os
#import Image
import time
import gzip
import math
import struct

import shutil

def cleanDir( Dir ):
	if os.path.isdir( Dir ):
		paths = os.listdir( Dir )
		for path in paths:
			filePath = os.path.join( Dir, path )
			if os.path.isfile( filePath ):
				try:
					os.remove( filePath )
				except os.error:
					autoRun.exception( "remove %s error." %filePath )#引入logging
			elif os.path.isdir( filePath ):
				if filePath[-4:].lower() == ".svn".lower():
					continue
				shutil.rmtree(filePath,True)

def getfilename(filepath):
	fileName = filepath.split("\\")
	fileName = fileName[len(fileName)-1]
	fileName = fileName.split(".")[0]
	return fileName
	
def getpathfilename(filepath):
	#print "~~~~~~~~~~~~"
	#print filepath
	fileName = filepath.replace(".model","")
	fileName = fileName.replace("E:\\svn\\bw-art\\tw2\\res\\","")
	#print fileName
	fileName = fileName.replace("\\","~")
	#print fileName
	return fileName

def getallfileInDir( Dir ):
	allfilesInfo = []
	if os.path.isdir( Dir ):
		paths = os.listdir( Dir )
		for path in paths:
			filePath = os.path.join( Dir, path )
			if os.path.isfile( filePath ):
				allfilesInfo.append(filePath)
			elif os.path.isdir( filePath ):
				shutil.rmtree(filePath,True)
	return allfilesInfo
	


def getValidFilepath(modelpaths):
	validModelpaths = []
	for modelpath in  modelpaths:
		#找不到对应.primitives文件的，不处理
		primitivespath = modelpath.replace(".model",".primitives")
		if os.path.isfile(primitivespath):
			#有的场景里放了角色模型，不处理
			if modelpath.find("char") == -1:#非PNUVTB的文件
				#if modelpath.find("slj_wjhd0010_wb") == -1:#非PNUVTB的文件
				validModelpaths.append(modelpath)
	return validModelpaths
