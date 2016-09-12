#!/usr/bin/env python
import os
import glob
import sys
import time
filesList = []
#xecDir = sys.argv[1]
#ttFilesDir = sys.argv[2]
ExecDir = "C:\Users\CAS\Desktop\Debug"
AttFilesDir = "C:\Users\CAS\Desktop\Debug"
os.chdir(AttFilesDir)
filesList = glob.glob('TestCase*.txt')
LogDir = "%s/Log_%s"%(ExecDir,time.time())
os.makedirs(LogDir)
TotalTests=0
TotalTestsFailed=0
TotalTestsPass=0
for file in filesList:
	print "=============================================="
	print "Executing ",file.split('.')[0]
	print "----------------------------------------------"
	print "TestCase Execution started..."
	logFile="%s/%s.log"%(LogDir,file.split('.')[0])
	cmd = "APITestTool.exe -s %s > %s"%(file,logFile)
	os.system(cmd)
	print "TestCase Execution completed"
	print "------------------------------------------------"
	f=open(logFile)
	content=f.read()
	TotalTests+=1
	if content.find("Exiting...") == -1 or content.find("failed") != -1:
		print "Result Of the TestCase:FAIL"
		TotalTestsFailed+=1
	else:
		print "Result of the TestCase:PASS"
		TotalTestsPass+=1
print "\n=============================\n"
print "Test Report:\n"
print "Total TestCases Executed:",TotalTests
print "Total TestCases Pass    :",TotalTestsPass
print "\nTotal Testcases Failed:",TotalTestsFailed
print "\n==============================\n"
print "\n Please find the Result files or Log files in the location with the <TestCaseName.log>",logFile
print "End of the Test Execution Bye Bye......."