#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import platform
if platform.system() != 'Linux':
	PACKAGE_PATH="C:\Git\dseqa\HomeGrownTools\QAAutomationPyFx\src"
else:
	PACKAGE_PATH=os.path.join(os.getenv("HOME"),"sqa/dseqa/HomeGrownTools/QAAutomationPyFx/src")
AUTOMATION_DIR=os.path.join(PACKAGE_PATH,"AutomationController")
exprtString="%s:."%(PACKAGE_PATH)
os.environ["PYTHONPATH"] = exprtString
projectName = sys.argv[1]
scope = sys.argv[2]
Range = sys.argv[3]

def InstallPreRequisites():
        print ("Installing pre-requisites")
		if platform.system() != 'Linux':
			command = "pip install setuptools matplotlib"
			command2 = "easy_install jira"
		else:
			command = "echo 'amd@123' | sudo -S DEBIAN_FRONTEND=noninteractive apt-get -y -q --force-yes install python3-setuptools python3-matplotlib mpv"
			command2 = "echo 'amd@123' | sudo -S DEBIAN_FRONTEND=noninteractive easy_install3 jira"	
        command_execution = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output,err = command_execution.communicate()
        command2_execution = subprocess.Popen(command2,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output2,err2 = command2_execution.communicate()
        if command_execution.returncode != 0 or command2_execution.returncode != 0:
                print("prerequisite installation failed")
                print("==================================")
                print(output)
                print("==================================")
                print(output2)
                print("==================================")
                print(err)
                print("==================================")
                print(err2)
                print("==================================")
                sys.exit(1)
        else:
                print("Prerequisite installation successful")
                print(output)
                print(output2)

def CloneGitRepo():
	print("Cloning dseqa repo...")
	if platform.system() != 'Linux':
		gitRepo=os.path.join("C:\Git")
	else:
		gitRepo=os.path.join(os.getenv("HOME"),"sqa")
	if os.path.isdir(gitRepo) != True:
		print("Removing the GitRepodir before cloning the latestone")
		#shutil.rmtree(gitRepo)
		os.makedirs(gitRepo)
	os.chdir(gitRepo)
	command = "git clone ssh://jenkinshas@git.amd.com:29418/eesc/ec/dse/dseqa"
	command_execution = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,err = command_execution.communicate()
	if command_execution.returncode != 0:
	    print("Git clone of dseqa repo failed")
	    print("Error is:",err)
	    sys.exit(1)
	else:
	    print("Cloning dseqa repo successful")
	    print(output)

def ExecuteTests():
	import os
	os.chdir(AUTOMATION_DIR)
	if platform.system() == 'Linux':
		if os.path.isdir("/home/jenkinshas/Streams") != True:
			os.makedirs("/home/jenkinshas/Streams")
		cmd = "cp -r /mnt/QA_PERFLAB/VDK_Testing/AXELL/Axell_streams/MPV_Streams/* /home/jenkinshas/Streams/"
		command_execution = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		output,err = command_execution.communicate()
		if command_execution.returncode != 0:
			print("Execution Failed")
			print(err)
			sys.exit(1)
		else:
			print("Execution successful")
			print(output)
			
	command = 'python3 QAAutomationPyFx.py -o \"ExecuteTests\" -a \"-p %s -s %s -r %s\"'%(projectName,scope,Range)
	command_execution = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,err = command_execution.communicate()
	if command_execution.returncode != 0:
		print("Execution Failed")
		print(err)
		sys.exit(1)
	else:
		print("Execution successful")
		print(output)
	
#InstallPreRequisites()
CloneGitRepo()
#ExecuteTests()

