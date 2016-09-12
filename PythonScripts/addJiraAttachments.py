#!/usr/bin/env python
from jira.client import JIRA
import sys
import os
import csv
user = 'chareddy'
password = 'Chandu@1268'
server = 'http://ontrack-internal.amd.com'
#QAAUTOMATIONPYFX_JIRA_URL = "http://ontrack-internal.amd.com"
#QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL = "http://ontrack-internal.amd.com/secure/attachment"
csvFile = sys.argv[1]
#attachDir = sys.argv[2]

if os.path.isfile(csvFile) != True:
	print("Invalid FCsv file mentioned")
	sys.exit(1)

#if os.path.isdir(attachDir) != True:
#	print("Invalid directory name mentioned")
#	sys.exit(1)

print ("Creating Jira Object")
try:
    interface_obj = JIRA(options = {'server' : server}, basic_auth = (user, password))
except:
    print("Creation of jira object failed..")
    sys.exit(1)
#os.chdir(attachDir)
fd = open(csvFile,'r')
reader = csv.DictReader(fd)
for r in reader:
    if r['TestcaseId'] == None:
        continue
    tcId = r['TestcaseId']
    print(tcId)
    attachment = r['Attachment']
    print("Attachment Name is:",attachment)
    dirName = os.path.dirname(attachment)
    fileName = os.path.basename(attachment)
    print("FileName is:",fileName)
    os.chdir(dirName)
    if os.path.isfile(attachment) != True:
        print("TestCase attachment dowsn't exist in the directory..")
        print("Skipping the adding the attachment for this testCase:",tcId)
        continue
    interface_obj.add_attachment(tcId, fileName, fileName)
    print ("===================================\n")
    print ("Testcase Attachment updated")
    print ("Issue: %s  logfile: %s" % (tcId, attachment))
    print ("===================================\n")
