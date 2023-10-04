file_running_directory = "C:/Users/myagmardorj/Git/lesson3/odoo_to_infinity/"
import psycopg2
from collections import Counter # can count unique value
import os,sys
import pypyodbc as odbc
from decimal import Decimal
sys.path.append(file_running_directory)
from datetime import datetime,timedelta
from lesson3.odoo_to_infinity.functions import readtextfile_to_dict
from lesson3.odoo_to_infinity.functions import list_unique_counter

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
# ? <<<<<<<<<<<<<<<<<<<<  QUERY functions
# ! region QUERY ZONE
now = datetime.now()
seconddate = now + timedelta(days=1)
tdate = "'"+ str(now)[:10]+ "' and '" +str(seconddate)[:10] +"'"
                           #0    #1              #2          #3       #4            #5              #6      #7                #8                      #9            #10                   #11            #12              #13              #14             #15         #16 
pos_orders_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE pos.refunded_orderline_id is null and pos.create_date between "+tdate
pos_payment_query = "SELECT p1.pos_order_id,p1.amount,p2.name,p1.payment_date,p1.is_change FROM pos_payment as p1 inner join pos_payment_method as p2  on p2.id = p1.payment_method_id where refunded_orderline_id is null and p1.payment_date between"+tdate

refund_pos_order_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE refunded_orderline_id > 0 and pos.create_date between "+tdate

# ? default variables
default_config_dict = readtextfile_to_dict(file_running_directory+"configuration.txt").returnc()
loop_status = 1
success_bill_orders = {}
loop_sleeptime = 2 #second
odoodatabases = {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'}

#loop inside
conp = psycopg2.connect(database=odoodatabases['database'], user=odoodatabases['user'], password=odoodatabases['password'], host=odoodatabases['server'], port= odoodatabases['port'])
pos_order_result = postg(conp,pos_orders_query)
pos_payment_result = postg(conp,pos_payment_query)
refund_pos_payment_result= postg(conp,refund_pos_payment_query)
# ? буцаалтын payment
for i in list_unique_counter(pos_payment_result,0).returnc():
    totalvalue = 0
    maxvalue = 0
    index_lists = []
    mainid= i
    for j in range(len(pos_payment_result)):
        if (mainid == int(pos_payment_result[j][0]) and pos_payment_result[j][2] == 'Cash'):
            index_lists.append(j)
            print("main id ",mainid)
            print("gg : ", pos_payment_result[j])
            totalvalue += float(pos_payment_result[j][1])
            if maxvalue < float(pos_payment_result[j][1]):
                maxvalue = float(pos_payment_result[j][1]) 

    if maxvalue > totalvalue:
        pos_payment_result.append((pos_payment_result[index_lists[0]][0], totalvalue, pos_payment_result[index_lists[0]][2], pos_payment_result[index_lists[0]][3], pos_payment_result[index_lists[0]][4]))
        indexcounter = 0
        print("indexs ",index_lists)
        print("listindex> ",index_lists)
        for kk in index_lists:
            pos_payment_result.pop(kk-indexcounter)
            indexcounter+=1

# ? cash dr хариулт өгсөн бол хариултын мөрийг арилгаж байна (20000 + -100) = 19900
for i in list_unique_counter(pos_payment_result,0).returnc():
    totalvalue = 0
    maxvalue = 0
    index_lists = []
    mainid= i
    for j in range(len(pos_payment_result)):
        if (mainid == int(pos_payment_result[j][0]) and pos_payment_result[j][2] == 'Cash'):
            index_lists.append(j)
            print("main id ",mainid)
            print("gg : ", pos_payment_result[j])
            totalvalue += float(pos_payment_result[j][1])
            if maxvalue < float(pos_payment_result[j][1]):
                maxvalue = float(pos_payment_result[j][1]) 

    if maxvalue > totalvalue:
        pos_payment_result.append((pos_payment_result[index_lists[0]][0], totalvalue, pos_payment_result[index_lists[0]][2], pos_payment_result[index_lists[0]][3], pos_payment_result[index_lists[0]][4]))
        indexcounter = 0
        print("indexs ",index_lists)
        print("listindex> ",index_lists)
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
            SaleItems1 = {"Barcode":pos_order_result[j][2],"Qty":float(pos_order_result[j][6]),"ItemDueAmount":float(pos_order_result[j][8])}
            TerminalID = pos_order_result[j][3][:4]
            CashierEmpCode = pos_order_result[j][14]
            DDTDNo = pos_order_result[j][16] 
            SalesDate = (pos_order_result[j][11]).strftime('%Y.%m.%d')
            SaleItems[counter] = SaleItems1
            counter+=1
    for k in range(len(pos_payment_result)):
        if i == pos_payment_result[k][0]:
            PayItems1 = {"PaymentAmount": int(pos_payment_result[k][1]), "PaymentTypeID": pos_payment_result[k][2]}
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
    items_sales_total_output["CashierEmpCode"] = CashierEmpCode
    items_sales_total_output["DDTDNo"] = DDTDNo
    items_sales_total_output["TxnType"] = "IN"
    items_sales_total_output["SalesDate"] = SalesDate
    bill_line["Sales"]=[items_sales_total_output]
    bill_line["token"]=default_config_dict['TOKEN']
    #print(bill_line)




#Refunded Orders