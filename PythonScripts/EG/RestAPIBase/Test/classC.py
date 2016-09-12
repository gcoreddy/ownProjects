#!/usr/bin/env python
from classA import ClassA
from classB import ClassB

class ClassD(ClassA,ClassB):
	def __init__(self, tcExecType):
		super(ClassD, self).__init__(tcExecType)
			
	def ExecLogic(self):
		print "Execution from overloading method"
		print self.tcExecType

	def tokka(self):
		d = ClassA("EG-46")
		d.Run()	
		

e = ClassD("TC_EXEC_TYPE_TXT")
e.tokka()
