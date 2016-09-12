#!/usr/bin/env python
import sys
import os
from ExecutionLogic import ExecutionLogic

class TestCase(object):
	def __init__(self, testCase, exec_obj):
		self.testCase = testCase
		self.tcExecType = None
		self.attachments = []
		self.tcId = None
		self.tcDesc = None
		self.exec_obj = exec_obj

	def execLogic(self):
		self.tcId = self.testCase.key
		self.tcDesc = self.testCase.fields.description
		self.attachments = self.testCase.fields.attachment
		for eType in self.testCase.fields.labels:
			if eType.find("TCEXECTYPE") != -1:
				self.tcExecType = eType
			else:
				continue
		if self.tcExecType == None:
			import sys
			print "Test Execution Type is not mentioned in the test case"
			print "Exiting ......"
			sys.exit(1)
		execCmd = ExecutionLogic(self.tcExecType,self.testCase,self.exec_obj)
		return  execCmd.run()

