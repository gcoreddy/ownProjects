#!/usr/bin/env python
import os
import sys

filesList=os.listdir(".")
for f in os.listdir("."):
	print f
	newName="%s.att"%(f.split(".")[0])
	os.rename(f,newName)
	
