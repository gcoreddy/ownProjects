#!/usr/bin/env python3
from jira.client import JIRA
import sys
import os
import csv

#user = 'chareddy'
#password = 'Chandu@468'
user = 'ServerSWQA'
password = 'Q7i4@c-2A9j='

server = 'http://ontrack-internal.amd.com'


def help():
    print("Help function")
    print("%s <option> <csvFile> <FilesDirectory>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("%s addAttachments <csvFile> <attachmentDir>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("%s deleteAttachments <csvFile>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("%s updateLabel <csvFile>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("%s updateSummary <csvFile>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")
    print("%s updateDescription <csvFile>"%(sys.argv[0]))
    print("+++++++++++++++++++++++++++++++++++++++++")

    sys.exit(1)

if len(sys.argv) < 2:
    print("Invalid arguments mentioned")
    help()

print ("Creating Jira Object")
try:
    interface_obj = JIRA(options = {'server' : server}, basic_auth = (user, password))
except:
    print("Creation of jira object failed..")
    sys.exit(1)

if sys.argv[1] == "addAttachments":
    if len(sys.argv) != 4:
        print(len(sys.argv))
        print("Invalid options mentioned")
        help()
    csvFile = sys.argv[2]
    attachDir = sys.argv[3]
    if os.path.isfile(csvFile) != True:
        print("Invalid FCsv file mentioned")
        sys.exit(1)

    if os.path.isdir(attachDir) != True:
        print("Invalid directory name mentioned")
        sys.exit(1)

    os.chdir(attachDir)
    fd = open(csvFile,'r')
    reader = csv.DictReader(fd)
    for r in reader:
        try:
            if r['TestcaseId'] == None:
                continue
            tcId = r['TestcaseId']
            attachment = r['Attachment']
        except Exception as e:
            print("Excpetion occured:",e)
            sys.exit(1)
        if os.path.isfile(attachment) != True:
            print("TestCase attachemnt dowsn't exist in the directory..")
            print("Skipping the adding the attachemnt for this testCase:",tcId)
            sys.exit(1)
        interface_obj.add_attachment(tcId, attachment, attachment)
        print ("===================================\n")
        print ("Testcase Attchment updated")
        print ("Issue: %s  logfile: %s" % (tcId, attachment))
        print ("===================================\n")

elif sys.argv[1] == "deleteAttachments":
    if len(sys.argv) != 3:
        print("Invalid Options mentioned")
        help()
    csvFile = sys.argv[2]
    fd = open(csvFile,'r')
    reader = csv.DictReader(fd)
    for r in reader:
        try:
            if r['TestcaseId'] == None:
                continue
            tcId = r['TestcaseId']
            print(tcId)
            attachment = r['Attachment']
            fileName = attachment
        except Exception as e:
            print("Excpetion occured:",e)
            sys.exit(1)
        issue = interface_obj.issue(tcId)
        for atchmnt in issue.fields.attachment:
            if atchmnt.filename == fileName:
                print("Deleting Filename:",fileName)
                atchmnt.delete()
        print ("===================================\n")
        print ("Testcase Attachment deleted")
        print ("Issue: %s  logfile: %s" % (tcId, attachment))
        print ("===================================\n")

elif sys.argv[1] == "updateLabel":
    if len(sys.argv) != 3:
        print("Invalid Options mentioned")
        help()
    csvFile = sys.argv[2]
    fd = open(csvFile,'r')
    reader = csv.DictReader(fd)
    for r in reader:
        try:
            if r['TestcaseId'] == None:
                continue
            tcId = r['TestcaseId']
            print(tcId)
            attachment = r['Labels']
            fileName = attachment
        except Exception as e:
            print("Exception occured:",e)
            sys.exit(1)
        issue = interface_obj.issue(tcId)
        issue.fields.labels.append(attachment)
        issue.update(fields={"labels": issue.fields.labels})
        print ("===================================\n")
        print ("Testcase Attachment updated")
        print ("Issue: %s  logfile: %s" % (tcId, attachment))
        print ("===================================\n")
elif sys.argv[1] == "updateSummary":
    if len(sys.argv) != 3:
        print("Invalid Options mentioned")
        help()
    csvFile = sys.argv[2]
    fd = open(csvFile,'r')
    reader = csv.DictReader(fd)
    for r in reader:
        try:
            if r['TestcaseId'] == None:
                continue
            tcId = r['TestcaseId']
            print(tcId)
            smry = r['Summary']
        except Exception as e:
            print("Exception occured:",e)
            sys.exit(1)
        issue = interface_obj.issue(tcId)
        issue.update(summary=smry)
        print ("===================================\n")
        print ("Testcase Summary updated")
        print ("Issue: %s  summary: %s" % (tcId, smry))
        print ("===================================\n")
elif sys.argv[1] == "updateDescription":
    if len(sys.argv) != 3:
        print("Invalid Options mentioned")
        help()
    csvFile = sys.argv[2]
    fd = open(csvFile,'r')
    reader = csv.DictReader(fd)
    for r in reader:
        try:
            if r['TestcaseId'] == None:
                continue
            tcId = r['TestcaseId']
            print(tcId)
            desc = r['Description']
        except Exception as e:
            print("Exception occured:",e)
            sys.exit(1)
        issue = interface_obj.issue(tcId)
        issue.update(description=desc)
        print ("===================================\n")
        print ("Testcase Description updated")
        print ("Issue: %s Description: %s" % (tcId, desc))
        print ("===================================\n")
else:
    print("Invalid option mentioned")
    help()
