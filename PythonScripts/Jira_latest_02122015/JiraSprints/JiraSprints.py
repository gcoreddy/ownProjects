#!/usr/bin/env python
from jira.client import JIRA
from jira.client import GreenHopper
from jira.resources import Issue
from datetime import *
from time import *
import csv
import sys

def help():
	print "%s <boardName>"%(sys.argv[0])
	print "Please pass the boardname as an argument"
	sys.exit(1)

if len(sys.argv) != 2:
	print "Invalid number of arguments"
	help()

server = "https://amdjira1.atlassian.net/"
user = "pavan.ramayanam@amd.com"
password = "Vidyuth6"
boardName = str(sys.argv[1])
options = {'server' : server}
completed_issues = []
incompleted_issues = []
issue_list = []
sbtskDict = {}
updtDict = {}
mnthDict = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


def getUpdatedContent(history):
	day=None
	updatedContent=None
	uDict = {}
	for item in history.items:
		count = 1
		spnt = str(sprintInfo['startDate'])
		sprintDate = spnt.split(" ")[0]
		startDate=date(int(str(20)+sprintDate.split("/")[2]),int(mnthDict[sprintDate.split("/")[1]]), \
									 int(sprintDate.split("/")[0]))
		eDate = history.created.split("T")[0].split("-")
		endDate = date(int(eDate[0]),int(eDate[1]),int(eDate[2]))
		for d in map( lambda x: startDate+timedelta(days=x), xrange((endDate-startDate).days)):
			count+=1
		if item.field == "timeestimate" or item.field == "timeoriginalestimate":
			day = "DAY%s EstimatedTime"%(count)
		elif item.field == "timespent":
			day = "DAY%s SpentTime"%(count)
		else:
			continue
		print "Updatating the modified field:%s Info"%(item.field)
		updatedContent="Field:%s\nFromString:%s\nToString:%s"%(item.field,item.fromString,item.toString)
		if day in uDict.keys():
			updatedContent = "%s \n %s"%(uDict[day],updatedContent)
		uDict[day] = updatedContent
	return uDict


class jiraSprint(JIRA):
	def __init__(self, options=None, basic_auth=None, oauth=None, async=None):
		super(jiraSprint, self).__init__(options=options, basic_auth=basic_auth, \
														oauth=oauth, async=async)
	
	def incompleted_issues(self, board_id, sprint_id):
		"""Return the incompleted issues for the sprint"""
		r_json = self._get_json('rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' \
		 							% (board_id, sprint_id),base=self.AGILE_BASE_URL)
		issues = [Issue(self._options, self._session, raw_issues_json) for raw_issues_json \
		 						in r_json['contents']['issuesNotCompletedInCurrentSprint']]
		return issues

print "Creating Jira Object"
jira = jiraSprint(options,basic_auth=(user, password))
ResultFile="Result_Summary_%s.csv"%(time())
csvFile=open(ResultFile,"w")
taskTotalTime = None
subtaskTotalTime = None
fieldnames = ['SPRINT NO','ISSUEID', 'ISSUE TYPE', 'STATE','RELATES TO', \
			'ESTIMATED TIME','START DATE', 'END DATE', 'COMPLETE DATE']
for i in range(1,32):
	dyEstd = "DAY%s EstimatedTime"%(i)
	dySpnt = "DAY%s SpentTime"%(i)
	fieldnames.append(dyEstd)
	fieldnames.append(dySpnt)
writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
writer.writeheader()
boards = jira.boards()

for board in boards:
	if str(board.name) == boardName:
		sprints = jira.sprints(board.id)
		for sprint in sprints:
			sprintInfo=jira.sprint_info(board.id,sprint.id)
			writer.writerow({'SPRINT NO': sprint.name, 'STATE': sprint.state, \
			'START DATE': sprintInfo['startDate'], 'END DATE': sprintInfo['endDate'], \
			 'COMPLETE DATE': sprintInfo['completeDate']})
			print "=============================================="
			print "Updating the information of Sprint:",sprint
			print "=============================================="
			incompleted_issues = jira.incompleted_issues(board.id, sprint.id)
			completed_issues = jira.completed_issues(board.id, sprint.id)
			issue_list = incompleted_issues + completed_issues
			if len(issue_list) != 0:
				for issu in issue_list:
					estTime = None
					issue=jira.issue(issu.key,expand='changelog')
					print "Updating the information about Story/Task:",issue.key
					for history in issue.changelog.histories:
						if history != None:
							updtDict.update(getUpdatedContent(history))
					if issue.fields.timeoriginalestimate != None:
						estTime = str(int(issue.fields.timeoriginalestimate)/3600)+"Hours"
					updtInfo = {'ISSUEID': issu.key, 'ISSUE TYPE':issue.fields.issuetype, 'ESTIMATED TIME':estTime}
					for key in updtDict.keys():
						updtInfo[key] = updtDict[key]
					writer.writerow(updtInfo)
					if issue.fields.issuetype.name == 'Story' or issue.fields.issuetype.name == "Task":
						for iss in issue.fields.subtasks:
							subtask = jira.issue(iss.key, expand='changelog')
							print "Updating the info about Subtask:",subtask.key
							for history in subtask.changelog.histories:
								sbtskDict.update(getUpdatedContent(history))
							if subtask.fields.timeoriginalestimate != None:
								estTime = str(int(subtask.fields.timeoriginalestimate)/3600)+"Hours"
							updtInfo = {'ISSUEID': subtask.key, 'ISSUE TYPE':subtask.fields.issuetype, \
													 'ESTIMATED TIME':estTime ,'RELATES TO': issue.key}
							for key in sbtskDict.keys():
								updtInfo[key] = sbtskDict[key]
							writer.writerow(updtInfo)
			else:
				print "No issues found in the current sprint......"
				continue
			print "============================================="
			print "Updation of the Sprint:%s Completed"%(sprint)
			print "============================================="
