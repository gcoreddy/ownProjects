#!/usr/bin/env python3
from jira.client import JIRA
import sys
import shutil
import csv
import os

# AMD JIRA Credentials
server = "http://10.181.36.21"
user = "chareddy"
password = "Chandu@468"

def help():
	print ("************************************************")
	print ("Use one of the following options to run the script")
	print ("OPTION1: %s \"<EpicName>\""%(sys.argv[0]))
	print ("OPTION2: %s <EpicName> <ExistingCsvFile>"%(sys.argv[0]))
	print ("If trying to extract for the first time, Then use first OPTION")
	print ("If trying to update the existing sheet, then use OPTION2")
	print ("************************************************")
	sys.exit(1)

if len(sys.argv) < 2 or len(sys.argv) > 3:
	print("Invalid Inputs passed")
	help()

epicName = str(sys.argv[1])
setFlag=False
if len(sys.argv) == 3:
	ResultFile=sys.argv[2]
	if os.path.isfile(ResultFile) != True:
		print("CSV files passed doesn't exist.")
		print("Please pass the correct csv")
		help()
	setFlag=True
else:
	ResultFile="ProjectStatusReport.csv"
	


options = {'server' : server}
projectName=epicName.split("-")[0]
print ("Creating Jira Object")
jira = JIRA(options,basic_auth=(user, password))
queryString = '"Epic Link" in (%s)'%(epicName)
issues = jira.search_issues(queryString,maxResults=-1,expand='changelog')
fieldnames = ['ISSUE ID', 'ISSUE NAME','ISSUE TYPE', 'STATE','LABELS', 'COMMENT']
if setFlag == True:
	csvFile = open(ResultFile, 'r')
	tpfile = open("tempFile.csv",'w')
	reader = csv.DictReader(csvFile)
	writer = csv.writer(tpfile, delimiter=',', quotechar='"')
	count=0
	newFieldNames=reader.fieldnames
	writer = csv.DictWriter(tpfile,fieldnames=newFieldNames)
	writer.writeheader()	
	for row in reader:
		if row['ISSUE ID'] == None or row['ISSUE ID'] == '':
			print("End of file reached")
			break
		for issue in issues:
			if row['ISSUE ID'] == issue.key:
				print("Getting or updating info about the issue:",issue.key)
				if row['ISSUE TYPE'] != str(issue.fields.issuetype):
					print("ISSUE type changed")
					row['ISSUE TYPE'] = issue.fields.issuetype
				if row['STATE'] != str(issue.fields.status):
					print("status changed")
					row['STATE'] = issue.fields.status
				if row['ISSUE NAME'] != str(issue.fields.summary):
					print("Issue name changed")
					row['ISSUE NAME'] = issue.fields.summary
				if row['LABELS'] != str(issue.fields.labels):
					print("label changed")
					print(row['LABELS'])
					print(issue.fields.labels)
					row['LABELS'] = issue.fields.labels
				writer.writerow(row)
				break
	csvFile.close()
	tpfile.close()
	shutil.move("tempFile.csv", ResultFile)
	print("***********************************************")
	print("Please find the updated report from the file:",ResultFile)
	print("***********************************************")
else:
	csvF=open(ResultFile,"w")
	writer = csv.DictWriter(csvF, fieldnames=fieldnames)
	writer.writeheader()
	count=0
	for issue in issues:
		count+=1
		print("Getting and updating info about the Issue:",issue.key)
		writer.writerow({'ISSUE ID': issue.key, 'ISSUE NAME':issue.fields.summary,'STATE':issue.fields.status, 'ISSUE TYPE': 'Defect','LABELS':issue.fields.labels})
	print("***********************************************")
	print("Total Issues found in this EPIC:",count)
	print("Please find the report from the file:",ResultFile)
	print("***********************************************")
	csvF.close()
