'''
Created on Dec 8, 2015

@author: ppremkum
'''
from abc import ABCMeta, abstractmethod
#Abstract class for the framework. Need to create implementor classes for this.
class RestAPIBase(object):

    __metaclass__ = ABCMeta
    
    scopeList = []
    execTypeList = []

    def __init__(self, server, user, password):

        self.server = server
        self.user = user
        self.password = password
        self.tcdict = {}

    @abstractmethod
    def pull_testcases(self, searchString, TAG, testInput):
        """Returns the response from the corresponding restapi's as per the formatted id and user story provided by the
         user """
        return

    @abstractmethod
    def execute_testcases(self, exec_obj):
        """Class for executing the sample based the validation input that we extracted from the each test case
        and returns the dictionary which contains the TC object id and command execution status"""
        return

    @abstractmethod
    def push_testResults(self):
        """Class for Updating  test results based on the command execution status that we got from the each test case
        and returns the dictionary which contains the TC object id and command execution status"""
        return
