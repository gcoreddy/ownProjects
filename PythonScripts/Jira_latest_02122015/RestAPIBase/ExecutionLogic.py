
class ExecutionLogic(object):

	def __init__(self, tcExecType, testCase, exec_obj):
		self.testCase = testCase
		self.tcExecType = tcExecType
		self.exec_obj = exec_obj

	def execute_testCase(self, data, issue_key):
		try:
			import platform
			import os
			import subprocess
			if platform.system() == "Windows":
				batch_file = issue_key +".bat"
				startLine=""
			elif platform.system() == "Linux":
				batch_file = issue_key +".sh"
				startLine="#!/bin/bash"
			if os.path.isfile(batch_file):
				os.remove(batch_file)
			fh = open(batch_file, "w")
			fh.writelines(startLine.replace('\r\n', os.linesep))
			fh.writelines("\n")
			fh.writelines(data.replace('\r\n', os.linesep))
			fh.close()
			os.chmod(batch_file,0777)
			command = os.path.join(os.getcwd(),batch_file)
			cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			output, err = cmd_execution.communicate()
			print output
			print "Error is:",err
			print cmd_execution.returncode
			if cmd_execution.returncode != 0:
				print "Command Executed: [%s]" % command
				print "Execution ERROR: \n",err
				output = err + "[TestCase FAILED]"
				print "=============%s CommandExecution Ends Status: [%s]======================" % (command, 'FAILED')
				return output
			else:
				print "Command Executed: [%s]" % command
				output = output + "[TestCase PASSED]"
				print "=============%s CommandExecution Ends Status: [%s]======================" % (command, 'PASSED')
				return output
		except IOError, e:
			print "ERROR: ", str(e)


	def run(self):
		print "Starting the Test Execution"
		if self.exec_obj != None:
			data = self.exec_obj.run(self.tcExecType, self.testCase)
			return self.execute_testCase(data, self.testCase.key)
		else:
			import sys
			print "Execute object is not present... exiting"
			sys.exit(1)
