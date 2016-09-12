#!/usr/bin/env python
'''
Created on Mar 22, 2016

@author: ppremkum
'''
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from core import QAAUTOMATIONPYFX_GRAPH_FILE, QAAUTOMATIONPYFX_GRAPH_TEMPLATE_FILE
#Creates html page with the graph file rendered based on test execution status.
def htmlCreator(fileName):
    import os
    if os.path.isfile(fileName):
        os.remove(fileName)
    html = open(fileName,'w')
    html.write('{% load static from staticfiles %}'+"\n")
    html.write('<img src="{% static "query/graph.jpg" %}" alt="Graph" />'+"\n")
    html.close()


def main(arguments):
    unique_lst = []
    tst_lst = []
    csvFile = None
    if type(arguments) is list:
        args = arguments[0].split(" ")
    else:
        args = arguments.split(" ")
    i = 0
    for arg in args:
        if arg == '-c' or arg == '--csv':
            csvFile = args[i + 1]
        elif arg == '':
            i += 1
        else:
            i += 2
    if csvFile == None:
        print("Wrong arguments mentioned. Please pass the proper csv file as an input..")
        print("-c csvFile")
        sys.exit(1)
    csvF = open(csvFile)
    reader = csv.DictReader(csvF)
    for row in reader:
        if row['UNIQUEID'] not in unique_lst:
            unique_lst.append(row['UNIQUEID'])
        if row['TestcaseId'] not in tst_lst:
            tst_lst.append(row['TestcaseId'])
    csvF.close()
    passMeans = []
    failMeans = []
    for l in unique_lst:
        pscnt=0
        flcnt=0
        ntcnt=0
        if l == '':
            continue
        for test in tst_lst:
            fd = open(csvFile, 'r')
            reader = csv.DictReader(fd)
            if l == '':
                continue
            for r in reader:
                if r['UNIQUEID'] != '':
                    if l == r['UNIQUEID'] and r['TestcaseId'] == test:
                        if r['Result'] == "PASS":
                            pscnt = pscnt+1
                        elif r['Result'] == "FAIL":
                            flcnt = flcnt+1
                        else:
                            ntcnt = ntcnt+1
            fd.close()
        passMeans.append(pscnt)
        failMeans.append(flcnt)
    N = len(unique_lst)
    passStd=[]
    failStd=[]
    for i in range(N):
        passStd.append(0)
        failStd.append(0)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, passMeans, width, color='b', yerr=passStd)
    rects2 = ax.bar(ind + width, failMeans, width, color='r', yerr=failStd)
    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of Tests')
    ax.set_title('Results of various runs')
    ax.set_xticks(ind + width)
    labels = []
    for unqId in unique_lst:
        labels.append(unqId.split("_")[-1])
        
    srng = unique_lst[0].split(labels[0])[0]
    stng = 'Project and scopes strings are:%s'%(srng)
    ax.set_xlabel(stng)
    ax.set_xticklabels(labels, rotation=45)
    ax.legend((rects1[0], rects2[0]), ('PASS', 'FAIL'))
    
    def autolabel(rects):
        # attach some text labels for height
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    plt.tight_layout()
    plt.savefig(QAAUTOMATIONPYFX_GRAPH_FILE)
    htmlCreator(QAAUTOMATIONPYFX_GRAPH_TEMPLATE_FILE)

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
