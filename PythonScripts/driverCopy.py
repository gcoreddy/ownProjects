#!/usr/bin/env python
import os
import threading
import sys
import shutil
import time
rootDir = sys.argv[1]
dest = sys.argv[2]
#dest="C:\Users\cas\Desktop\NEW"
#rootDir="\\\perflab-blr.amd.com\\PerformanceLAB\\DRIVERS\\AMD\\15.x\\15.10\\beta12\\150330a-182123E-ATI"

if len(sys.argv) != 3:
	print "Invalid arguments mentioned"
	print "%s <Driver location> <destination directory to which driver need to copy>"%(sys.argv[0])
	sys.exit(1)
	
def worker(src,des):
	print "Start copying"
	cmd="copy %s %s"%(src,des)
	os.system(cmd)
	return
	
threads = []
startTime=time.time()
for root,dirs,files in os.walk(rootDir):
	print "Root Dir is:",root
	print dirs
	print files
	for dir in dirs:
		newPath=os.path.join(root,dir)
		newDir=newPath.split(rootDir)[1]
		os.chdir(dest)
		#print os.path.join(dest,newDir[1:])
		DirPath=os.path.join(dest,newDir[1:])
		os.makedirs(DirPath)
	for file in files:
		import threading
		#print "File isssssssss"
		new=root.split(rootDir)[1]
		new2=os.path.join(dest,new[1:])
		source = os.path.join(root,file)
		#destination=os.path.join(new2,file)
		print "====================="
		print "source is:",source
		print "Destination is:",new2
		print "======================="
		t = threading.Thread(target=worker,args=(source,new2))
		threads.append(t)
		t.start()
		#md="copy %s %s"%(source,new2)
		#s.system(cmd)
elaspedTime=time.time()-startTime
print "\n================================"
print "totatime taken to copy the files is:",elaspedTime
		
	
	
