#!/usr/bin/env python
from classB import ClassB
class ClassA(ClassB):
	def __init__(self,tcId):
		self.tcId = tcId

	def Run(self):
		print "Execution from base class"
		c = ClassB("TC_EXECTYPE_ATT")
		c.ExecLogic()
	
	def tcDisc(self):
		print "tcDisc function"
