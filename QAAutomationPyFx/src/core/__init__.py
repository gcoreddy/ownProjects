import os
import sys
import platform
# Globals

#WORKSPACE Directories
#If TEST_NAME is found it means test execution is through jenkins otherwise normal execution.Environment variables are updated according to the execution mode(jenkins/normal).
if os.getenv("TEST_NAME") == None or os.getenv("TEST_NAME") == '':
	QAAUTOMATIONPYFX_WIN_WORKSPACE = "C:\Temp\QAAutomationPyFxWS"
	QAAUTOMATIONPYFX_LINUX_WORKSPACE = os.getenv("HOME")
	summaryXmlFile = "summary.xml"
else:
	testName = os.getenv("TEST_NAME")
	nodeName = os.getenv("THIS_NODE")
	home = os.getenv("HOME")
	#summaryXmlFile = "%s_%s.xml"%(nodeName,testName)
	summaryXmlFile = "summary.xml"
	QAAUTOMATIONPYFX_WIN_WORKSPACE = "C:\Temp\QAAutomationPyFxWS"
	QAAUTOMATIONPYFX_LINUX_WORKSPACE = "%s/workspace/%s/label/%s"%(home,testName,nodeName)

    
QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID = ""

#Django Framework Variables 
#Automation Folder root directory, Used by Django framework
if platform.system() == 'Linux':
	QAAUTOMATIONPYFX_ROOT_FILE=r'%s/sqa/dseqa/HomeGrownTools/QAAutomationPyFx/src'%(os.getenv("HOME"))

	QAAUTOMATIONPYFX_GRAPH_TEMPLATE_FILE = r'%s/sqa/dseqa/HomeGrownTools/SQADjangoFx/sqadashboard/templates/query/graph.html'%(os.getenv("HOME"))

	QAAUTOMATIONPYFX_REPORT_FILE = r'%s/sqa/dseqa/HomeGrownTools/SQADjangoFx/sqadashboard/templates/query/detail.html'%(os.getenv("HOME"))

	QAAUTOMATIONPYFX_COMPARE_FILE = r'%s/sqa/dseqa/HomeGrownTools/SQADjangoFx/sqadashboard/templates/query/compare.html'%(os.getenv("HOME"))

	QAAUTOMATIONPYFX_GRAPH_FILE = r'%s/sqa/dseqa/HomeGrownTools/SQADjangoFx/sqadashboard/static/query/graph.jpg'%(os.getenv("HOME"))

	QAAUTOMATIONPYFX_XML_FILE = os.path.join(QAAUTOMATIONPYFX_LINUX_WORKSPACE,summaryXmlFile)
	QAAUTOMATIONPYFX_WORKSPACE = QAAUTOMATIONPYFX_LINUX_WORKSPACE
	QAAUTOMATIONPYFX_API_BIN =  r'%s/sqa/dseqa/HomeGrownTools/APITestTool/APITestTool/apiTestSet/dtApiTestSet/bin/dtApiTestSet-d'%(os.getenv("HOME"))


else:
	

	QAAUTOMATIONPYFX_ROOT_FILE=r'C:\Git\dseqa\HomeGrownTools\QAAutomationPyFx\src'

	#File name of which report will be generated to. 
	QAAUTOMATIONPYFX_GRAPH_TEMPLATE_FILE = r'C:\Git\dseqa\HomeGrownTools\SQADjangoFx\sqadashboard\templates\query\graph.html'

	#File name of which report will be generated to. 
	QAAUTOMATIONPYFX_REPORT_FILE = r'C:\Git\dseqa\HomeGrownTools\SQADjangoFx\sqadashboard\templates\query\detail.html'

	#File name to which compared data will be written
	QAAUTOMATIONPYFX_COMPARE_FILE = r'C:\Git\dseqa\HomeGrownTools\SQADjangoFx\sqadashboard\templates\query\compare.html'

	#File name to which Graph related data will be written.
	QAAUTOMATIONPYFX_GRAPH_FILE = r'C:\Git\dseqa\HomeGrownTools\SQADjangoFx\sqadashboard\static\query\graph.jpg'
	QAAUTOMATIONPYFX_XML_FILE = os.path.join(QAAUTOMATIONPYFX_WIN_WORKSPACE,summaryXmlFile)
	QAAUTOMATIONPYFX_WORKSPACE = QAAUTOMATIONPYFX_WIN_WORKSPACE
        #ApiTesttool binaryPath
	QAAUTOMATIONPYFX_API_BIN =  r'C:\Git\dseqa\/APITestTool/apiTestSet/dtApiTestSet/bin/dtApiTestSet-d'

#Attlassian JIRA details
#QAAUTOMATIONPYFX_JIRA_URL = "https://amdjira1.atlassian.net"
#QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL = "https://amdjira1.atlassian.net/secure/attachment"

#ontrack JIRA details.
QAAUTOMATIONPYFX_JIRA_URL = "http://10.181.36.21"
QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL = "http://10.181.36.21/secure/attachment"

#List of supported tags/Scope list. If the Tag is not listed in this variable, will throw an error.
#SCOPE_LIST = ["QA_EG_AXELL_TC","QA_EG_AXELL_TC_NONLOOP","QA_EG_AXELL_TC_tokkalee"]

#List of supported execution type list. If the execution type is not listed in this variable, will throw an error.
#EXEC_TYPE_LIST = ["QA_EGVDK_TC", "QA_EGVDK_TCEXECTYPE_ATT","QA_TCEXECTYPE_SHELL"]

#QA execution history story name to which results will be uploaded to. If not mentioned will throw an error.
EXEC_QA_STORY = "VDK-23"

#UserName and password of JIRA
#userName = 'chareddy'
#passwd = 'Chandu@468'
userName = 'ServerSWQA'
passwd = 'Q7i4@c-2A9j='
