#!/usr/bin/env python
from RestAPIBase import RestAPIBase
from JiraTestCase import TestCase
from jira.client import JIRA


class JiraRestInterface(RestAPIBase):
	tc_dict = {}
	scopeList = []
	execTypeList = []

	def __init__(self, server, user,  password):
		import csv
		import time
		super(JiraRestInterface, self).__init__(server, user, password)
		self.server = server
		self.user = user
		self.password = password
		self.tcdict = {}
		self.timedict = {}
		print "Creating Jira Object"
		self.interface_obj = JIRA(options={'server' : self.server},basic_auth =(self.user, self.password))
		ResultFile="Result_Summary_%s.csv"%(time.time())
		csvFile=open(ResultFile,"w")
		fieldnames = ['TestCaseId', 'Result', 'ResultFile', 'Error']
		self.writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
		self.writer.writeheader()


	def parse_args(self,TestListRange):
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
			
	def pull_testCases(self, searchString, testInput=None, TAG=None):
		import sys
		projects=self.interface_obj.projects()
		keys = sorted([project.key for project in projects])
		self.TAG = TAG
		self.testInput = str(testInput)
		self.issue_list = []
		tmp_list = []
		full_list = []
		Arg_list = self.parse_args(self.testInput)
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
		print tp_list
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
		print self.issue_list

	def execute_testCases(self, exec_obj):
		import collections
		import os
		import time
		import sys
		if isinstance(self.issue_list,collections.Iterable) == False:
			issueList=[self.issue_list]
		else:
			issueList=self.issue_list
		self.logFiles = []
		self.exec_obj = exec_obj
		for self.response in issueList:
			print "Executing TestCase:",self.response
			start_time=time.time()
			execTest = TestCase(self.response, self.exec_obj)
			result = execTest.execLogic()
			self.tcdict[self.response.key] = result
			if result.find("[TestCase PASSED]") != -1:
				self.writer.writerow({'TestCaseId': self.response.key,'Result': 'PASS'})
			else:
				self.writer.writerow({'TestCaseId': self.response.key,'Result': 'FAIL', 'Error': result})
			end_time=time.time()
			self.timedict[self.response.key] = (end_time-start_time)
			print self.tcdict
			print self.timedict

	def push_testResults(self):
		import os
		import time
		import sys
		import csv
		import shutil
		import platform
		time_stamp = time.time()
		projectName=self.projectName
		scope=self.scope
		patrn="%s_%s_%s_Run"%(projectName,self.scope,time_stamp)
		totalTests=0
		passCount=0
		failCount=0
		for tc_id, result in self.tcdict.items():
			for tcid,time in self.timedict.items():
				if tc_id == tcid:
					execTime = time
			try:
				totalTests+=1
				if platform.system() == "Windows":
					logDir="%s\%s\\"%(os.getcwd(),patrn)
					logfile = "%s%s-%s.log"%(logDir,tc_id,patrn)
				elif platform.system() == "Linux":
					logDir="%s/%s/"%(os.getcwd(),patrn)
					logfile = "%s%s-%s.log"%(logDir,tc_id,patrn)
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
				self.interface_obj.add_attachment(tc_id,logfile,logfile.split(logDir)[1])
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

	def pull_testResults(self,project,string):
		import sys
		import os
		import csv
		self.project = project
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
		self.pull_testCases(self.project)
		for issue in self.issue_list:
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

									
							
