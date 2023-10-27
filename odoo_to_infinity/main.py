file_running_directory = "C:/Users/myagmardorj/Git/lesson3/odoo_to_infinity/"
import psycopg2
from collections import Counter # can count unique value
import os,sys
import pypyodbc as odbc
from decimal import Decimal
sys.path.append(file_running_directory)
import time
import urllib.parse
import requests
from datetime import datetime,timedelta
from lesson3.odoo_to_infinity.functions import find_value_in_list_selected_column
from lesson3.odoo_to_infinity.functions import readtextfile_to_dict
from lesson3.odoo_to_infinity.functions import list_unique_counter
from lesson3.odoo_to_infinity.functions import writetextappend
from lesson3.odoo_to_infinity.functions import read_txt_line_by_line_to_list
from lesson3.odoo_to_infinity.functions import database_insert_new_baraa


# ? >>>>>>>>> QUERY functions
def postg(conn,query):
    global stringa;
    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    #print(len(data))
    #for row in data:
        #print(row)
        #stringa = row;
    return data
    conn.close()                                                          
#! QUERY ZONE
#region 
now = datetime.now()
seconddate = now + timedelta(days=1)
tdate = "'"+ str(now)[:10]+ "' and '" +str(seconddate)[:10] +"'"
                           #0    #1              #2          #3       #4            #5              #6      #7                #8                      #9            #10                   #11            #12              #13              #14             #15         #16         #17
pos_orders_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id,ord.name  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE pos.refunded_orderline_id is null and pos.create_date between "+tdate
pos_payment_query = "SELECT p1.pos_order_id,p1.amount,p2.name,p1.payment_date,p1.is_change FROM pos_payment as p1 inner join pos_payment_method as p2  on p2.id = p1.payment_method_id where p1.payment_date between"+tdate
pos_order_id_query = "SELECT id,bill_id FROM pos_order where name = 'value'"
refund_pos_order_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id,ord.name  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE pos.refunded_orderline_id > 0 and pos.create_date between "+tdate
#endregion
# ? default variables
default_config_dict = readtextfile_to_dict(file_running_directory+"configuration.txt").returnc()
loop_status = 1
success_bill_orders = {}
lines=[]
logpath = file_running_directory+"mainlog.txt"
loop_sleeptime = 120 #second
odoodatabases = {'user': 'readonly_c17','password': 'readonly_c17_password','server': '10.17.1.220','port': 5432,'database':'STORE17_LIVE'}
headers = {"Content-Type": "application/json; charset=utf-8"}
# ! test orchin 
#pos_orders_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id,ord.name  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE ord.bill_id='000002057441017231026001701000218'"

#loop inside
while True:
    now = datetime.now()
    try:
        conp = psycopg2.connect(database=odoodatabases['database'], user=odoodatabases['user'], password=odoodatabases['password'], host=odoodatabases['server'], port= odoodatabases['port'])      
        pos_order_result = postg(conp,pos_orders_query)
        pos_payment_result = postg(conp,pos_payment_query)
        refund_pos_order_result= postg(conp,refund_pos_order_query)
    except:
        writetextappend(str(now) + " " + "ultimate ruu holbogdoj chadsangvi",logpath)  

    # ? cash dr хариулт өгсөн бол хариултын мөрийг арилгаж байна (20000 + -100) = 19900
    for i in list_unique_counter(pos_payment_result,0).returnc():
        totalvalue = 0
        maxvalue = 0
        index_lists = []
        mainid= i
        for j in range(len(pos_payment_result)):
            if (mainid == int(pos_payment_result[j][0]) and pos_payment_result[j][2] == 'Cash'):
                index_lists.append(j)
                totalvalue += float(pos_payment_result[j][1])
                if maxvalue < float(pos_payment_result[j][1]):
                    maxvalue = float(pos_payment_result[j][1]) 

        if maxvalue > totalvalue:
            pos_payment_result.append((pos_payment_result[index_lists[0]][0], totalvalue, pos_payment_result[index_lists[0]][2], pos_payment_result[index_lists[0]][3], pos_payment_result[index_lists[0]][4]))
            indexcounter = 0
            for kk in index_lists:
                pos_payment_result.pop(kk-indexcounter)
                indexcounter+=1

    # ? bill iin medeelliig боловсруулж байна
    for i in list_unique_counter(pos_order_result,9).returnc():
        bill_line = {}
        counter = 0
        SaleItems = {}
        counter2 = 0
        PayItems = {}
        for j in range(len(pos_order_result)):
            if pos_order_result[j][9] == i:
                SaleItems1 = {"Barcode":pos_order_result[j][2],"Qty":f'{pos_order_result[j][6]:.2f}',"ItemDueAmount":float(pos_order_result[j][8])}
                TerminalID = pos_order_result[j][3]#[:4]
                CashierEmpCode = pos_order_result[j][14]
                DDTDNo = pos_order_result[j][16] 
                #SalesDate = (pos_order_result[j][11]).strftime('%Y.%m.%d')
                SaleItems[counter] = SaleItems1
                counter+=1
        for k in range(len(pos_payment_result)):
            if i == pos_payment_result[k][0]:
                # ? Bankii ner oorchilj bna 
                if pos_payment_result[k][2] == "Golomt Bank":
                    paymenttypeid = "GOLOMTCARD"
                elif pos_payment_result[k][2] == "Khan Bank":
                    paymenttypeid = "KHAANCARD"
                elif pos_payment_result[k][2] == "SocialPay":
                    paymenttypeid = "SOCIAL"
                elif pos_payment_result[k][2] == "QPay":
                    paymenttypeid = "QPAY"
                elif pos_payment_result[k][2] == "Cash":
                    paymenttypeid = "CASH"
                else:
                    paymenttypeid = "OTHER"
                PayItems1 = {"PaymentAmount": int(pos_payment_result[k][1]), "PaymentTypeID": paymenttypeid}
                PayItems[counter2] = PayItems1
                counter2+=1
        
        items_sales_total_output = {
        "SaleItems": [
            {
                "Barcode": str(item['Barcode']),
                "Qty":item['Qty'],
                "ItemDueAmount": int(item['ItemDueAmount'])
            }
            for item in SaleItems.values()
        ],
        "SalePayments": [
            {
                "PaymentTypeID": str(item['PaymentTypeID']),
                "PaymentAmount":item['PaymentAmount']
            }
            for item in PayItems.values()
        ]
        }
        items_sales_total_output["TerminalID"] = TerminalID
        items_sales_total_output["CashierEmpCode"] = str(CashierEmpCode)
        items_sales_total_output["DDTDNo"] = DDTDNo
        items_sales_total_output["TxnType"] = "IN"
        items_sales_total_output["SiteId"] = '08'
        #items_sales_total_output["SalesDate"] = SalesDate
        bill_line["Sales"]=[items_sales_total_output]
        bill_line["token"]=default_config_dict['TOKEN'] #bill_line["token"]=urllib.parse.unquote(default_config_dict['TOKEN'])
        #print(bill_line)
        # ? reading pos order_id txt ees unshij bna 
        lines = read_txt_line_by_line_to_list(file_running_directory + default_config_dict['sale_order_textname'],[],'r').returnc()
        if str(i) in lines:
            pass 
        else:
            response = requests.post(default_config_dict['URL'], headers=headers,json=bill_line)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                responsetype = response.json()['retType']
                responseretdesc = response.json()['retDesc']
                if responseretdesc == "Succesfull Executed Query":
                    print("amjilttai hadgallaaa")
                    responseaffectedrows = response.json()['affectedRows']
                    salesNo = response.json()['retData'][0]['SalesNo']
                    lines.append(str(i))
                    print("Bill Number: ",len(lines))
                    read_txt_line_by_line_to_list(file_running_directory + default_config_dict['sale_order_textname'],lines,'w')
                    writetextappend(str(i)+"="+str(salesNo),file_running_directory + 'sales_id.txt')
                    writetextappend(str(now) + " " + str(bill_line) + ";order_id: " +str(i) + ";cashiername: " + str(pos_order_result[j][15]),logpath)
                elif 'бүртгэлгүй' in  responseretdesc:
                    print(' Бүртгэлгүй бараа байна')
                    errorinfo = ' burtgelgvi baraa bna'
                    writetextappend(str(now) + " " + ";order_id: " +str(i) + errorinfo,logpath)
                elif 'Cannot insert' in responseretdesc:
                    print('cannont insert value null into VATIncluded')
                    errorinfo = ' cannont insert value null into VATIncluded'
                    writetextappend(str(now) + " " + ";order_id: " +str(i) + errorinfo,logpath)
            
            
        
    # ? буцаалтын pos orders 
    for i in list_unique_counter(refund_pos_order_result,9).returnc():
        refund_bill_line = {}
        counter = 0
        SaleItems = {}
        counter2 = 0
        PayItems = {}
        for j in range(len(refund_pos_order_result)):
            if refund_pos_order_result[j][9] == i:
                SaleItems1 = {"Barcode":refund_pos_order_result[j][2],"Qty":float(refund_pos_order_result[j][6]),"ItemDueAmount":float(refund_pos_order_result[j][8])}
                CashierEmpCode = refund_pos_order_result[j][14]
                #SalesDate = (refund_pos_order_result[j][11]).strftime('%Y.%m.%d')
                SaleItems[counter] = SaleItems1
                counter+=1 # olon baraatai billiin baraag ni toolj
                # ? finding үндсэн билл ордерийг хайх гэж байна ,  refund order_id өөрөөр үүсдэг юм байна
                billdugaar = (refund_pos_order_result[j][17]).split()[0]
                
                pos_order_id_query2 = pos_order_id_query.replace('value',billdugaar)
                pos_order_id_result = []
                pos_order_id_result = postg(conp,pos_order_id_query2)
                sales_id_list = readtextfile_to_dict(file_running_directory+"sales_id.txt").returnc()
                # ? бид энэ order_id g ашиглан sales_id дотроос order_id and нубиагаас өгсөн борлуулалтын id-гаар солих боломжтой
                print("order id: ", pos_order_id_result)
                sales_id = sales_id_list[str(pos_order_id_result[0][0])]
                DDTDNo = pos_order_id_result[0][1] 
                TerminalID = billdugaar.split('/')[0]
        for k in range(len(pos_payment_result)):
            if i == pos_payment_result[k][0]:
                 # ? Bankii ner oorchilj bna 
                if pos_payment_result[k][2] == "Golomt Bank":
                    paymenttypeid = "GOLOMTCARD"
                elif pos_payment_result[k][2] == "Khan Bank":
                    paymenttypeid = "KHAANCARD"
                elif pos_payment_result[k][2] == "SocialPay":
                    paymenttypeid = "SOCIAL"
                elif pos_payment_result[k][2] == "QPay":
                    paymenttypeid = "QPAY"
                elif pos_payment_result[k][2] == "Cash":
                    paymenttypeid = "CASH"
                else:
                    paymenttypeid = "OTHER"
                PayItems1 = {"PaymentAmount": int(pos_payment_result[k][1]), "PaymentTypeID": paymenttypeid}
                PayItems[counter2] = PayItems1
                counter2+=1
        
        refund_total_orders = {
        "SaleItems": [
            {
                "Barcode": str(item['Barcode']),
                "Qty":item['Qty'] if item['Qty'] > 0 else item['Qty']*-1,
                "ItemDueAmount": int(item['ItemDueAmount']) if item['ItemDueAmount'] > 0 else item['ItemDueAmount']*-1
            }
            for item in SaleItems.values()
        ],
        "SalePayments": [
            {
                "PaymentTypeID": str(item['PaymentTypeID']),
                "PaymentAmount":item['PaymentAmount'] if item['PaymentAmount'] > 0 else item['PaymentAmount']*-1
            }
            for item in PayItems.values()
        ]
        }
        refund_total_orders["TerminalID"] = TerminalID
        refund_total_orders["CashierEmpCode"] = CashierEmpCode
        refund_total_orders["DDTDNo"] = DDTDNo
        refund_total_orders["TxnType"] = "CM"
        refund_total_orders["SalesNo"] = sales_id
        #refund_total_orders["SalesDate"] = SalesDate
        refund_bill_line["Sales"]=[refund_total_orders]
        refund_bill_line["token"]=default_config_dict['TOKEN']
        #print(bill_line)  
        # ? буцаалтын биллийг txt data -тай тулгаж , байхгүй бол текстэнд хадгалж байна
        lines = read_txt_line_by_line_to_list(file_running_directory + default_config_dict['refund_order_textname'],[],'r').returnc()
        if str(i) in lines:
            pass 
        else:
            response = requests.post(default_config_dict['URL'], headers=headers,json=refund_bill_line)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                responsetype = response.json()['retType']
                responseretdesc = response.json()['retDesc']
                if responseretdesc == "Succesfull Executed Query":
                    print("amjilttai hadgallaaa")
                    responseaffectedrows = response.json()['affectedRows']
                    salesNo = response.json()['retData'][0]['SalesNo'] 
                    lines.append(str(i))
                    writetextappend(str(now) + " refund;" + str(refund_bill_line) + ';order_id: ' + str(pos_order_id_result[0][0]),logpath)
                    writetextappend(str(i)+"="+str(salesNo),file_running_directory + default_config_dict['sales_id_ref'])
                else:
                    writetextappend(str(now) + " refund aldaa " + ';order_id: ' + str(pos_order_id_result[0][0]),logpath)
            read_txt_line_by_line_to_list(file_running_directory + default_config_dict['refund_order_textname'],lines,'w')
          
        
    # ! omnox odriin bill vvdiig ustgaj bna
    if now.hour == 0 and now.minute <= (loop_sleeptime/60):
        os.remove(file_running_directory + default_config_dict['sale_order_textname'])
        with open(file_running_directory + default_config_dict['sale_order_textname'], 'w') as f:
            pass
        os.remove(file_running_directory + default_config_dict['refund_order_textname'])
        with open(file_running_directory + default_config_dict['refund_order_textname'], 'w') as f:
            pass   
    print("sleeping...")
    time.sleep(loop_sleeptime)


    

    
