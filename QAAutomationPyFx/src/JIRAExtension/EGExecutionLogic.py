'''
Created on Dec 8, 2015

@author: ppremkum
'''
#!/usr/bin/env python
from core.ExecutionLogic import ExecutionLogic

#Inherited class from ExecutionLogic and should return content of test script which is down-loaded from issue attachment.This logic can be diferent for various projects. 
class EGExecutionLogic(ExecutionLogic):
    user = None
    password = None
    def __init__(self):
        print ("")
                                                    
    def get_data(self, downloadurl):
        #get_data method is used to download the testcase file from the jira.requests module is used for downloading the file.
        import requests
        import sys
        global count
        count = 0
        jira_session = requests.session()
        try:
            from core import QAAUTOMATIONPYFX_JIRA_URL
            jira_session.post(QAAUTOMATIONPYFX_JIRA_URL, auth=(EGExecutionLogic.user, EGExecutionLogic.password), verify=False)
        except:
            print('Unable to connect or authenticate with JIRA server.')
            sys.exit(1)
        def retry():
            #Retry method when download method fails.This method will retry for 5 times and mark the test case as NOT RUN. 
            global count
            if count >= 5:
                print("Failed to get the file content. Max retry count reached... So exiting")
                sys.exit(1)
            try:
                results = jira_session.get(downloadurl)
                count+=1
                if results is None:
                    print("File content get returned NoneType object, so retrying once again..Count No:",count)
                    retry()
                elif results.content == None or results.content == '':
                    print("File content get content returned None value so retrying once again..Count No:",count)
                    retry()
            except Exception as e:
                print("Exception is :",e)
                print("File content get failed so retrying once again..Count No:",count)
                retry()
            else:
                return results
        result = retry()
        if result != None:
            return result.content
        else:
            return None
    
    def run(self, tcExecType, testcase):
        import sys
        import os
        
        self.tcExecType = tcExecType
        self.testcase = testcase
        filename = None
        #Condition for checking the testcase file. Testcase file should contain "TestCase" in the fileName, will skip the test exection if condition fails.
        if self.testcase.fields.attachment != None:
            for attachment in self.testcase.fields.attachment:
                fName=str(attachment.filename)
                if "TestCase" in fName:
                    attachmentId = attachment.id
                    filename = attachment.filename
            if filename == None:
                return 1
            from core import QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL
            downloadurl = QAAUTOMATIONPYFX_JIRA_ATTACHMENTURL + "/%s/%s"%(attachmentId, filename)
            data = self.get_data(downloadurl)
            
            # "TEST_EGVDK_TCEXECTYPE_ATT" & "SQA_EGVDK_TCEXECTYPE_ATT" are for the EG and SQA projects in the Cloud JIRA respectively
            # "QA_EGVDK_TCEXECTYPE_ATT" is for the VDK project in AMD JIRA
            #if self.tcExecType == "TEST_EGVDK_TCEXECTYPE_ATT":
            #if self.tcExecType == "SQA_EGVDK_TCEXECTYPE_ATT":
            #Doing extra steps required depends on test execution type. For apitesttool, need to export extra variables.
            if self.tcExecType == "QA_EGVDK_TCEXECTYPE_ATT":
                apiTestToolBinPath = os.getenv("APITESTTOOL_BIN_PATH")
                
                print ("Bye-passing the Environment Variable setting just for dev purposes. In Production env, this has to be removed.")
                import platform
                if platform.system() == "Windows":
                    from core import QAAUTOMATIONPYFX_WIN_WORKSPACE
                    apiTestToolBinPath = QAAUTOMATIONPYFX_WIN_WORKSPACE + "\\APITestTool.exe"
                elif platform.system() == "Linux":
                    from core import QAAUTOMATIONPYFX_LINUX_WORKSPACE
                    apiTestToolBinPath = QAAUTOMATIONPYFX_LINUX_WORKSPACE + "/APITestTool"
                
                if apiTestToolBinPath == None:
                    print ("APITESTTOOL_BIN_PATH env variable not set to point to the APITestTool binary. Set and export the env variable to proceed.")
                    sys.exit(1)

                from core import QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID
                print ("Here I'm in EGExecutionLogic: " + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
                if platform.system() == "Windows":
                    genTCAttScript = QAAUTOMATIONPYFX_WIN_WORKSPACE + "\\" + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "\\" + "TestCase.att"
                elif platform.system() == "Linux":
                    genTCAttScript = QAAUTOMATIONPYFX_LINUX_WORKSPACE + "/" + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "/" + "TestCase.att"
                    
                if os.path.isfile(genTCAttScript):
                    os.remove(genTCAttScript)
                    
                attFile = open(genTCAttScript, "w")
                attFile.writelines(str(data))
                attFile.close()
                
                data = "%s -s %s"%(apiTestToolBinPath, genTCAttScript)
                return data
            
            #elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_MANUAL":
            #elif self.tcExecType == "SQA_TCEXECTYPE_MANUAL":
            elif self.tcExecType == "QA_TCEXECTYPE_MANUAL":
                print ("\nThis is Manual Testcase. Need to execute it manually.")
                print ("\nSkipping the testcase execution...")
                
            #elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_GUIAUTOMATION":
            #elif self.tcExecType == "SQA_TCEXECTYPE_GUIAUTOMATION":
            elif self.tcExecType == "QA_TCEXECTYPE_GUIAUTOMATION":
                print ("\nThis testcase is GUI Automation Testcase")
                print ("\nSkipping the testcase execution...")
                
            #elif self.tcExecType == "TEST_EGVDK_TCEXECTYPE_TXT":
            #elif self.tcExecType == "SQA_TCEXECTYPE_TXT":
            elif self.tcExecType == "QA_TCEXECTYPE_TXT":
                print ("Executing Testcase by parsing the txt file...")
                return data
            elif self.tcExecType == "QA_TCEXECTYPE_SHELL":
                print ("Executing Testcase by parsing the txt file...")
                return data
            
            else:
                print ("Invalid Exec Type - " + self.tcExecType)
                sys.exit(1)
