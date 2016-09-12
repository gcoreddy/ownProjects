#!/usr/bin/env python
'''
Created on Dec 8, 2015

@author: ppremkum
'''
from core.RestAPIBase import RestAPIBase
from JIRAExtension.JiraTestcase import Testcase
from jira.client import JIRA    
#Implementor class for RestApiBase.This contains actual implementation code for the methods defined in the RestApiBase class.
class JiraRestInterface(RestAPIBase):
    tc_dict = {}
    #Initializing all the variables based on values mentioned in the core module and also defining some default variables for later usage.
    def __init__(self, server, user, password):
        
        super(JiraRestInterface, self).__init__(server, user, password)
        self.server = server
        self.user = user
        self.password = password
        self.tcdict = {}
        self.timedict = {}
        self.xmltcDict = {}
        self.xmltimeDict = {}
       
        #Creating JIRA object using user name and password initialized in the constructor. 
        print ("Creating Jira Object")
        self.interface_obj = JIRA(options = {'server' : self.server}, basic_auth = (self.user, self.password))
    
    #Parsing the inputs passed to the range option and creating a list based on input.
    def parse_args(self, TestListRange):
        Tests = []
        FinalList = []
        if TestListRange.find(",") != -1:
            Tests = TestListRange.split(",")
            for test in Tests:
                if test.find("-") != -1:
                    temp = test.split("-")
                    FinalList.extend(range(int(temp[0]), int(temp[1]) + 1))
                else:
                    FinalList.append(int(test))
        elif TestListRange.find("-") != -1:
            temp = TestListRange.split("-")
            FinalList.extend(range(int(temp[0]), int(temp[1]) + 1))
        elif TestListRange == "ALL" or TestListRange == "all":
            FinalList.append(TestListRange)
        else:
            FinalList.append(int(TestListRange))
        return FinalList
           
    #pull_testcases method return the actual list of test cases to be executed based on inputs provided(range, scope, project).
    def pull_testcases(self, searchString, testInput=None, TAG=None):
        import sys
        import datetime
        #Getting the total projects available in the jira and adding them into a list.
        projects = self.interface_obj.projects()
        keys = sorted([project.key for project in projects])
        self.TAG = []
        #Check for the scope option.Split the values pnd assign it to a tuple, when more than 1 value mentioned as a input to the scope option.
        if TAG.find(",") != -1:
            self.TAG = TAG.split(",")
        else:
            self.TAG.append(TAG)
        print(self.TAG)
        if len(self.TAG) == 1:
            tag = "(%s)"%(self.TAG[0])
        else:
            tag = tuple(self.TAG)
        self.testInput = str(testInput)
        self.issue_list = []
        full_list = []
        Arg_list = self.parse_args(self.testInput)
        print(sorted(Arg_list))
        tp_list = []
        #Checking whether project name mentioned exists in the jira or not.
        if searchString in keys:
            self.projectName = searchString
            print ("Project \"%s\" found!"%self.projectName)
            searching = 'project = ' + self.projectName
            search_query = "%s and labels IN %s"%(searching,tag)
            print(search_query)
            print("Getting the issue list from projectId")
#            if Arg_list[0] == "ALL" or Arg_list[0] == "all": 
#                strtAt = 0
#            else:
#                strtAt = 0
#            full_list.extend(self.interface_obj.search_issues(search_query,startAt=strtAt, maxResults=-1, expand='changelog'))
            #Getting the full list of tests based on search query in the project mentioned.
            full_list.extend(self.interface_obj.search_issues(search_query,startAt=0, maxResults=-1, expand='changelog'))
        else:
            try:
                storyName = searchString
                self.projectName = storyName.split("-")[0]
                issue_obj = self.interface_obj.issue(storyName, expand='changelog')
                search_query = "status in ('Open') AND parent in (%s) and labels IN %s"%(storyName,tag)
                if issue_obj.fields.subtasks:
                    full_list.extend(self.interface_obj.search_issues(search_query, maxResults=-1, expand='changelog')) 
                else:
                    full_list.append(issue_obj)
            except:
                print ("Project or Story name does not exist or there is insufficient access permission")
                sys.exit(1)
        
        time_stamp = datetime.datetime.now()
        #Assiging/Creating UNIQUE string based on all inputs(project and scope and time stamp), to differentiate between different runs.
        self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID = "%s_%s_%s_Run"%(self.projectName, "_".join(self.TAG), str(time_stamp.isoformat()).replace(":","-"))
        print (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
       
        #Creating final list of tests to be executed based on range mentioned. 
        if testInput == "ALL" or testInput == None:
            tp_list = full_list
        else:
            for i in Arg_list:
                print ("Searching for \"%s-%s\"" % (self.projectName, i))
                issue = self.projectName + "-" + str(i)
                for isue_obj in full_list:
                    if isue_obj.key == issue:
                        tp_list.append(isue_obj)
        self.issue_list = tp_list

    #execute_testcases method executes the tests and returns the output for each and every test case and writes the test summary into the csv file.
    def execute_testcases(self, exec_obj):
        import collections
        import time
        import platform
        import csv
        import os
        import errno
        
        totalTests = 0
        passCount = 0
        failCount = 0
        notRunCount = 0
       
        #Assiging the csv file variable with proper values based on OS. 
        if platform.system() == "Windows":
            from core import QAAUTOMATIONPYFX_WIN_WORKSPACE
            ResultFile = QAAUTOMATIONPYFX_WIN_WORKSPACE + "\\" + self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "\\" + "Result_Summary.csv"
        elif platform.system() == "Linux":
            from core import QAAUTOMATIONPYFX_LINUX_WORKSPACE
            ResultFile = QAAUTOMATIONPYFX_LINUX_WORKSPACE + "/" + self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "/" + "Result_Summary.csv"
        
        try:
            os.makedirs(os.path.dirname(ResultFile))
        except OSError as ex:  # Python version above 2.5
            if ex.errno == errno.EEXIST and os.path.isdir(os.path.dirname(ResultFile)):
                pass
            else:
                raise
        #Opening a csv file in write mode for summary generation. 
        csvFile = open(ResultFile, "w")
        fieldnames = ['TestcaseId', 'Result', 'ResultFile', 'Error', 'Time', 'UNIQUEID']
        self.writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
        self.writer.writeheader()
        
        print ("Executing tests with Unique InstanceId:", self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
        #Converting issue list into a list if single testcase mentioned.
        if isinstance(self.issue_list, collections.Iterable) == False:
            issueList = [self.issue_list]
        else:
            issueList = self.issue_list
        
        self.logFiles = []
        self.exec_obj = exec_obj
        print ("Getting the QA story object:",JiraRestInterface.execQAStory)
        #Creating QA story object to write the summary of execution for the prticular run.
        self.execQaStory_obj = self.interface_obj.issue(str(JiraRestInterface.execQAStory), expand='changelog')
        try:
            JiraRestInterface.description
        except:
            JiraRestInterface.description = "Test Cycle Unique Id:%s" % (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
        summary = "Test Cycle Unique Id:%s" % (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
        subtsk_dict = {
                       'project' : { 'key': self.projectName },
                       'summary' : summary,
                       'description' : JiraRestInterface.description ,
                       'issuetype' : { 'name' : 'Sub-task' },
                       'parent' : { 'id' : self.execQaStory_obj.key },
                       'components' : [{'name':"QA"}],
                       'customfield_12610': { "value" : 'Low' , "id" : '13917' } 
                       }
        print("Creating subtask QaExecStory")
        #Creating the subtask in the QAExecStory to update the summary of the perticular run.
        sbtsk = self.interface_obj.create_issue(fields=subtsk_dict)
        execTestList = []
        failTestList = []
        if len(issueList) == 0:
            import sys
            print("No issues found with the scope mentioned..... exiting")
            print("Please mention the valid scope")
            sys.exit(1)
        for self.response in issueList:
            print ("Executing Testcase:", self.response)
            totalTests+=1
            self.response = self.interface_obj.issue(self.response.key,expand='changelog')
            start_time = time.time()
            execTest = Testcase(self.response, self.exec_obj)
            result = execTest.execLogic()
            end_time = time.time()
            execTime = (end_time - start_time)
            self.timedict[self.response.key] = execTime
            self.xmltimeDict[self.response.key] = execTime
            if result != 1:
                self.tcdict[self.response.key] = result
                self.xmltcDict[self.response.key] = result
                execTestList.append(self.response.key)
                if result.find(b"[Testcase PASSED]") != -1:
                    passCount+=1
                    self.writer.writerow({'TestcaseId': self.response.key, 'Result': 'PASS'})
                elif result.find(b"[Testcase FAILED]") != -1:
                    failCount+=1
                    self.writer.writerow({'TestcaseId': self.response.key, 'Result': 'FAIL', 'Error': result})
                elif result.find(b"[Testcase NOTRUN]") != -1:
                    if self.response.key in failTestList:
                        notRunCount+=1
                        print("Not run tests failed in retry also.... Marking them as Not run")
                        self.writer.writerow({'TestcaseId': self.response.key, 'Result': 'NOTRUN', 'Error': result})
                    else:
                        print("Retrying to execute the Not run tests......")
                        totalTests-=1
                        issueList.append(self.response)
                        failTestList.append(self.response.key)
                        self.tcdict.clear()
                        self.timedict.clear()
                        continue
                self.push_testResults()
                self.timedict.clear()
                self.tcdict.clear()
            else:
                print("Test Execution Type is not mentioned in the test case...skip the execution")
                continue
        #Updating the result as comment in the jira.
        self.interface_obj.add_comment(sbtsk, str(execTestList))
        csvFile.close()
        #Creating XML file for jenkins purpose with the result summary.
        import xml.etree.cElementTree as ET
        from core import QAAUTOMATIONPYFX_XML_FILE
        import os
        root = ET.Element("testsuites", disabled="0", errors=str(notRunCount), failures=str(failCount), name=self.projectName, tests=str(totalTests) )
        tc = {}
        tme = 0
        nodeName = os.getenv("THIS_NODE")
        if nodeName == None:
            nodeName = platform.node()
        tmestamp = self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID.split("_")[-2].split(".")[0]
        clsName = "%s.%s"%(self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID.split(tmestamp)[0].strip("_"),nodeName)
        for t in self.xmltimeDict.values():
            tme+=t
        doc = ET.SubElement(root, "testsuite", disabled="0", errors=str(notRunCount), failures=str(failCount), hostname=platform.node(), id=self.projectName, name=self.projectName, skipped=str(tme), tests=str(totalTests), time="100", timestamp=tmestamp)
        i = 0
        for tst in self.xmltcDict.keys():
            if self.xmltcDict[tst].find(b"[Testcase PASSED]") != -1:
                tc[i] = ET.SubElement(doc, "testcase", classname=clsName,name=tst,time=str(self.xmltimeDict[tst]),status="PASS")
                #ET.SubElement(tc[i], "system-out").text = str(self.xmltcDict[tst])
                ET.SubElement(tc[i], "system-out").text = "[Testcase PASSED]"
            elif self.xmltcDict[tst].find(b"[Testcase FAILED]") != -1:
                tc[i] = ET.SubElement(doc, "testcase", classname=clsName,name=tst,time=str(self.xmltimeDict[tst]),status="FAIL")
                ET.SubElement(tc[i], "error",message=str(self.xmltcDict[tst]), type="exception").text = str(self.xmltcDict[tst])
            else:
                tc[i] = ET.SubElement(doc, "testcase", classname=clsName,name=tst,time=str(self.xmltimeDict[tst]),status="NOTRUN")
                ET.SubElement(tc[i], "error",message=str(self.xmltcDict[tst]), type="exception").text = str(self.xmltcDict[tst])
            i+=1
        tree = ET.ElementTree(root)
        xmlF = "%s_%s.xml"%(os.path.basename(QAAUTOMATIONPYFX_XML_FILE).split(".")[0],nodeName)
        xmlFile = os.path.join(os.path.dirname(QAAUTOMATIONPYFX_XML_FILE),xmlF)
        #tree.write(QAAUTOMATIONPYFX_XML_FILE)
        tree.write(xmlFile)
        print(os.getcwd())
        print ("Test Execution Summary")
        print ("Total Tests Executed:", totalTests)
        print ("Total Tests Passed:", passCount)
        print ("Total Tests Failed:", failCount)
        print ("Total Tests NotRun:", notRunCount)
        print ("======================================")

    #push_testResults method is used to update the results in the jira. 
    def push_testResults(self):
        import os
        import time
        import platform
        for tc_id, result in self.tcdict.items():
            for tcid, time in self.timedict.items():
                if tc_id == tcid:
                    execTime = time
            #Creating the log file based on various unique params.
            from core import QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID
            print ("Here I'm in JiraRestInterface 2: " + self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
            if platform.system() == "Windows":
                from core import QAAUTOMATIONPYFX_WIN_WORKSPACE
                logDir = "%s\\%s\\" % (QAAUTOMATIONPYFX_WIN_WORKSPACE, self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                logfile = "%s%s-%s.log" % (logDir, tc_id, self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
            elif platform.system() == "Linux":
                from core import QAAUTOMATIONPYFX_LINUX_WORKSPACE
                logDir = "%s/%s/" % (QAAUTOMATIONPYFX_LINUX_WORKSPACE, QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                logfile = "%s%s-%s.log" % (logDir, tc_id, self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                
            if not os.path.exists(logDir):
                os.makedirs(logDir)
                
            if b"[Testcase PASSED]" in result:
                cmnt = "%s:[Testcase PASSED] \n EXECUTION_TIME:[%s sec]" % (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID, str(execTime))
            elif b"[Testcase FAILED]" in result:
                cmnt = "%s:[Testcase FAILED] \n EXECUTION_TIME:[%s sec]" % (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID, str(execTime))
            elif b"[Testcase NOTRUN]" in result:
                cmnt = "%s:[Testcase NOTRUN] \n EXECUTION_TIME:[%s sec]" % (self.QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID, str(execTime))
            #Writing the result into the log file and attaching the log file to the issue/Testcase in jira.Updates the comment as well.
            fh = open(logfile, "w")
            fh.writelines(str(result))
            fh.close()                
            self.interface_obj.add_attachment(tc_id, logfile, logfile.split(logDir)[1])
            comment = self.interface_obj.add_comment(tc_id, cmnt)
            print ("Added Comment \"" + comment.__str__() + "\" to TestcaseId: " + tc_id)
            print ("===================================\n")
            print ("Testcase Attchment updated")
            print ("Issue: %s  logfile: %s" % (tc_id, logfile))
            print ("===================================\n")
