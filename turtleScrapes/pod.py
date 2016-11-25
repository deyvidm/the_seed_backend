import xlrd
import json
import sys

def isFloat(s):
    try:
        float(s)
        return True
    except:
        return False

def printAll(s):
    jout = printOrder(s)
    jout = json.dumps(jout)
    f = open('order.json', 'w')
    f.write(jout)
    f.close()
    
    jout = printInvoice(s)
    jout = json.dumps(jout)
    f = open('invoice.json', 'w')
    f.write(jout)
    f.close()
    
def printOrder(s):
    try:
        book = xlrd.open_workbook(s)
        sh = 0 #sheet init
        for x in range(5):
            sh = book.sheet_by_index(x)
            if sh.name.lower() == "order sheet":
                break

        jout = "{\"order sheet\":[" #json format string builder
        total = 0 #total price
        org = 0 #organization
        week = 0 #week number
        date = 0 #delivery date
        for rx in range(sh.nrows):
            try:
                index = sh.cell_value(rowx=rx, colx=0)
                if isFloat(index):
                    name = sh.cell_value(rowx=rx, colx=1)
                    unit = sh.cell_value(rowx=rx, colx=2)
                    supplier = sh.cell_value(rowx=rx, colx=3)
                    pod = sh.cell_value(rowx=rx, colx=4)
                    quantity = sh.cell_value(rowx=rx, colx=6)
                    subtotal = sh.cell_value(rowx=rx, colx=7)
                    js = {"number":index,"name":name,"unit":unit,"supplier":supplier,"pod":pod,"quantity":quantity,"subtotal":subtotal}
                    js = json.dumps(js) #convert to string
                    jout+=js #append to output string
                    jout+="," #insert seperator
                elif "total" in sh.cell_value(rowx=rx, colx=6).lower():
                    total = sh.cell_value(rowx=rx, colx=7)
                elif "organization" in sh.cell_value(rowx=rx, colx=1).lower():
                    org = sh.cell_value(rowx=rx, colx=2)
                elif "week" in sh.cell_value(rowx=rx, colx=6).lower():
                    week = sh.cell_value(rowx=rx, colx=7)
                elif "delivery date" in sh.cell_value(rowx=rx, colx=1).lower():
                    date = sh.cell_value(rowx=rx, colx=2)
            except: #do nothing
                index = 0
                
        jout = jout[:-1] #remove last comma
        jout+="],\"total\":"
        jout+=str(total)
        jout+=",\"organization\":\""
        jout+=str(org)
        jout+="\",\"week\":\""
        jout+=str(week)
        jout+="\",\"delivery date\":\""
        jout+=str(date)
        jout+="\"}"
        jout = json.loads(jout) #to json
        return jout
    except:
        print "failed to read from POD order sheet"
        return None
    
def printInvoice(s):
    try:
        book = xlrd.open_workbook(s)
        sh = 0 #sheet init
        for x in range(5):
            sh = book.sheet_by_index(x)
            if sh.name.lower() == "invoice":
                break

        jout = "{\"invoice\":[" #json format string builder
        total = 0 #total price
        org = 0 #organization
        week = 0 #week number
        date = 0 #date
        due = 0 #payment due date
        invoice = 0 #invoice number
        address = [] #pay to the order of
        for rx in range(sh.nrows):
            try:
                index = sh.cell_value(rowx=rx, colx=1)
                if isFloat(index):
                    name = sh.cell_value(rowx=rx, colx=2)
                    unit = sh.cell_value(rowx=rx, colx=6)
                    quantity = sh.cell_value(rowx=rx, colx=5)
                    subtotal = sh.cell_value(rowx=rx, colx=7)
                    js = {"number":index,"name":name,"unit":unit,"quantity":quantity,"subtotal":subtotal}
                    js = json.dumps(js) #convert to string
                    jout+=js #append to output string
                    jout+="," #insert seperator
                elif "total payable" in sh.cell_value(rowx=rx, colx=5).lower():
                    total = sh.cell_value(rowx=rx, colx=7)
                elif "organization" in sh.cell_value(rowx=rx, colx=4).lower():
                    org = sh.cell_value(rowx=rx, colx=6)
                elif "week" in sh.cell_value(rowx=rx, colx=4).lower():
                    week = sh.cell_value(rowx=rx, colx=6)
                elif "date" in sh.cell_value(rowx=rx, colx=4).lower():
                    date = sh.cell_value(rowx=rx, colx=6)
                elif "payment due" in sh.cell_value(rowx=rx, colx=2).lower():
                    due = sh.cell_value(rowx=rx, colx=4)
                elif "invoice number" in sh.cell_value(rowx=rx, colx=4).lower():
                    invoice = str(sh.cell_value(rowx=rx, colx=6)) + " "
                    invoice += str(sh.cell_value(rowx=rx, colx=7)) + " "
                    invoice += str(sh.cell_value(rowx=rx, colx=8))
                elif "pay to" in sh.cell_value(rowx=rx, colx=1).lower():
                    for x in range(5):
                        address.append(sh.cell_value(rowx=rx+x+1, colx=1))
            except: #do nothing
                index = 0
        if due == 0:
            if isFloat(date):
                due = date + 30
            else:
                due = str(date) + "+30"
        jout = jout[:-1] #remove last comma
        jout+="],\"total payable\":"
        jout+=str(total)
        jout+=",\"organization\":\""
        jout+=str(org)
        jout+="\",\"week\":\""
        jout+=str(week)
        jout+="\",\"date\":\""
        jout+=str(date)
        jout+="\",\"invoice number\":\""
        jout+=str(invoice)
        jout+="\",\"payment due next 30\":\""
        jout+=str(due)
        jout+="\",\"pay to the order of\":"
        if address != []:
            jout+='['+''.join('\"'+str(x)+'\",' for x in address)
            jout = jout[:-1]
            jout+=']'
        else:
            jout+="\"None\""
        jout+="}"
        jout = json.loads(jout) #to json
        return jout
    except:
        print "failed to read from POD invoice sheet"
        return None
try:
    printAll(sys.argv[1])
except:
    print "Sample usage: python pod.py <file>"
print "Exited."