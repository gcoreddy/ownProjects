#!/usr/bin/env python
import sys
import re
import os
import subprocess
import platform
from datetime import date
from RestAPIBase import RestAPIBase
import fnmatch
from jira.client import JIRA
errout = sys.stderr.write

def parse_args(TestListRange):
	Tests=[]
	FinalList=[]
	if TestListRange.find(",") != -1:
		Tests=TestListRange.split(",")
		for test in Tests:
			if test.find("-") != -1:
				temp=test.split("-")
				FinalList.extend(range(int(temp[0]),int(temp[1])))
			else:
				FinalList.append(test)
	elif TestListRange.find("-") != -1:
		temp=TestListRange.split("-")
		print temp
		FinalList.extend(range(int(temp[0]),int(temp[1])))
	else:
		FinalList.append(TestListRange)
	return FinalList

def get_data(url,user,passwd):
	import requests
	list=[]
	jira_session = requests.session()
	try:
		jira_session.post('https://amdjira1.atlassian.net', auth=(user, passwd), verify=False)
	except:
		print('Unable to connect or authenticate with JIRA server.')
		return 1
	results = jira_session.get(url)
	return results.content

def command_execution(data, issue_key):
	try:
		if sys.platform == "Windows":
			batch_file = issue_key +".bat"
			startLine=""
		else:
			batch_file = issue_key +".sh"
			startLine="#!/bin/bash"
		if os.path.isfile(batch_file):
			os.remove(batch_file)
		fh = open(batch_file, "w")
		fh.writelines(startLine.replace('\r\n', os.linesep))
		fh.writelines("\n")
		fh.writelines(data.replace('\r\n', os.linesep))
		fh.close()
		os.chmod(batch_file,0777)
		command = os.path.join(os.getcwd(),batch_file)
		cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output, err = cmd_execution.communicate()
		print output
		print "Error is:",err
		print cmd_execution.returncode
		if cmd_execution.returncode != 0:
			print "Command Executed: [%s]" % command
			print "Execution ERROR: \n",err
			output = err + "[TestCase FAILED]"
			print "=============%s CommandExecution Ends Status: [%s]======================" % (command, 'FAILED')
			return output
		else:
			print "Command Executed: [%s]" % command
			output = output + "[TestCase PASSED]"
			print "=============%s CommandExecution Ends Status: [%s]======================" % (command, 'PASSED')
			return output
	except IOError, e:
		print "ERROR: ", str(e)

class JiraRestInterface(RestAPIBase):
	scopeList = []
	execTypeList = []

	def __init__(self, server, user,  password):
		super(JiraRestInterface, self).__init__(server, user, password)
		self.server = server
		self.user = user
		self.password = password
		self.tcdict = {}
		self.timedict = {}
		print "Creating Jira Object"
		self.interface_obj = JIRA(options={'server' : self.server},basic_auth =(self.user, self.password))

	def pull_testCases(self, searchString, testInput=None, TAG=None):
		projects=self.interface_obj.projects()
		keys = sorted([project.key for project in projects])
		self.TAG = TAG
		self.testInput = str(testInput)
		self.issue_list = []
		tmp_list = []
		full_list = []
		Arg_list = parse_args(self.testInput)
		tp_list = []
		if searchString in keys:
			self.projectName = searchString
			searching = 'project =' + self.projectName
			for iss in self.interface_obj.search_issues(searching):
				full_list.append(iss.key)
		else:
			storyName = searchString
			self.projectName = storyName.split("-")[0]
			issue_obj = self.interface_obj.issue(storyName)
			if issue_obj.fields.subtasks:
				for iss in issue_obj.fields.subtasks:
					full_list.append(iss.key)
			else:
				full_list.append(issue_obj.key)
		if testInput == "ALL" or testInput == None:
			tp_list = full_list
		else:
			for i in Arg_list:
				issue = self.projectName + "-" + str(i)
				tmp_list.append(issue)
			tp_list= set(full_list) & set(tmp_list)
		for issue in tp_list:
			issue_obj = self.interface_obj.issue(issue)
			if self.TAG !=None:
				if self.TAG in JiraRestInterface.scopeList:
					for t in issue_obj.fields.labels:
						if t == self.TAG:
							self.scope = self.TAG
							self.issue_list.append(issue_obj)
							break
				else:
					print "Invalid Scope mentioned"
					print "Exiting......"
					sys.exit(1)
			else:
				self.issue_list.append(issue_obj) 
		return self.issue_list

	def execute_testCases(self, issueList,attScript=None):
		import collections
		import os
		import time
		if isinstance(issueList,collections.Iterable) == False:
			issueList=[issueList]
		self.logFiles = []
		issue_list=[issueList]
		for self.response in issueList:
			start_time=time.time()
			if self.response.fields.attachment != None:
				TAG=self.response.fields.labels
				for attachment in self.response.fields.attachment:
					fName=str(attachment.filename)
					if "TestCase" in fName:
						id=attachment.id
						filename=attachment.filename
				downloadurl="https://amdjira1.atlassian.net/secure/attachment/%s/%s"%(id,filename)
				data=get_data(downloadurl,self.user,self.password)
				for tag in self.response.fields.labels:
					if tag in JiraRestInterface.execTypeList:
						if tag == "TEST_EGVDK_TCEXECTYPE_ATT":
							if attScript != None:
								if os.path.isfile("TestCase.att"):
									os.remove("TestCase.att")
								attFile=open("TestCase.att","w")
								attFile.writelines(data)
								attFile.close()
								data = "%s -s TestCase.att"%(attScript)
								self.tcdict[self.response.key] = command_execution(data, self.response.key)
							else:
								print "Please provide ATT script file as input to iexecutor"
								sys.exit(1)
						elif tag == "TEST_EGVDK_TCEXECTYPE_MANUAL":
							print "\nThis is Manual TestCase. Need to execute it manually."
							print "\nSkipping the testCase execution"
							continue
						elif tag == "TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION":
							print "\nThis testCase is GUI Automation TestCase"
							print "\n skipping execution"
							continue
						elif tag == "TEST_EGVDK_TCEXECTYPE_TXT":
							print "Executing TestCase by parsing the txt file"
							self.tcdict[self.response.key] = command_execution(data, self.response.key)
						else:
							print "Invalid Execution Type mentioned.."
							print "Exiting....."
							sys.exit(1)
						end_time=time.time()
						self.timedict[self.response.key] = (end_time-start_time)
		return self.tcdict

	def push_testResults(self, tc_dict):
		import time
		import sys
		import csv
		import shutil
		time_stamp = time.time()
		projectName=self.projectName
		scope=self.scope
		patrn="%s_%s_%s_Run"%(projectName,self.scope,time_stamp)
		release="3.0"
		totalTests=0
		passCount=0
		failCount=0
		for tc_id, result in tc_dict.items():
			for tcid,time in self.timedict.items():
				if tc_id == tcid:
					execTime = time
			try:
				totalTests+=1
				if sys.platform == "Windows":
					logDir="%s\%s\\"%(os.getcwd(),patrn)
					logfile = "%s%s-%s.log"%(logDir,tc_id,patrn)
				else:
					logDir="%s/%s/"%(os.getcwd(),patrn)
					logfile = "%s%s-%s.log"%(logDir,tc_id,patrn)
				#attachment = "%s-%s.log"%(tc_id,patrn)
				if not os.path.exists(logDir):
					os.makedirs(logDir)
				if "[TestCase PASSED]" in result:
					cmnt="%s:[TestCase PASSED] \n EXECUTION_TIME:[%s sec]"%(patrn,execTime)
					Result="PASS"
					passCount+=1
				else:
					cmnt ="%s:[TestCase FAILED] \n EXECUTION_TIME:[%s sec]"%(patrn,execTime)
					Result="FAIL"
					failCount+=1
				fh = open(logfile, "w")
				fh.writelines(result)
				fh.close()
				issue_obj = self.interface_obj.issue(tc_id)
				print logfile
				print logDir
				print logfile.split(logDir)[1]
				self.interface_obj.add_attachment(tc_id,logfile,logfile.split(logDir)[1])
				#self.interface_obj.add_attachment(tc_id,logfile,attachment)
				comment = self.interface_obj.add_comment(tc_id,cmnt)
			except Exception as e:
				sys.stderr.write('ERROR: %s \n' % e)
				sys.exit(2)
			print "===================================\n"
			print "Testcase Attchment updated"
			print "Issue: %s  logfile: %s" % (tc_id, logfile)
			print "===================================\n"
		print "Test Execution Summary"
		print "Total Tests Executed:",totalTests
		print "Total Tests Passed:",passCount
		print "Total Tests Failed:",failCount
		print "======================================"

	def ipuller_logs_from_string(self,jira_obj,project,string):
		import sys
		import os
		import csv
		self.interface_obj = jira_obj
		self.project = project
		#resultLoc=JiraRestInterface.PERFLAB_LOCATION
		fDict={}
		issueList=[]
		searchString=string
		ResultFile="Result_Summary.csv"
		csvFile=open(ResultFile,"w")
		fieldnames = ['TestCaseId', 'Result', 'ResultFile']
		writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
		writer.writeheader()
		TotalCount=0
		passCount=0
		failCount=0
		issueList=self.ipuller_issues_from_prjct_or_story_id(jira_obj,self.project)
		for issue in issueList:
			if issue.fields.comment.comments != None:
				for comment in issue.fields.comment.comments:
					if searchString in comment.body:
						res_file="%s-%s.log"%(issue.key,searchString)
						TotalCount+=1
						if comment.body.find("[TestCase PASSED]") != -1:
							passCount+=1
							Result="PASS"
						else:
							failCount+=1
							Result="FAIL"
						#if comment.body.split(":")[1] == "[TestCase PASSED]":
						#	passCount+=1
						#	Result="PASS"
						#else:
						#	failCount+=1
						#	Result="FAIL"
						fDict[issue.key] = Result
						writer.writerow({'TestCaseId': issue.key,'Result': Result, 'ResultFile': res_file})
						break
		print "====================================="
		print "Test Execution Summary"
		print "Total Tests Executed:",TotalCount
		print "Total Tests Passed:",passCount
		print "Total Tests Failed:",failCount
		print "Summary Dict:",fDict
		print "Please find the %s file for detailed report,which is placed in local Folder"%(ResultFile)
		print "======================================"

									
							
