#!/usr/bin/env python
from ExecutionLogic import ExecutionLogic
class EGExecLogic(ExecutionLogic):
	user = None
	password = None
	def __init__(self):
		print "init function"
													
	def get_data(self, downloadurl):
		import requests
		list=[]
		jira_session = requests.session()
		try:
			jira_session.post('https://amdjira1.atlassian.net', auth=(EGExecLogic.user, EGExecLogic.password), verify=False)
		except:
			print('Unable to connect or authenticate with JIRA server.')
			sys.exit(1)
		results = jira_session.get(downloadurl)
		return results.content
	
	def run(self,tcExecType,testCase):
		import sys
		import os
		self.tcExecType = tcExecType
		self.testCase = testCase
		if self.testCase.fields.attachment != None:
			for attachment in self.testCase.fields.attachment:
				fName=str(attachment.filename)
				if "TestCase" in fName:
					id = attachment.id
					filename = attachment.filename
			downloadurl = "https://amdjira1.atlassian.net/secure/attachment/%s/%s"%(id,filename)
			data = self.get_data(downloadurl)
			if self.tcExecType == "TEST_EGVDK_TCEXECTYPE_ATT":
				attScript = os.getenv("ATT_SCRIPT_FILE")
				if attScript != None:
					if os.path.isfile("TestCase.att"):
						os.remove("TestCase.att")
					attFile=open("TestCase.att","w")
					attFile.writelines(data)
					attFile.close()
					data = "%s -s TestCase.att"%(attScript)
					return data
				else:
					print "Please provide att script file path"
					print "Please export the ATT_SCRIPT_FILE environment variable before running the script"
					sys.exit(1)
			elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_MANUAL":
				print "\nThis is Manual TestCase. Need to execute it manually."
				print "\nSkipping the testCase execution"
			elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION":
				print "\nThis testCase is GUI Automation TestCase"
				print "\n skipping execution"
			elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_TXT":
				print "Executing TestCase by parsing the txt file"
				return data
			else:
				print "Invalid Exec Type"
				sys.exit(1)
