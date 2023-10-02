file_running_directory = "C:/Users/myagmardorj/Git/lesson3/odoo_to_infinity/"
import psycopg2
import os,sys
import pypyodbc as odbc
sys.path.append(file_running_directory)
from datetime import datetime,timedelta
from lesson3.odoo_to_infinity.functions import readtextfile_to_dict

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
pos_orders_query = "SELECT pos.id,pos.company_id,pro.barcode,pos.name,pos.product_id,pos.price_unit,pos.qty,pos.price_subtotal,pos.price_subtotal_incl,pos.order_id,pos.full_product_name,pos.create_date FROM pos_order_line as pos inner join product_product pro on pos.product_id = pro.id WHERE pos.create_date between "+tdate
# ? default variables
default_config_dict = readtextfile_to_dict(file_running_directory+"configuration.txt").returnc()
loop_status = 1
loop_sleeptime = 2 #second
odoodatabases = {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'}

conp = psycopg2.connect(database=odoodatabases['database'], user=odoodatabases['user'], password=odoodatabases['password'], host=odoodatabases['server'], port= odoodatabases['port'])
qresult = postg(conp,pos_orders_query)
print(qresult[0])
