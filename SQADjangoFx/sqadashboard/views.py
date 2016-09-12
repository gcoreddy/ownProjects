from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta
from sqa import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import Context
from sqadashboard import models as m
from django.template import RequestContext, Template, Context

automationDir = settings.AUTOMATION_BASE_DIR
def query_Results(projectName, scope, startDate, endDate=None):
    import subprocess
    import os, sys
    cur_dir = os.getcwd()
    os.chdir(automationDir)
    if endDate == None:
        cmd = '-o QueryResults -a "-p %s -s %s -sd %s"' % (projectName, scope, startDate)
    else:
        cmd = '-o QueryResults -a "-p %s -s %s -sd %s -ed %s"' % (projectName, scope, startDate, endDate)
    command = "python QAAutomationPyFx.py %s" % (cmd)
    cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = cmd_execution.communicate()
    if cmd_execution.returncode != 0:
        print("Failed to execute the query....")
        print("Err is:",err)
        sys.exit(1)
    print("output isss:",output, err)
    try:
        resFile = output.split(b' ResultFile:')[1].strip().decode("utf-8")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Something went wrong")
        print("Exception is:")
        print(e)
        sys.exit(1)
    os.chdir(cur_dir)
    return resFile


def script_exec(resFile,genericString=None):
    import subprocess
    import os, sys
    try:
        cur_dir = os.getcwd()
        os.chdir(automationDir)
        cmd = '-o GenerateReport -a "-c %s -g %s"' % (resFile,genericString)
        command = "python QAAutomationPyFx.py %s" % (cmd)
        cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = cmd_execution.communicate()
        if cmd_execution.returncode != 0:
            print("Failed to generate the Report")
            print("Error is:",err)
            sys.exit(1)
        os.chdir(cur_dir)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error is %s" % (e))
        sys.exit(1)

def compare_results(resFile):
    import subprocess
    import os,sys
    try:
        cur_dir = os.getcwd()
        os.chdir(automationDir)
        cmd = '-o CompareResults -a "-c %s"' % (resFile)
        command = "python QAAutomationPyFx.py %s" % (cmd)
        cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = cmd_execution.communicate()
        if cmd_execution.returncode != 0:
            print("Failed to generate the comparison report")
            print("Error is:",err)
            sys.exit(1)
        os.chdir(cur_dir)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error occured:%s"%(e))
        sys.exit(1)

def plot_graph(resFile):
    import subprocess
    import os,sys
    try:
        cur_dir = os.getcwd()
        os.chdir(automationDir)
        cmd = '-o PlotGraph -a "-c %s"' % (resFile)
        command = "python QAAutomationPyFx.py %s" % (cmd)
        cmd_execution = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = cmd_execution.communicate()
        if cmd_execution.returncode != 0:
            print("Failed to plot the Graph")
            print("Error is:",err)
            sys.exit(1)
        print("Output is:",output)
        os.chdir(cur_dir)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Error occured:%s"%(e))
        sys.exit(1)

def query_detail(request, query_id):
    try:
        query = m.Search.objects.get(pk=query_id)
    except m.Search.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404
    return render(request, 'query/detail.html', {'query': query})

def compare_detail(request, compare_id):
    try:
        compare = m.Search.objects.get(pk=compare_id)
    except m.Search.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404
    return render(request, 'query/compare.html', {'query': compare})

def plot_detail(request, plot_id):
    try:
        plot = m.Search.objects.get(pk=plot_id)
    except m.Search.DoesNotExist:
        # If no Post has id post_id, we raise an HTTP 404 error.
        raise Http404
    return render(request, 'query/graph.html', {'query': plot})

def getQuery(request):
    if request.method == 'GET':
        return render(request, 'query/upload.html', {})
    elif request.method == 'POST':
        if request.POST['OPTION'] == "QUERYRESULTS":
                if request.POST['endDate']:
                    resFile = query_Results(request.POST['projectName'], request.POST['scope'],
                                            request.POST['startDate'], request.POST['endDate'])
                else:
                    resFile = query_Results(request.POST['projectName'], request.POST['scope'],
                                            request.POST['startDate'])
                script_exec(resFile,request.POST['genericString'])
                query = m.Search.objects.create(projectName=request.POST['projectName'], startDate=datetime.utcnow(),
                                                scope=request.POST['scope'], endDate=datetime.utcnow(),genericString=request.POST['genericString'])
                return HttpResponseRedirect(reverse('query_detail', kwargs={'query_id': query.id}))
        elif request.POST['OPTION'] == "GENERATEREPORT":
            try:
                if request.POST['csvFile']:
                    script_exec(request.POST['csvFile'],request.POST['genericString'])
                    query = m.Search.objects.create(projectName=request.POST['projectName'],
                                                    startDate=datetime.utcnow(), scope=request.POST['scope'],
                                                    endDate=datetime.utcnow(),genericString=request.POST['genericString'])
                    return HttpResponseRedirect(reverse('query_detail', kwargs={'query_id': query.id}))
            except Exception as e:
                print("Error is %s" % (e))
                return render(request, 'query/error.html', {})
        elif request.POST['OPTION'] == "COMPARERESULTS":
            if request.POST['endDate']:
                resFile = query_Results(request.POST['projectName'], request.POST['scope'],request.POST['startDate'], request.POST['endDate'])
            else:
                resFile = query_Results(request.POST['projectName'], request.POST['scope'],request.POST['startDate'])
            compare_results(resFile)
            query = m.Search.objects.create(projectName=request.POST['projectName'], startDate=datetime.utcnow(),
                                                scope=request.POST['scope'], endDate=datetime.utcnow(),genericString=request.POST['genericString'])
            return HttpResponseRedirect(reverse('compare_detail',kwargs={'compare_id':query.id}))
        elif request.POST['OPTION'] == "TRENDING":
            if request.POST['endDate']:
                resFile = query_Results(request.POST['projectName'], request.POST['scope'],request.POST['startDate'], request.POST['endDate'])
            else:
                resFile = query_Results(request.POST['projectName'], request.POST['scope'],request.POST['startDate'])
            plot_graph(resFile)
            query = m.Search.objects.create(projectName=request.POST['projectName'], startDate=datetime.utcnow(),
                                                scope=request.POST['scope'], endDate=datetime.utcnow(),genericString=request.POST['genericString'])
            return HttpResponseRedirect(reverse('plot_detail',kwargs={'plot_id':query.id}))
        elif request.POST['OPTION'] == "PERFORMANCE":
            print("PASS")


