import time
import random,sys
import os
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
    
class find_value_in_list_selected_column(): # ? 2 хэмжээст листнээс баганаа сонгож тэндээс ХАЙЖ буй тоо байвал мөрөн листыг буцаана
    def __init__(self,value,listname,index):
        self.value = value
        self.index = index
        self.list = listname
        self.resultlist = []
        self.resultlist = [sublist for sublist in self.list if sublist[self.index] == self.value]

    def returnc(self):
        return self.resultlist

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

class connect_sql_server_select():
    def __init__(self,server,database,table,username,password):
        self.server = server  # Replace 'server_name' with the name or IP address of your SQL Server
        self.database = database  # Replace 'database_name' with the name of your database
        self.username = username # Replace 'username' with your SQL Server username
        self.password = password  # Replace 'password' with your SQL Server password
        self.table = table
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)

        # Create a cursor object using the cursor() method
        cursor = conn.cursor()
        print('SELECT * FROM '+self.table + 'WHere isTicket = 0')
        # Execute SQL queries
        cursor.execute('SELECT * FROM '+self.table + ' WHere isTicket = 0')  # Replace 'your_table_name' with the name of your table
        self.result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()
    def returnc(self):
        return self.result
class connect_sql_server_insert():
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
    