file_running_directory = "C:/Users/myagmardorj/Git/lesson3/odoo_to_infinity/"
import psycopg2
from collections import Counter # can count unique value
import os,sys
import pypyodbc as odbc
sys.path.append(file_running_directory)
from datetime import datetime,timedelta
from lesson3.odoo_to_infinity.functions import readtextfile_to_dict
from lesson3.odoo_to_infinity.functions import list_unique_counter
from lesson3.odoo_to_infinity.functions import list_unique_count_sum

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
pos_orders_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date,ord.amount_paid,ord.pos_reference,ord.employee_id,ord.cashier,ord.bill_id  FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id inner join pos_order as ord on ord.id = pos.order_id WHERE pos.create_date between "+tdate
pos_payment_query = "SELECT p1.pos_order_id,p1.amount,p2.name,p1.payment_date,p1.is_change FROM pos_payment as p1 inner join pos_payment_method as p2  on p2.id = p1.payment_method_id where p1.payment_date between"+tdate
# ? default variables
default_config_dict = readtextfile_to_dict(file_running_directory+"configuration.txt").returnc()
loop_status = 1
loop_sleeptime = 2 #second
odoodatabases = {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'}

#loop inside
conp = psycopg2.connect(database=odoodatabases['database'], user=odoodatabases['user'], password=odoodatabases['password'], host=odoodatabases['server'], port= odoodatabases['port'])
pos_order_result = postg(conp,pos_orders_query)
pos_payment_result = postg(conp,pos_payment_query)
print(pos_order_result[0][3])

for i in list_unique_counter(pos_order_result,9).returnc():
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
            PayItems1 = {"PaymentTypeID": int(pos_payment_result[k][1]), "PaymentAmount": pos_payment_result[k][2]}
            PayItems[counter2] = PayItems1
            counter2+=1
    if(i == 397345):
        
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

        print(items_sales_total_output)




