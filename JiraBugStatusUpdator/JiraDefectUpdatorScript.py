#!/usr/bin/env python3
from jira.client import JIRA
import csv
import sys
from tempfile import NamedTemporaryFile
import shutil
import csv

# AMD JIRA
server = "http://10.181.36.21"
#user = 'chareddy'
#password = 'Chandu@468'
user = "ServerSWQA"
password = "Q7i4@c-2A9j="

def help():
	print ("Use the following command to run the script\n")
	print ("%s \"<boardName>\""%(sys.argv[0]))
	sys.exit(1)

epicName = str(sys.argv[1])
setFlag=False
if len(sys.argv) == 3:
	ResultFile=sys.argv[2]
	setFlag=True
else:
	ResultFile="Result_Summary.csv"
	


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
	for row in reader:
		if count == 0:
			lst = row.keys()
			for l in lst:
				if l not in fieldnames:
					fieldnames.append(l)
			writer = csv.DictWriter(tpfile,fieldnames=fieldnames)
			writer.writeheader()	
		if row['ISSUE ID'] == None or row['ISSUE ID'] == '':
			print("End of file reached")
			break
		for issue in issues:
			if row['ISSUE ID'] == issue.key:
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
				break
		print("Row info after update",row)
		writer.writerow(row)
		count+=1
	csvFile.close()
	tpfile.close()
	shutil.move("tempFile.csv", ResultFile)
else:
	csvF=open(ResultFile,"w")
	writer = csv.DictWriter(csvF, fieldnames=fieldnames)
	writer.writeheader()
	count=0
	for issue in issues:
		count+=1
		print("Updating info about issue:",issue.key)
		writer.writerow({'ISSUE ID': issue.key, 'ISSUE NAME':issue.fields.summary,'STATE':issue.fields.status, 'ISSUE TYPE': 'Defect','LABELS':issue.fields.labels})
	print("Total Defects are:",count)
	csvF.close()
