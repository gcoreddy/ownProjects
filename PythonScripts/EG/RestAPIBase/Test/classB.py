#!/usr/bin/env python

class ClassB(object):
	def __init__(self,ExecType):
		self.ExecType = ExecType 

	def ExecLogic(self):
		print "Execution Logic menthod calling"
		print self.ExecType
