#!/usr/bin/env python
import RestAPIBase
from JiraRestInterface import JiraRestInterface
from EGExecLogic import EGExecLogic


class TestUtils(JiraRestInterface,EGExecLogic):
	EGExecLogic.user = 'chandra-obul.Reddy@amd.com'
	EGExecLogic.password = 'Chandu@40689'
	JiraRestInterface.scopeList = ["TEST_SANITY","TEST_FULL"]
	JiraRestInterface.execTypeList = ["TEST_EGVDK_TCEXECTYPE_ATT","TEST_EGVDK_TCEXECTYPE_MANUAL","TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION","TEST_EGVDK_TCEXECTYPE_TXT"]
	def __init__(self,  server, user, password):
		super(TestUtils, self).__init__(server, user, password)
		"""Return a new Jira object."""
		self.server = server
		self.user = user
		self.password = password

test = TestUtils('https://amdjira1.atlassian.net/', 'chandra-obul.Reddy@amd.com', '**********')
exec_obj = EGExecLogic()
test.pull_testCases('EG',"114-123","TEST_SANITY")
test.execute_testCases(exec_obj)
test.push_testResults()
test.pull_testResults("EG","EG_TEST_SANITY_1448976500.64_Run")


