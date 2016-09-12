#!/usr/bin/env python
import sys
import os

class TestCase(object):
	def __init__(self, testCase):
		self.testCase = testCase
		self.tcExecType = None
		self.attachments = []
		self.tcId = None
		self.tcDesc = None

	def run(self):
			
	def createTestConfig(self):
		self.tcId = self.testCase.key
		self.tcDesc = self.testCase.fields.description
		self.attachments = self.testCase.fields.attachment
		for eType in self.testCase.fields.labels:
			if eType.contains("TCEXECTYPE"):
				self.tcExecType = eType
