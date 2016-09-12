#!/usr/bin/env python
import os
import sys

for i in range(21,121):
	if i < 100:
		flag = "00%s"%(i)
	elif i >= 100:
		flag ="0%s"%(i)
	masterConfig = "masterconfig_%s.cfg"%(flag)
	
	fd = open(masterConfig,"w")
	tiledPlaybackConfig = "tiledPlaybackConfig_%s.cfg"%(flag)
	fd.writelines("1")
	fd.writelines("\n")
	fd.writelines(tiledPlaybackConfig)
	fd.close()
	
	