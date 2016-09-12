#!/usr/bin/env python3
import os
import sys
import shutil
import platform
import subprocess
import stat

if len(sys.argv) != 2:
	print("Invalid arguments mentioned")
	sys.exit(1)
sdkPath=sys.argv[1]

if sdkPath == "buildRoom":
	if os.path.isfile("archive.zip"):
		os.remove("archive.zip")
		shutil.rmtree("archive")
	archive="wget http://10.138.131.11:8080/job/PachinkoGaming_pkg/C=Release,L=LBM,O=Ubuntu-15.04,P=amd64,R=static,T=gcc-default/lastSuccessfulBuild/artifact/*zip*/archive.zip"
	command_execution = subprocess.Popen(archive,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,err = command_execution.communicate()
	if command_execution.returncode != 0:
		print("Failed download the latest build from build room ")
		sys.exit(1)
	else:
		try:
			import glob
			os.system("unzip archive.zip")
			scrptPath = glob.glob("archive/*.sh")[0]
			os.chmod(scrptPath,stat.S_IXGRP | stat.S_IXUSR | stat.S_IRUSR | stat.S_IRGRP)
			sdkActualPath = os.path.join(os.getcwd(),scrptPath)
		except Exception as e:
			print("Installation Failed with an error",e)
			sys.exit(1)
elif platform.system() == 'Linux' and sdkPath.find("perflab") != -1:
	sdkActualPath = sdkPath.replace("\\perflab-blr\\PerformanceLAB\\","/mnt/QA_PERFLAB/").replace("\\","/")
else:
	sdkActualPath = sdkPath

if os.path.exists(sdkActualPath) == 0:
	print("Invalid sdk File mentioned....")
	sys.exit(1)
else:
	sdkInstaller = os.path.basename(sdkActualPath)

destDir = os.getcwd()

try:
	shutil.copy(sdkActualPath,destDir)
except Exception as e:
	print("Copying of pachinko installar failed..")
	print(e)
	sys.exit(1)

sdkCurInstallFile = os.path.join(os.getcwd(),sdkInstaller)
inStallDir = os.path.join(os.getcwd(),"sdkInstaller")
if os.path.exists(inStallDir):
	shutil.rmtree(inStallDir)
os.makedirs(inStallDir)

cmd = "./%s --noexec --nox11 --target %s &> stdouterr.txt"%(sdkInstaller,inStallDir)
print("Command is:",cmd)
command_execution = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
output,err = command_execution.communicate()
if command_execution.returncode != 0:
	print("Installer script failed with an error:",output)
	print("Installer script failed with an error:",err)
	sys.exit(1)
else:
	os.chdir(inStallDir)
	cmd = "./install.sh --acceptEULA yes --silent"
	command_execution = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output,err = command_execution.communicate()
	if command_execution.returncode != 0:
		print("Installation failed while running install.sh in silent mode")
		print(err)
		print(output)
		sys.exit(1)
	else:
		print("Installation successful")
		#os.system("source ~/.bashrc")
		print("SDKPACHINKOROOTis:",os.getenv("AMDPACHINKOSDKROOT"))
		shutil.rmtree(inStallDir)
		os.remove(sdkCurInstallFile)
		print(output)




	
