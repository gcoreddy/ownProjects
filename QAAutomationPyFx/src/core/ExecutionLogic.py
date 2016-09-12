'''
Created on Dec 8, 2015

@author: ppremkum
'''
#Class contain actual execution logic. Data of the testScript is the input for this class.
#Takes the data of the testScript and converts it into bat or bash file depending upon platform/OS
#Return the execution result(output/error).
class ExecutionLogic(object):
    #Constructor method initializes test execution type, testcase object, execution object. testcase object is nothing but issue object, exec_obj is different for different projects. tcExecType is execution type, ATT/SHELL/BAT etc.
    def __init__(self, tcExecType, testcase, exec_obj):
        self.testcase = testcase
        self.tcExecType = tcExecType
        self.exec_obj = exec_obj

    def execute_testcase(self, data, issue_key):
        global QAAutomationPyFx_Worksapce
        try:
            import platform, os, subprocess, stat
            from core import QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID
            print ("Here I'm in ExecutionLogic: " + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID)
            #Checking the platform and assigning the startLine(For bash #!/bin/bash should be added). Depends on platform .bat or .sh files will be created with execution data.Created file will be executed and output and return value will be captured. Based on Return value testcase will be marked as PASS/FAIL.
            if platform.system() == "Windows":
                from core import QAAUTOMATIONPYFX_WIN_WORKSPACE
                exec_file = QAAUTOMATIONPYFX_WIN_WORKSPACE + "\\" + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "\\" + issue_key + ".bat"
                startLine=""
            elif platform.system() == "Linux":
                from core import QAAUTOMATIONPYFX_LINUX_WORKSPACE
                exec_file = QAAUTOMATIONPYFX_LINUX_WORKSPACE + "/" + QAAUTOMATIONPYFX_UNIQUE_EXEC_INST_ID + "/" + issue_key +".sh"
                if data.decode('ascii').find("#!/bin/bash") == -1:
                    startLine="#!/bin/bash"
                else:
                    startLine=""
            if os.path.isfile(exec_file):
                os.remove(exec_file)
            fh = open(exec_file, "w")
            fh.writelines(startLine.replace('\r\n', os.linesep))
            fh.writelines("\n")
            fh.writelines(data.decode('ascii').replace('\r\n', os.linesep))
            fh.close()
            os.chmod(exec_file, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IWOTH|stat.S_IXOTH)
            command = os.path.join(os.getcwd(),exec_file)
            cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output, err = cmd_execution.communicate()
            execOut = b"Executing the command:\n %s \n"%(data)
            print (cmd_execution.returncode)
            if cmd_execution.returncode != 0:
                print ("Command Executed: [%s]" % command)
                print ("Execution ERROR: \n",err)
                output = execOut + err + output + b"\n[Testcase FAILED]"
                print ("=============%s CommandExecution Ends Status: [%s]======================" % (command, 'FAILED'))
                return output
            else:
                print ("Command Executed: [%s]" % command)
                output = execOut + output + b"\n[Testcase PASSED]"
                print ("=============%s CommandExecution Ends Status: [%s]======================" % (command, 'PASSED'))
                return output
        except Exception as e:
            import sys
            print ("Execution ERROR: \n", str(e))
            output = b"ERROR: Unable to Get/Download the testCase file data" + b"\n[Testcase NOTRUN]"
            print ("=============CommandExecution Ends Status: NOTRUN======================")
            print(output)
            return output
            


    def run(self):
        print ("Starting the Test Execution")
        if self.exec_obj != None:
            #Getting the test script data from Execution logic object.
            data = self.exec_obj.run(self.tcExecType, self.testcase)
            if data !=1:
                return self.execute_testcase(data, self.testcase.key)
            else:
                return 1
        else:
            import sys
            print ("Execute object is not present... exiting")
            sys.exit(1)
