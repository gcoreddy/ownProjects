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
#Inherited class from the JiraRestInterface.Functionality of this class is to delete the older logs and comments based on inputs.
class TestReportViewer(JiraRestInterface):
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
    #Parsing the arguments
    if type(arguments) is list:
        args = arguments[0].split(" ")
    else:
        args = arguments.split(" ")
    i = 0
    edDate = None
    scope = None
    project = None
    stDate = None
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
    if (project == None) or (scope == None) or (stDate == None):
        print ("Invalid Arguments mentioned")
        print ("please specify the proper values")
        print ("-p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
        print ("End Date is not mandatory")
        sys.exit(1)
    scpe = []
    if scope.find(",") != -1:
        scpe = scope.split(",")
    else:
        scpe.append(scope)
    execQaStry = "VDK-23"
    test = TestReportViewer(QAAUTOMATIONPYFX_JIRA_URL, userName, passwd)
    projects = test.interface_obj.projects()
    keys = sorted([prjct.key for prjct in projects])
    if project in keys:
        print ("Valid ProjectName mentioned.. Continuing")
    else:
        print ("Invalid Project name mentioned Exiting....")
        sys.exit(1)
    #Changing the input dates into proper python readable formats.If end date is not mentioned, by default it takes today as end date.
    st_list = stDate.split("-")
    startDate = date(int(st_list[0]),int(st_list[1]),int(st_list[2]))
    if edDate != None:
        et_list = edDate.split("-")
        endDate = date(int(et_list[0]),int(et_list[1]),int(et_list[2]))
        edDt = date(int(et_list[0]),int(et_list[1]),int(et_list[2])+1)
    else:
        endDate = date.today()
    day_count = (endDate - startDate).days + 1
    execQaStory = test.interface_obj.issue(execQaStry,expand='changelog')
    totalIssues = []
    print(endDate)
    #Getting the issues which are updated between startdate and enddate.
    #search_query = "parent in (%s) AND created >= %s"%(execQaStory.key,startDate)
    search_query = "parent in (%s) AND created >= %s AND created <= %s "%(execQaStory.key,startDate,edDt)
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
            prog = re.compile(searchString)
            print(sbtask.fields.summary)
            print(searchString)
            #Getting the final issue list if comment has the search string.
            if prog.search(sbtask.fields.summary):
                for cmt in sbtask.fields.comment.comments:
                    totalIssues.extend(cmt.body.strip("[]").split(", "))
                    #subtask.delete()
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
                        #subtask.delete()
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
    #Check if comment matches with the start date or end date and delete the comment and log file from the jira issue.
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
                    print("Comment matched")
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
                            res_file = "%s-%s_Run.log"%(issue.key,QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                            #res_file = "%s-%s.log"%(issue.key,QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                            print(res_file)
                            for attachment in issue.fields.attachment:
                                fName=str(attachment.filename)
                                print(fName)
                                if res_file == fName:
                                    try:
                                        attachmentId = attachment.id
                                        filename = attachment.filename
                                        print("Deleting the attachment:",filename)
                                        attachment.delete()
                                        print("Deleting the Comment:",comment)
                                        comment.delete()
                                    except:
                                        print("Unable to delete the attachments and comments...")
                                        continue
                            
if (__name__ == "__main__"):
    ret = main(sys.argv[1:])
    sys.exit(ret)
