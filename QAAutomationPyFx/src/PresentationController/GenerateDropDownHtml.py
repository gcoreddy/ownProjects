'''
Created on Feb 29, 2016

@author: ppremkum
'''
#!/usr/bin/env python
import sys
import csv
  
def htmlCreater(rdr, lst,genericString):
    print ("Creating html file...")
    from core import QAAUTOMATIONPYFX_REPORT_FILE
    divlst = []
    #Creates html page with dropdown list, dropdown list contains uniqueId's.If selects, all the tests in the perticular run will be poped out.Below code has this logic using java script.
    for l in lst:
        cmd = '<div class="%s box"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" /> \
              <title>JIRA AUTOMATION Validation Report</title> \
        <align="center"><body><font color = "#303030" size="4"> <center> <b> JIRA REST API Report </center></body> </b> <br/> <body> \
        <table><table border = 1><tr></tr> \
        <td bgcolor=#45582D> <font color="#FFFFFF"><b><a name="GENERICSTRING">%s</a></b></td><tr></tr> \
        <td bgcolor=#45582D> <font color="#FFFFFF"><b><a name="UNIQUEINSTANCEID">%s</a></b></td><tr></tr> \
        <td bgcolor=#45582D> <font color="#FFFFFF"><b><span class="valid" title="TestCaseId">TestCaseId</b></b></td> \
        <td bgcolor=#45582D> <font color="#FFFFFF"><b> <span class="valid" title="RESULT">Result</b></td> \
        <tr></tr>'%(l.split(".")[0],genericString,l)
        fd = open(rdr, 'r')
        reader = csv.DictReader(fd)
        for r in reader:
            if r['TestcaseId'] == None:
                continue
            if l == r['UNIQUEID']:
                tcId = '<td bgcolor=#FFFFFF> <font color="#000000"><b>%s</b></td>' % (r['TestcaseId'])
                cmd = cmd + tcId
                if r['Result'] != "FAIL":
                    result = '<td  bgcolor="#006666"> <font color="#000000"><b><a href="%s" style="color: #FFFFFF" target="rightside">%s</a></b></td>' % (r['ResultFile'], r['Result'])
                else:
                    result = '<td  bgcolor="#730B00"> <font color="#000000"><b><a href="%s" style="color: #FFFFFF" target="rightside">%s</a></b></td>' % (r['ResultFile'], r['Result'])
                cmd = cmd + result + '<tr></tr>'
        cmd = cmd + "</table>"
        divlst.append(cmd)
        fd.close()


    html = open(QAAUTOMATIONPYFX_REPORT_FILE,'w')
    html.write('<html lang="en">' + "\n")
    html.write("<head>"+"\n")
    html.write('<meta charset="utf-8">'+"\n")
    html.write("<title>JIRA AUTOMATION Validation Report</title>"+"\n")
    html.write('<style type="text/css"> \
    .box{ \
        padding: 20px; \
        display: none; \
        margin-top: 20px; \
        border: 1px solid #000; \
    } \
    .red{ background: #ff0000; } \
    .green{ background: #00ff00; } \
    .blue{ background: #0000ff; }\
</style>'+"\n")
    html.write('<script type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>' + "\n")
    var1 = lst[0].split(".")[0]
    cmd = '<script type="text/javascript"> \
    $(document).ready(function(){ \
        $("select").change(function(){ \
            $(this).find("option:selected").each(function(){ \
                if($(this).attr("value")=="%s"){ \
                    $(".box").not(".%s").hide(); \
                    $(".%s").show(); \
                }'%(var1,var1,var1)
    for l in lst[1:]:
        var2 = l.split(".")[0]
        cmd = cmd + 'else if($(this).attr("value")=="%s"){ \
                    $(".box").not(".%s").hide(); \
                    $(".%s").show(); \
                }'%(var2,var2,var2)
    cmd = cmd+ 'else{ \
                    $(".box").hide(); \
                } \
            }); \
        }).change(); \
    }); \
    </script>'
    html.write(cmd + "\n")
    html.write('</head>' + "\n")
    html.write('<body>' + '\n')
    html.write('<div>' + "\n")
    html.write('<select>' + "\n")
    html.write('<option>Choose Value</option>'+"\n")
    for l in lst:
        cmd = '<option value="%s">%s</option>'%(l.split('.')[0],l.split('.')[0])
        html.write(cmd + "\n")
    html.write('<select>' + "\n")
    html.write('</div>' + "\n")
    for l in lst:
        for div in divlst:
            if div.find(l) != -1:
                #cmd = '<div class="%s box">%s</div>'%(l.split('.')[0],div)
                html.write(div + "\n")
        html.write('</div>' + "\n")
    html.write('</body>' + "\n")
    html.write('</html>' + "\n")
    html.close()
    print ("html creation done")
    
def main(arguments):
    unique_lst = []
    genericString = None
    csvFile = None
    #Parsing the arguments based on inputs.
    if type(arguments) is list:
        args = arguments[0].split(" ")
    else:
        args = arguments.split(" ")
    i = 0
    for arg in args:
        if arg == '-c' or arg == '--csv':
            csvFile = args[i + 1]
        elif arg == '-g':
            genericString = args[i+1]
        elif arg == '':
            i += 1
        else:
            i += 2
    if genericString == None or csvFile == None:
        print("Generic string or csvFile is not mentioned please mention proper inputs.. exiting")
        print("Inputs to be passed -c 'csvFile' -g 'GenericString'")
        sys.exit(1)
    #Opening csv file and creating a list with the unique ids.
    csvF = open(csvFile)
    reader = csv.DictReader(csvF)
    for row in reader:
        if row['UNIQUEID'] not in unique_lst:
            unique_lst.append(row['UNIQUEID'])
    csvF.close()
    htmlCreater(csvFile, unique_lst,genericString)

if __name__ == "__main__":
    ret = main(sys.argv[1:])
    sys.exit(ret)
