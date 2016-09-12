'''
Created on Dec 23, 2015

@author: ppremkum
'''

from JIRAExtension.JiraRestInterface import JiraRestInterface

import csv
from datetime import date, timedelta
from time import strftime
import platform
import os
import sys
from core import userName, passwd, QAAUTOMATIONPYFX_JIRA_URL
#Inherited class from the JiraRestInterface.Generates report of execution based on inputs.
class TestReportViewer(JiraRestInterface):
    #Constructor menthod for initializing variables.
    def __init__(self,  server, user, password):
        super(TestReportViewer, self).__init__(server, user, password)
        """Return a new Jira object."""
        self.server = server
        self.user = userName
        self.password = passwd
    
def main(arguments):
    import re
    global uniqueId
    uniqueId = None
    if type(arguments) is list:
        args = arguments[0].split(" ")
    else:
        args = arguments.split(" ")
    i = 0
    edDate = None
    scope = None
    project = None
    stDate = None
    #Argument parsing and assigning it to the variables.
    for arg in args:
        if arg == '-p' or arg == '--project':
            project = args[i+1]
        elif arg == '-s' or arg == '--scope':
            scope = args[i+1]
        elif arg == '-sd' or arg == '--startDate':
            stDate = args[i+1]
        elif arg == '-ed' or arg == '--endDate':
            edDate = args[i+1]
        elif arg == '':
            i+=1
        else:
            i+=2
    #Exits if project name/scope/startdate is not mentioned.
    if (project == None) or (scope == None) or (stDate == None):
        print ("Invalid Arguments mentioned")
        print ("please specify the proper values")
        print ("-p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
        print ("End Date is not mandatory")
        sys.exit(1)
    scpe = []
    #Append the scopes when more than 1 scope is mentioned.
    if scope.find(",") != -1:
        scpe = scope.split(",")
    else:
        scpe.append(scope)
    #Summary csv file creation based on OS.
    QAAUTOMATIONPYFX_UNIQUE_EXEC_START_DATE = "%s_%s_%s"%(project,"_".join(scpe),stDate)
    print ("Here I'm in JiraRestInterface 3: " + QAAUTOMATIONPYFX_UNIQUE_EXEC_START_DATE)
    if platform.system() == "Windows":
        from core import QAAUTOMATIONPYFX_WIN_WORKSPACE
        ResultFile = QAAUTOMATIONPYFX_WIN_WORKSPACE + "\\" + QAAUTOMATIONPYFX_UNIQUE_EXEC_START_DATE + "\\" + "Result_Summary.csv"
    elif platform.system() == "Linux":
        from core import QAAUTOMATIONPYFX_LINUX_WORKSPACE
        ResultFile = QAAUTOMATIONPYFX_LINUX_WORKSPACE + "/" + QAAUTOMATIONPYFX_UNIQUE_EXEC_START_DATE + "/" + "Result_Summary.csv"
    from core import EXEC_QA_STORY
    execQaStry = EXEC_QA_STORY
    #Check for the directory existence and create if not exist.
    if  (os.path.isdir(ResultFile.split("Result_Summary.csv")[0])) != True:
        os.makedirs(ResultFile.split("Result_Summary.csv")[0])
    csvFile = open(ResultFile, "w")
    fieldnames = ['UNIQUEID','TestcaseId', 'Result', 'ResultFile']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
    writer.writeheader()
        
    TotalCount = 0
    passCount = 0
    failCount = 0
    #Creating jira object and checking if projectname passed is valid or not.
    test = TestReportViewer(QAAUTOMATIONPYFX_JIRA_URL, userName, passwd)
    projects = test.interface_obj.projects()
    keys = sorted([prjct.key for prjct in projects])
    if project in keys:
        print ("Valid ProjectName mentioned.. Continuing")
    else:
        print ("Invalid Project name mentioned Exiting....")
        sys.exit(1)
    #if scpe != None:
        #uniqueId = "%s_.*%s.*"%(project,scope)
        #uniqueId = "%s_%s"%(project,"_".join(scpe))
    #else:
    #    uniqueId = project
    #Converting start date and end date passed to python readable format.
    st_list = stDate.split("-")
    startDate = date(int(st_list[0]),int(st_list[1]),int(st_list[2]))
    if edDate != None:
        et_list = edDate.split("-")
        endDate = date(int(et_list[0]),int(et_list[1]),int(et_list[2]))
    else:
        endDate = date.today()
    day_count = (endDate - startDate).days + 1
    #Creating execution history object to get the list of runs executed.
    execQaStory = test.interface_obj.issue(execQaStry,expand='changelog')
    totalIssues = []
    #getting the subtasks list which are created > start date.
    search_query = "parent in (%s) AND created >= %s"%(execQaStory.key,startDate)
    #Getting the final issue list based on search_query(startdate, projectname and scope)
    for subtask in test.interface_obj.search_issues(search_query, maxResults=-1, expand='changelog'):
        print("Getting the info from the subtask:",subtask.key)
        sbtask= test.interface_obj.issue(subtask.key,expand='changelog')
        for single_date in [d for d in (startDate + timedelta(n) for n in range(day_count)) if d <= endDate]:
            finalDate = strftime("%Y-%m-%d", single_date.timetuple())
            if len(scpe) == 1:
                uniqueId = "%s_.*%s.*"%(project,scpe[0])
            else:
                uniqueId = "%s_%s"%(project,"_".join(scpe))
            searchString = "%s_%s"%(uniqueId,finalDate)
            #Getting the issue list from the comment of execution QA history.This list will be union of all runs.
            prog = re.compile(searchString)
            if prog.search(sbtask.fields.summary):
                for cmt in sbtask.fields.comment.comments:
                    totalIssues.extend(cmt.body.strip("[]").split(", "))
            else:
                scpe.reverse()
                if len(scpe) == 1:
                    uniqueId = "%s_.*%s.*"%(project,scpe[0])
                else:
                    uniqueId = "%s_%s"%(project,"_".join(scpe))
                searchString = "%s_%s"%(uniqueId,finalDate)
                prog = re.compile(searchString)
                if prog.search(sbtask.fields.summary):
                    for cmt in sbtask.fields.comment.comments:
                        totalIssues.extend(cmt.body.strip("[]").split(", "))
                else:
                    scpe.reverse()
                    if len(scpe) == 1:
                        uniqueId = "%s_.*%s.*"%(project,scpe[0])
                    else:
                        uniqueId = "%s_%s"%(project,"_".join(scpe))
    print(totalIssues)
    totalIssues = list(set(totalIssues))
    print(totalIssues)

    dupList = []
    #For loop check the search string ineach and every test case issue and writes the result into csv file if matches.
    for issuekey in totalIssues:
        if issuekey.find("u") != -1:
            issue = test.interface_obj.issue(issuekey.split("u'")[1].strip("'"),expand='changelog')
        else:
            issue = test.interface_obj.issue(issuekey.split("'")[1],expand='changelog')
        if issue.key not in dupList:
            dupList.append(issue.key)
        else:
            print("This test Case is duplicate.. so Skipping the execution of this test")
            continue
        if issue.fields.comment.comments != None:
            for comment in issue.fields.comment.comments:
                m = re.compile(uniqueId)
                if m.match(comment.body):
                    day_count = (endDate - startDate).days + 1
                    for single_date in [d for d in (startDate + timedelta(n) for n in range(day_count)) if d <= endDate]:
                        finalDate = strftime("%Y-%m-%d", single_date.timetuple())
                        searchString = "%s_%s"%(uniqueId,finalDate)
                        m = re.compile(searchString)
                        if m.match(comment.body):
                            string = "%s.*T\d{2}-\d{2}-\d{2}.\d{1,8}"%(searchString)
                            regex=re.compile(string)
                            m = regex.search(comment.body)
                            if m:
                                QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID = str(m.group())
                            else:
                                QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID = searchString
                            from core import QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL
                            res_file = "%s-%s_Run.log"%(issue.key,QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                            for attachment in issue.fields.attachment:
                                fName=str(attachment.filename)
                                if res_file == fName:
                                    attachmentId = attachment.id
                                    filename = attachment.filename
                            downloadurl = QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL + "/%s/%s"%(attachmentId, filename)               
                            TotalCount += 1
                            if comment.body.find("[Testcase PASSED]") != -1:
                                passCount+=1
                                Result="PASS"
                            else:
                                failCount+=1
                                Result="FAIL" 
                            writer.writerow({'TestcaseId': issue.key,'Result': Result, 'ResultFile': downloadurl, 'UNIQUEID':QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID})
    csvFile.close()           
               
    print ("=====================================")
    print ("Test Execution Summary")
    print ("Total Tests Executed:", TotalCount)
    print ("Total Tests Passed:", passCount)
    print ("Total Tests Failed:", failCount)
    print ("For detailed Report Please find the ResultFile:%s"%(ResultFile))

if (__name__ == "__main__"):
    ret = main(sys.argv[1:])
    sys.exit(ret)
