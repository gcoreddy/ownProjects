#!/usr/bin/env python
from jira.client import JIRA
from jira.client import GreenHopper
import jira.client
import csv
import time
import sys

server = "https://amdjira1.atlassian.net/"
user = "chandra-obul.Reddy@amd.com"
password = "Chandu@40689"

projectName =  sys.argv[1]
boardId = sys.argv[2]
tcdict = {}
options = {'server' : server}
print "Creating Jira Object"
interface_obj = JIRA(options,basic_auth=(user, password))
ResultFile="Result_Summary_%s.csv"%(time.time())
#csvFile=open(ResultFile,"w")
fieldnames = ['IssueId', 'IssueType', 'EstimatedTime']
#writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
#writer.writeheader()
#projects=interface_obj.projects()
#keys = sorted([project.key for project in projects])
issue_list = []
completed_issues = []
incompleted_issues = []

#if projectName in keys:
#	searching = 'project =' + projectName
#	for iss in interface_obj.search_issues(searching):
#		issue_list.append(iss.key)
		
#print issue_list

gh = GreenHopper(options,basic_auth=(user, password))
# Get all boards viewable by anonymous users.
boards = gh.boards()
# Get the sprints in a specific board
for board in boards:
	if board.id == 11:
		sprints = gh.sprints(board.id)
		for sprint in sprints:
			print sprint
			incompleted_issues.append(gh.incompleted_issues(board.id,sprint.id))
			completed_issues.append(gh.completed_issues(board.id,sprint.id))
			#incompleted_issues = gh.incompleted_issues(board.id, sprint.id)
			#print incompleted_issues
			# gh.incompleted_issues(board.id,sprint.id)
			#for iss in interface_obj.search_issues(sprint.name):
			#	issue_list.append(iss.key)
print "Completed issues areeeee:",completed_issues
print "Incompleted issue areeeeeeeeeeeeee:",incompleted_issues
#for sprint in sprints:
#	print sprint.raw
#	print sprint.id
#	print sprint.name
		#sys.exit(1)
