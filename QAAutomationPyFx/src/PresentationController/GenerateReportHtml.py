'''
Created on Feb 29, 2016

@author: ppremkum
'''
#!/usr/bin/env python
import sys
import csv
  
def htmlCreater(rdr, lst, tst):
    print ("Creating html file...")
    from core import QAAUTOMATIONPYFX_REPORT_FILE
    html = open(QAAUTOMATIONPYFX_REPORT_FILE,'w')
    #html = open("C:\\Users\\ppremkum\\Desktop\\Report.html", 'w')
    html.writelines("<html>")
    html.writelines("<head>")
    html.writelines("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" />")
    html.writelines("<title>JIRA AUTOMATION Validation Report</title>")
    html.writelines('<align="center"><body><font color = "#303030" size="4"> <center> <b> JIRA REST API Report </center></body> </b> <br/> <body>')
    for l in lst:
        print ("List:", l)
        html.writelines("<table>")
        html.writelines("<table border = 1><tr>")
        html.writelines("</tr>")
        cmd = '<td bgcolor="#303030"> <font color="#FFFFFF"><b><a name="UNIQUEINSTANCEID">%s</a></b></td>' % (l)
        html.writelines(cmd)
        html.writelines("<tr>")
        html.writelines("</tr>")
        html.writelines('<td bgcolor="#303030"> <font color="#FFFFFF"><b><span class="valid" title="TestCaseId">TestCaseId</b></b></td>')
        html.writelines('<td bgcolor="#303030"> <font color="#FFFFFF"><b> <span class="valid" title="RESULT">Result</b></td>')
        html.writelines('<tr>')
        html.writelines('</tr>')
        fd = open(rdr, 'r')
        reader = csv.DictReader(fd)        
        for r in reader:
            print ("Reader:", r)
            if r['TestcaseId'] == None:
                continue
            if l == r['UNIQUEID']:
                tcId = '<td bgcolor=#45582D> <font color="#FFFFFF"><b>%s</b></td>' % (r['TestcaseId'])
                html.writelines(tcId)
                result = '<td bgcolor=#45582D> <font color="#FFFFFF"><b><a href="%s" style="color: #FFFFFF" target="rightside">%s</a></b></td>' % (r['ResultFile'], r['Result'])
                html.writelines(result)
                html.writelines("<tr>")
                html.writelines("</tr>")
        html.writelines('</table>')
        fd.close()

    html.writelines("</html>")
    print ("html creation done")
    
def main(arguments):
    unique_lst = []
    tst_lst = []
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
    print (csvFile)
    csvF = open(csvFile)
    reader = csv.DictReader(csvF)
    for row in reader:
        if row['UNIQUEID'] not in unique_lst:
            unique_lst.append(row['UNIQUEID'])
        if row['TestcaseId'] not in tst_lst:
            tst_lst.append(row['TestcaseId']) 
    print (unique_lst)
    csvF.close()
    htmlCreater(csvFile, unique_lst,tst_lst)

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
