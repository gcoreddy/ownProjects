#!/usr/bin/env python
import RestAPIBase
from JiraRestInterface_EG import JiraRestInterface


class TestUtils(JiraRestInterface):

    JiraRestInterface.scopeList = ["TEST_SANITY","TEST_FULL"]
    JiraRestInterface.execTypeList = ["TEST_EGVDK_TCEXECTYPE_ATT","TEST_EGVDK_TCEXECTYPE_MANUAL","TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION","TEST_EGVDK_TCEXECTYPE_TXT"]
    def __init__(self,  server, user, interface_type, password):
        super(TestUtils, self).__init__(server, user, interface_type, password)
        """Return a new Jira object."""
        self.server = server
        self.user = user
        self.password = password
        self.interface_type = interface_type


test = TestUtils('https://amdjira1.atlassian.net/', 'chandra-obul.Reddy@amd.com', 'Chandu@40689','Jira')

#Jira_obj = test.interface_obj('https://amdjira1.atlassian.net/', 'chandra-obul.Reddy@amd.com', 'Chandu@40689','Jira')
puller_from_prjct_id = test.pull_testCases('EG-128')
print puller_from_prjct_id
#puller_from_project_id = test.ipuller_issues_from_prjct_or_story_id(Jira_obj,"EG","1-100","TEST_SANITY")
#print puller_from_project_id
#tc_dict=test.iexecutor(puller_from_project_id,"/home/cas/chandu/APITestTool/APITestTool/qvaApiTestSet/bin/qvaApiTestSet-r")
#tc_upater = test.iupdater(tc_dict)
#test.ipuller_logs_from_string(Jira_obj,"EG","EG_TEST_SANITY_1443160761.47_Run")


