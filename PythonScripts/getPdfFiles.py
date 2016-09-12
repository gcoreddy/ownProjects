#!/usr/bin/env python
import os
import sys
import shutil

sourceDir=sys.argv[1]
#destDir=sys.argv[2]
FileList=[]
LinkList=[]
links=[]
for root,dirs,files in os.walk(sourceDir):
	for f in files:
		if f.endswith(".pdf"):
			sourceFile=os.path.join(root,f)
			#shutil.copy(sourceFile,destDir)
			outFile="/home/cas/tokkale/%s.txt"%(f.split(".")[0])
			if not os.path.exists("/home/cas/tokkale"):
				os.makedirs("/home/cas/tokkale",0777)
			os.system(("pdftotext %s %s")%(sourceFile,outFile))
			with open(outFile,'r') as INF:
				for line in INF:
					print "Line is:",line
					if ("Compute SDK" in line) or ("ComputeSDK" in line) or ("appsdk" in line):
						print "Verification of pdfFile:%s failed"%(outFile)
						print "File contains Compute SDK string"
						if sourceFile not in FileList:
							FileList.append(sourceFile)

print "totalFileList is:",FileList
			
