#!/usr/bin/env python
import os
import sys

for i in range(21,121):
	if i < 100:
		flag = "00%s"%(i)
	elif i >= 100:
		flag ="0%s"%(i)
	testCaseFile = "EG-Axell-Lin-TiledPlayback-TestCase-%s.sh"%(flag)
	configFile = "./tiledPlayback masterconfig_%s.cfg"%(flag)
	fd = open(testCaseFile,"w")
	fd.writelines("#!/bin/bash")
	fd.writelines("\n")
	fd.writelines("cd $AMDPACHINKOSDKROOT/samples/tiledPlayback/bin/x86_64/Release")
	fd.writelines("\n")
	fd.writelines(configFile)
	fd.close()
