#!/usr/bin/env python
'''
Created on Dec 20, 2015

@author: ppremkum
'''
#importing required modules into this file
from AutomationController import JiraTestController
from PresentationController import TestReportViewer, GenerateDropDownHtml, CompareResults, PlotGraph, PurgeResults
import argparse

#Help Function, which describes about the usage.
def help_func():
    print("===================================================================")
    print ("%s <option> <args>")
    print ("<option takes ExecuteTests/QueryResults/GenerateReport as an argument>")
    print ("<args are specific to the option selected>")
    print ("<ExecuteTests> -p 'projectName' -s 'scope' -r 'range'")
    print ("<QueryResults> -p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
    print ("<CompareResults> -p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
    print ("<PlotGraph> -p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
    print ("<GenerateReport> -f 'csvFile'")
    print ("<PurgeResults> -p 'projectName' -s 'scope' -sd 'startDate' -ed 'endDate'")
    print("===================================================================")

'''This function parses and return arguments passed in'''
# Assign description to the help doc
parser = argparse.ArgumentParser(description='Script retrieves and executes the jira testcases or queries for test results or generates test reports')

# Add arguments
parser.add_argument('-o', '--option', type=str, help=help_func(), required=True)
parser.add_argument('-a', '--args', help='Arguments corresponding to the option selected', required=True, type=str)
arguments = parser.parse_args()
# Assign args to variables
option = arguments.option
args = arguments.args
    
print ("Arguments Passed are:",args)
try:
    if option == "ExecuteTests":
        # This will execute the tests and updates the results based on arguments.
        JiraTestController.main(args)
    elif option == "QueryResults":
        # This will fetch the results based on arguments and creates CSV file with the results.
        TestReportViewer.main(args)
    elif option == "GenerateReport":
        #Generates html report from a given search criteria.
        GenerateDropDownHtml.main(args)
    elif option == "CompareResults":
        #Compares the results between runs based on search criteria. 
        CompareResults.main(args)
    elif option == "PlotGraph":
        #Generates graph from the results based on search criteria.
        PlotGraph.main(args)
    elif option == "PurgeResults":
        #Purges(Deletes permanently) the previous results based on search criteria(startDate and endDate).
        PurgeResults.main(args)
    else:
        print ("Invalid option mentioned")
        help_func()
except Exception as e:
    import traceback
    import sys
    print("Error occured while running the command:",option)
    print("Exception occured is:")
    traceback.print_exc()
    sys.exit(1)
