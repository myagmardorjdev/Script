file_running_directory = "C:/Users/myagmardorj/Git/lesson3/odoo_to_infinity/"
import time
import random,sys
import requests
import os
from requests.auth import HTTPBasicAuth
import json
import pyodbc
import openpyxl
import sqlite3
from datetime import datetime
import random
import string
import pandas as pd
from typing import Any
from zipfile import ZipFile 



class getfilesize():
    def __init__(self,path,size):
        self.type = size
        self.divider = 1
        self.ans = 0
        self.divider = 1024 if self.type == 'kb' else (1024*1024 if self.type == 'mb' else (1024*1024*1024 if self.type == 'gb' else 1))

        try:
            self.ans = os.path.getsize(path)/self.divider
        except FileNotFoundError:
            print("File not found.")
        except OSError:
            print("OS error occurred.")
    def returnc(self):
        return self.ans
    
class find_value_in_list_selected_column(): # ? 2 хэмжээст листнээс баганаа сонгож тэндээс ХАЙЖ буй тоо байвал мөрөн листыг бүтнээр нь буцаана
    def __init__(self,value,listname,index):
        self.value = value
        self.index = index
        self.list = listname
        self.resultlist = []
        self.resultlist = [sublist for sublist in self.list if sublist[self.index] == self.value]

    def returnc(self):
        return self.resultlist

class get_index_list_selected_column(): # ? 2 хэмжээст листнээс баганаа сонгож тэндээс ХАЙЖ буй тоо байвал index -ыг буцаана 
    def __init__(self,value,listname,index):
        self.value = value 
        self.listname = listname 
        self.index = index 
        self.returnvalue = -1
        for i in range(len(self.listname)):
            if self.listname[i][index] == self.value:
                self.returnvalue = i 
                break
    def returnc(self):
        return self.returnvalue 
    
class read_txt_line_by_line_to_list(): # ? доошоо урссан текст тоонуудыг уншиж листэнд хадгалж буцаана
    def __init__(self,value,list,type):
        if type == 'r':
            self.filepath = value
            with open(self.filepath, 'r') as file:
                self.lines = [line.strip() for line in file.readlines()]
        else: 
            self.filepath = value
            with open(self.filepath, 'w') as file:
                for line in list:
                    file.write(line + '\n')
    def returnc(self):
        return self.lines

class list_unique_counter(): # ? list байдлаар давтагдахгүй дугааруудыг буцаана.
    def __init__(self, listname,index):
        self.content = listname
        self.index = index
        self.checkvalues = []
        for i in range(len(self.content)):
            if self.content[i][self.index] in self.checkvalues:
                pass
            else:
                self.checkvalues.append(self.content[i][self.index])
    def returnc(self):
        return self.checkvalues

class writetextnew():                                                                               
    def __init__(self, content,path):
        self.path = path
        self.content =content
        with open(self.path, 'w') as f:
            string = self.content
            f.write(string)

class writetextappend():                                                                               
    def __init__(self, content,path):
        self.path = path
        self.content = "\n" + content
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                pass
                print('null')
        with open(self.path,'a',encoding="utf-8") as f:
            string = self.content
            f.writelines(string)

class generatepkid():
    def __init__(self):
        self.now = datetime.now()
        self.genid = random.randint(100,999)
        self.value = (str(self.now.year) + ("0" if self.now.month < 10 else "") + str(self.now.month)+("0" if self.now.day < 10 else "")+str(self.now.day)+("0" if self.now.hour < 10 else "")+str(self.now.hour)+("0" if self.now.minute < 10 else "")+str(self.now.minute)+("0" if self.now.second < 10 else "")+str(self.now.second)+ str(self.genid))
    
    def returnc(self):
        return int(self.value)

class readtextfile_to_dict():  #? текст файлыг уншиж dic хэлбэрээр буцаана                                                                             
    def __init__(self, value):
        self.filename = value
        self.contents = []
        self.configuredict = {}
        self.read_file_contents()

    def read_file_contents(self):
        with open(self.filename, 'r') as f:
            self.contents = f.readlines()

    def returnc(self):
        for i in range(len(self.contents)):
            ind = self.contents[i].strip().find('=') 
            if ind != -1:
                self.configuredict[(self.contents[i].strip()[:ind]).strip()]=(self.contents[i].strip()[ind+1:]).strip()
        return self.configuredict

class generate_random_string(): # ? нууц үгийн зориулалтаар санамсаргүй текст үүсгэж өгнө
    def __init__(self,length):
        self.lenght = length
        self.characters = string.ascii_letters + string.digits  # You can customize this string to include more characters if needed
        self.random_string = ''.join(random.choice(self.characters) for _ in range(self.lenght))
    def returnc(self):
        return self.random_string

class now_date_to_text_date():
    def __init__(self):
        self.now = datetime.now()
        self.value = str(self.now.year) + "-" + str(self.now.month) +'-'+str(self.now.day)+' '+str(self.now.hour)+':'+str(self.now.minute)+':'+str(self.now.second)
    def returnc(self):
        return self.value

class text_date_to_now_date():
    def __init__(self,date):
        self.date = date
        self.format = '%Y-%m-%d %H:%M:%S'
        self.realdate = datetime.strptime(self.date, self.format)
    def returnc(self):
        return self.realdate


    def __init__(self,server,database,table,username,password,column,compare):
        self.server = server  # Replace 'server_name' with the name or IP address of your SQL Server
        self.database = database  # Replace 'database_name' with the name of your database
        self.username = username # Replace 'username' with your SQL Server username
        self.password = password  # Replace 'password' with your SQL Server password
        self.table = table
        self.column= column 
        self.compare = compare
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)

        # Create a cursor object using the cursor() method
        self.cursor = self.conn.cursor()
        print("update calllogs set isTicket = 1 where " + self.column + " = '" +self.compare+"'")
        # Execute SQL queries
        self.cursor.execute("update calllogs set isTicket = 1 where " + self.column + " = '" +self.compare+"'")  # Replace 'your_table_name' with the name of your table
        self.conn.commit()

        # Close the cursor and connection
        self.cursor.close()
        self.close()

class ticket_mysql_insert():
    def __init__(self,item_id,title,content,entity,category):
        #self.query_get_lastid_glpi = query
        self.title = title
        now = datetime.now()
        self.content = content
        self.entity = entity
        self.id = item_id
        self.category = category
        config = {
            'user': 'it',
            'password': 'password',
            'host': '10.0.0.14',
            'database': 'glpidb',
            'raise_on_warnings': True
        }
        try:
            connection = mysql.connector.connect(**config)
            # Create a cursor object
            cursor = connection.cursor()
            insert_query = "INSERT INTO glpi_tickets (id, name, content, entities_id, itilcategories_id,date,date_mod,priority) VALUES (%s,%s, %s, %s, %s,%s,%s,%s)"
 
 
            cursor.execute(insert_query, (self.id,self.title,self.content,self.entity,self.category,now_date_to_text_date().returnc(),now_date_to_text_date().returnc(),3))
 
 
            connection.commit()
            # Fetch and print the inserted data
           
        except mysql.connector.Error as error:
            print("Error: {}".format(error))
 
        finally:
            # Close the cursor and connection
            if connection.is_connected():
                cursor.close()
                connection.close()    

class dict_to_text_file_save():                                                                               
    def __init__(self, filename,dictname):
        self.path = filename
        self.dic = dictname
        with open(self.path, 'w') as f:
                pass
        for key,i in self.dic.items():
            self.dt = "\n"+key + "=" + i 
            with open(self.path,'a',encoding="utf-8") as f:
                f.writelines(self.dt)

default_config_dict = readtextfile_to_dict(file_running_directory+"configuration.txt").returnc()


class add_new_baraa_to_ultimate_pos_api():
    def __init__(self, barcode,taxbarcode,itemname,MaterialType,ClassID,SalesUnitID,PSprice,SOPrice,isNoatus,NoatRegister):
        self.barcode = barcode
        self.taxbarcode = taxbarcode # Такс код "ДОТООД КОД байж болно"
        self.Descr = itemname # Барааны нэр 
        self.MaterialType = '2052041' # Ангилал код  # department id gaar oruulya # 2052041
        self.ClassID = ClassID #Категори ID  "product_template # Group Category 
        self.VendID = '0004' # Нийлүүлэгч код  DEFAULT '0004'
        self.PrimaryBinCode = '001' # Үндсэн байршил DEFAULT '001'
        self.SalesUnitID = SalesUnitID #Хэмжих нэгж   , Шир EA,KG   # uom_id = 1 EA , 12 KG
        self.PSPrice = PSprice # Борлуулалтын үнэ 
        self.SOPrice = SOPrice # Худалдан авалтын үнэ  
        self.isNoatus = isNoatus # Нөат төлөгч эсэх  Y , N  tax_id = 4 baiwal нөатгүй
        self.NoatRegister = NoatRegister # Байгууллагын регистер 
        self.headers = {"Content-Type": "application/json; charset=utf-8"}
        self.mainjson = {}
        self.mainjson['token'] = default_config_dict['TOKEN']
        self.inv2 = {}
        self.inv2['BarCode'] = self.barcode
        self.inv2['TaxBarCode'] = self.taxbarcode
        self.inv2['Descr'] = self.Descr
        self.inv2['MaterialType'] = self.MaterialType
        self.inv2['ClassID'] = self.ClassID
        self.inv2['VendID'] = self.VendID 
        self.inv2['PrimaryBinCode'] = self.PrimaryBinCode
        self.inv2['SalesUnitID'] = self.SalesUnitID
        self.inv2['PSPrice'] = self.PSPrice
        self.inv2['SOPrice'] = self.SOPrice
        self.inv2['isNoatus'] = 'Y'
        self.inv2['NoatRegister'] = self.NoatRegister
        self.inv = [self.inv2]
        self.mainjson['Inventory'] = self.inv 
        print('---------------------------')
        try:
            self.response = requests.post(default_config_dict['URLventory'], headers=self.headers,json=self.mainjson)
            self.data_dict = json.loads(self.response.text)
        except:
            self.data_dict = []
            pass
        print(self.data_dict)
    def returnc(self):
        return self.data_dict

class get_baraa_info_ultimate_pos_api():
    def __init__(self, fieldname,barcode,withfilter):
        self.fieldname = fieldname
        self.barcode = barcode
        self.isyes = 'Y' if withfilter > 0 else 'N'
        self.url = default_config_dict['URLinv'] + '?token='
        
        if self.isyes == 'Y':
            self.url = self.url + default_config_dict['TOKEN']+'&IsFilter=Y&FieldName='+self.fieldname+'&Value='+self.barcode
        else:
            self.url = self.url + default_config_dict['TOKEN']+'&IsFilter=N&FieldName='+self.fieldname+'&Value='+self.barcode

        try:
            self.response = requests.get(self.url)
            self.data_dict = json.loads(self.response.text)

            self.ret_type = self.data_dict['retType']
            self.ret_desc = self.data_dict['retDesc']
            self.ret_data = self.data_dict['retData']
            print(self.ret_data)
        except:
            self.ret_data = []
            pass
        
    def returnc(self):
        return self.ret_data

class UpdateBaraaPriceToUltimatePosAPI():
    def __init__(self, invtid, Unitid, nnewcost, nstandardprice, versionid):
        self.invtid = invtid  # барааны код
        self.unitid = Unitid  # хэмжих нэгж
        self.nnewcost = '0' # nnewcost should be an integer, convert it from string
        self.versionid = versionid  # versionid should be an integer, convert it from string
        self.nstandardprice = nstandardprice  # ПОС-ын үнэ should be an integer, convert it from string
        self.mainjson = {}
        self.mainjson['token'] = default_config_dict['TOKEN']
        self.mainjson['VersionID'] = self.versionid
        self.psSalesPrice = {}
        self.psSalesPrice['InvtID'] = self.invtid
        self.psSalesPrice['UnitID'] = self.unitid
        self.psSalesPrice['NNewCost'] = self.nnewcost
        self.psSalesPrice['NStandardPrice'] = self.nstandardprice
        self.inve2 = {}
        self.inve2['psSalesPrice'] = self.psSalesPrice
        self.mainjson['InventoryProduct'] = [self.inve2]
        print('---------------------------')
        try:
            self.response = requests.post(default_config_dict['URLchange'], headers=self.headers,json=self.mainjson)
            self.data_dict = json.loads(self.response.text)
        except:
            self.data_dict = []
            pass
        print(self.data_dict)
    def returnc(self):
        return self.data_dict
# Create an instance of the class with appropriate arguments

