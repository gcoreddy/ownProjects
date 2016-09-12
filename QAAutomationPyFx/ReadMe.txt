ReadMe for QA AutomationPyFx:

Pre-reqs:
1. Python 3.4.1 is required to run the framework.
2. JIRA 1.0.3 or later
3. matplotlib (1.5.1 or later)
4. matplotlib install the following pre-reqs automatically
      : numpy (1.10.4), cycler (0.10.0), python-dateutil (2.5.1), pyparsing (2.1.1), pytz (2016.2)

Execute Tests Command Line:
$> python QAAutomationPyFx.py -o "ExecuteTests" -a "-p SQA -r 635-639 -s QA_EG_AXELL_TC"

Query Results Command Line:
$> python QAAutomationPyFx.py -o "QueryResults" -a "-p SQA -s QA_EG_AXELL_TC -sd 20160322 -g CHECK_QUERY"
$> python QAAutomationPyFx.py -o "QueryResults" -a "-p VDK -s QA_TCSCOPE_SANITY -sd 20160322 -g CHECK_JIRAACCESS"

Generate Report Command Line:
$> python QAAutomationPyFx.py -o "GenerateReport" -a "-c C:\Temp\QAAutomationPyFxWS\SQA_QA_EG_AXELL_TC_2016-03-21\Result_Summary.csv -g CHECK_GENERATION"
