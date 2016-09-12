'''
Created on Dec 8, 2015

@author: ppremkum
'''
#!/usr/bin/env python
from core.ExecutionLogic import ExecutionLogic
#This class defines the test case with exectype, description etc.
class Testcase(object):
    #Constructor method to initialize all the variables.
    def __init__(self, testcase, exec_obj):
        self.testcase = testcase
        self.tcExecType = None
        self.attachments = []
        self.tcId = None
        self.tcDesc = None
        self.exec_obj = exec_obj
    #execLogic menthod creates and invokes the actual run method from executionLogic.
    def execLogic(self):
        self.tcId = self.testcase.key
        self.tcDesc = self.testcase.fields.description
        #Searching for the TCEXECTYPE in all the labels from the test case and assigning it to the tcExecType variable. Test case will be invoked according to the execType. 
        for eType in self.testcase.fields.labels:
            if eType.find("TCEXECTYPE") != -1:
                self.tcExecType = eType
            else:
                continue
        #If test execution type if not found in the label, that test case will be skipped from execution. 
        if self.tcExecType == None:
            import sys
            print ("Test Execution Type is not mentioned in the test case")
            print ("Exiting ......")
            sys.exit(1)
        
        execCmd = ExecutionLogic(self.tcExecType,self.testcase,self.exec_obj)
        return  execCmd.run()
