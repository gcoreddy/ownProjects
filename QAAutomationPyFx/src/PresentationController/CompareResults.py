#!/usr/bin/env python
'''
Created on Mar 22, 2016

@author: ppremkum
'''
import sys
import csv
#htmlCreater method creates html file based on summary csv file.
def htmlCreater(rdr, lst, tst):
    print ("Creating html file...")
    from core import QAAUTOMATIONPYFX_COMPARE_FILE
    html = open(QAAUTOMATIONPYFX_COMPARE_FILE,'w')
    html.write('<html lang="en">' + "\n")
    html.write("<head>"+"\n")
    html.write('<meta charset="utf-8">'+"\n")
    cmd = ''
    #Creating html table with uniqueId and test caseIds.Checkbox will be given to select the comparision between runs.
    unq_id = '<table><table border = 1><tr></tr><td bgcolor=#45582D> <font color="#FFFFFF"><b><span class="valid" title="UNIQUEINSTANCEID">UNIQUEINSTANCEID</b></b></td>\';'
    #list.sort(tst)
    for test in tst:
        cmd +='<td bgcolor=#45582D> <font color="#FFFFFF"><b><a name="TestCaseId">%s</a></b></td>'%(test)
    cmd+='<tr></tr>'
    command = '<script> \
function loopForm(form) { \
    var cbResults = \'%s \
    cbResults+= \'%s\' \
    \n for (var i = 0; i < form.elements.length; i++ ) {  \
        if (form.elements[i].type == "checkbox") {  \
            if (form.elements[i].checked == true) { \
                cbResults += form.elements[i].name + \' \'; \
            } \
        } \
    } \
    cbResults+=\'</table>\' \
    \n document.getElementById("cbResults").innerHTML = cbResults; \
} \
</script>'%(unq_id,cmd)
    html.write(command+"\n")
    html.write('</head>'+"\n")
    html.write("<title>Comparison of Tests among different runs</title>" + "\n" )
    html.write('<align="center"><body><font color = "#303030" size="4"> <center> <b> COMPARISION OF DIFFERENT RUNS </center></body> </b> <br/> <body>'+'\n')
    html.write('<body>')
    html.write('<form  name="thisForm">'+'\n')
    for l in lst:
        if l == '':
            continue
        cmd = ''
        cmd = cmd + '<td bgcolor=#FFFFFF> <font color="#000000"><b>%s</b></td>' % (l)
        for test in tst:
            found = False
            fd = open(rdr, 'r')
            reader = csv.DictReader(fd)
            if test == '':
                continue
            for r in reader:
                if r['UNIQUEID'] != '':
                    if l == r['UNIQUEID'] and r['TestcaseId'] == test:
                        if r['Result'] == "PASS":
                            found = True
                            result = '<td  bgcolor="#006666"> <font color="#000000"><b><a href="%s" style="color: #FFFFFF" target="rightside">%s</a></b></td>' % (r['ResultFile'], r['Result'])
                        elif r['Result'] == "FAIL":
                            found = True
                            result = '<td  bgcolor="#730B00"> <font color="#000000"><b><a href="%s" style="color: #FFFFFF" target="rightside">%s</a></b></td>' % (r['ResultFile'], r['Result'])
                        cmd = cmd + result
            if found != True:
                result = '<td  bgcolor="#00ff00"> <font color="#000000"><b><a href="#" style="color: #FFFFFF" target="rightside">NOTRUN</a></b></td>'
                cmd = cmd + result
            fd.close()
        cmd = cmd + "<tr></tr>"
        comand = '<input type="checkbox" name=\'%s\' value="%s" />%s<br>'%(cmd,l,l)
        html.write(comand + "\n")
    html.write('<input type="button" value="CompareResults" onclick="loopForm(document.thisForm);">'+ "\n")
    html.write('</form>'+'\n')
    html.write('<div id="cbResults"></div>'+'\n')
    html.write('</body>'+'\n')
    html.write("</html>"+ "\n")
    html.close()
    print ("html creation done")
    
def main(arguments):
    unique_lst = []
    tst_lst = []
    csvFile = None
    #Parsing arguments and assiging the csv file to variable.
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
    #Opening the csv file and reading it with the csv Dictreader module.
    csvF = open(csvFile)
    reader = csv.DictReader(csvF)
    #Creating the unique list to know the number of runs executed for the comparision. Also creating the list of test cases executed  in all runs.
    for row in reader:
        if row['UNIQUEID'] not in unique_lst:
            unique_lst.append(row['UNIQUEID'])
        if row['TestcaseId'] not in tst_lst:
            tst_lst.append(row['TestcaseId'])
    csvF.close()
    #Sending the unique list(number of runs) and test case list to the htmlCreator method to create html file.
    htmlCreater(csvFile, unique_lst,tst_lst)

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
