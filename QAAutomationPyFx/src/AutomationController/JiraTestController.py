'''
Created on Dec 8, 2015

@author: ppremkum
'''
#!/usr/bin/env python

#import argparse
#import datetime
import sys


from JIRAExtension.JiraRestInterface import JiraRestInterface
from JIRAExtension.EGExecutionLogic import EGExecutionLogic
from core import userName, passwd, EXEC_QA_STORY


class JiraTestController(JiraRestInterface, EGExecutionLogic):
    #Assigning username and password of jira from core module__init__ file.
    #Please fill the details of user name and password in core __init__ file
    EGExecutionLogic.user = userName
    EGExecutionLogic.password = passwd
    #This "scopeList" and "execTypeList" are for Cloud JIRA's EG project
    #JiraRestInterface.scopeList = ["TEST_SANITY","TEST_FULL"]
    #JiraRestInterface.execTypeList = ["TEST_EGVDK_TCEXECTYPE_ATT","TEST_EGVDK_TCEXECTYPE_MANUAL","TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION","TEST_EGVDK_TCEXECTYPE_TXT"]
    
    #This "scopeList" and "execTypeList" are for Cloud JIRA's SQA project with EG as the project set
    #JiraRestInterface.scopeList = ["SQA_TCSCOPE_SANITY","SQA_TCSCOPE_FULL"]
    #JiraRestInterface.execTypeList = ["SQA_EGVDK_TC", "SQA_EGVDK_TCEXECTYPE_ATT"]
    
    #This "scopeList" and "execTypeList" are for AMD JIRA's VDK project with EG as the project set
    #JiraRestInterface.scopeList = ["QA_EG_AXELL_TC","QA_EG_AXELL_TC_NONLOOP"]
    #JiraRestInterface.execTypeList = ["QA_EGVDK_TC", "QA_EGVDK_TCEXECTYPE_ATT","QA_TCEXECTYPE_SHELL"]
    
    #Assigning list of valid scope list, execution type list and execution Qa history story.
    #Need to fill these variables in the core module with proper values otherwise test will fail. 
    JiraRestInterface.execQAStory = EXEC_QA_STORY
    #JiraRestInterface.description="Please specify the description you want"
    def __init__(self,  server, user, password):
        #Creating a JIRA object based on server, user and password.
        super(JiraTestController, self).__init__(server, user, password)
        """Return a new Jira object."""
        self.server = server
        self.user = user
        self.password = password


def main(arguments):
    #Converting arguments into list and assigning it into args variable
    if type(arguments) is list:
        args = arguments[0].split(" ")
    else:
        args = arguments.split(" ")
    i = 0
    #Assigning default values, if nothing mentioned in the inputs default values will be taken.If nothing passed to range variable by default range will be set to ALL.
    testRange = "ALL"
    scope = None
    project_name = None
    #Parsing the arguments and assigning them to the variables.
    for arg in args:
        if arg == '-p' or arg == '--project':
            project_name = args[i+1]
        elif arg == '-s' or arg == '--scope':
            scope = args[i+1]
        elif arg == '-r' or arg == '--range':
            testRange = args[i+1]
        elif arg == '':
            i+=1
        else:
            i+=2

    if project_name == None or scope == None:
        print ("=======================================================")
        print ("Please mention the project name as an argument")
        print ("please specify the proper values")
        print ("-p 'projectName' -s 'scope' -r 'Range of tests'")
        print ("scope and range are not mandatory by default range value taken as ALLand scope value taken as None")
        print ("=======================================================")
        sys.exit(1)
        
    from core import QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID , QAAUTOMATIONPYFX_JIRA_URL
    print ("Running QA Automation Instance for project: \"" + project_name + "\" with Unique Instance Id: \"" + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "\"")
    
    #Creating Jira Instance by  creating object. 
    test = JiraTestController(QAAUTOMATIONPYFX_JIRA_URL, userName, passwd)
    
    #Creating executionLogic object to execute tests.
    #This execution object may vary depending upon the project. If the execution method of project changes we need to create
    #New execution logic and need to create object for that execution logic.
    try:
        exec_obj = EGExecutionLogic()
    
        #Gets the testCase list based on range, scope and project name.
        test.pull_testcases(project_name,testRange,scope)
    
        #Executes the tests and updates the test result which are pulled based on inputs. 
        test.execute_testcases(exec_obj)
    except Exception as e:
        import traceback
        print("Failed to execute the tests as Exception occured")
        print("Exception is:",e)
        traceback.print_exc()
        sys.exit(1)

if (__name__ == "__main__"):
    ret = main(sys.argv)
    sys.exit(ret)
