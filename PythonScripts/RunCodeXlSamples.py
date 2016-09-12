#!/usr/bin/env python
import os
import sys
import glob
print len(sys.argv)
if len(sys.argv) != 3:
	print "Please enter the valid inputs"
	print "%s <ARG1> <ARG2>"%(sys.argv[0])
	print "%s <Opencl Samples Directory> <Results path>"%(sys.argv[0])
	sys.exit(1)

path=sys.argv[1]
#resultPath="/home/cas/chandu/tokka/"
resultPath=sys.argv[2]
#workingDir="/home/cas/AMDAPPSDK-3.0/samples/opencl/bin/x86_64"
workingDir=path
#path=workingDir
if not os.path.isdir(resultPath):
	os.makedirs(resultPath)

if not os.path.isdir(path):
	print "Wrong input for samples directory"
	print "Please provide the proper samples directory"
	sys.exit(1)
for root,dirs,files in os.walk(path):
	for f in files:
		if f.endswith(".bmp") or f.endswith(".so") or f.endswith(".txt") or f.endswith(".h") or f.endswith(".hpp") or f.endswith(".bc") or f.endswith(".cl"):
			continue
		else:
			cmd = "./sprofile -o %s/%s.atp -t -T -w %s %s/%s --device gpu"%(resultPath,f,workingDir,workingDir,f)
			import commands
			#(ret,op) = commands.getstatusoutput(cmd)
			ret = os.system(cmd)
			if ret !=0:
				print "Command Failed with the sample:",f
		

