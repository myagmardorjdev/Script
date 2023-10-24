import time
import random,sys
import os
import sqlite3
from datetime import datetime
import random
import string
import pandas as pd
from typing import Any


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
        return self.value

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

class get_uid_on_selected_table():
    def __init__(self,db,table,column):
        self.databasename = db
        self.table = table 
        self.column = column
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        self.query = "SELECT " + column + " FROM " + self.table
        self.c.execute(self.query)
        self.conn.commit()
        self.conn.close()
    
    def returnc(self):
        return self.c

class creating_default_database_tables():
    def __init__(self,name):
        self.databasename= name
        self.conn = sqlite3.connect(self.databasename)
        self.query = "CREATE TABLE IF NOT EXISTS baraanuud (barcode        TEXT (16)  NOT NULL UNIQUE,name           TEXT (255),relatedbarcode TEXT (255),isActive       INTEGER    DEFAULT (1),isVat          INTEGER    DEFAULT (1),isFraction     INTEGER    DEFAULT (0),Category       TEXT (255) DEFAULT nogroup,uid  INTEGER);"
        self.conn.execute(self.query)
        
        self.conn.close()

class database_insert_new_baraa():
    def __init__(self,basename,tablename,barcode,price,name,relbarcode,fraction):
        self.barcode = barcode
        self.price = price
        self.name = name
        self.stringdate = now_date_to_text_date().returnc()
        self.pkid = generatepkid().returnc()
        self.fraction = fraction
        self.relbarcode = relbarcode
        self.tablename = tablename
        self.databasename= basename
        self.conn = sqlite3.connect(self.databasename)
        self.c = self.conn.cursor()
        self.query = "INSERT INTO " + self.tablename +"(barcode,name,relatedbarcode,isFraction,uid,date) "+ " Values(" +str(self.barcode)  +",'" +self.name +"','" + self.relbarcode+ "'," +str(self.fraction)+ ","+str(self.pkid) +",'"+ self.stringdate +"')"
        print(self.query)
        self.c.execute(self.query)
        self.conn.commit()
        self.conn.close()
    
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

creating_default_database_tables("handodatabase")
#database_insert_new_baraa("handodatabase","baraanuud",8606004234634,22300,'Ааруул','n',0)
get_uid_on_selected_table("handodatabase","baraanuud",'uid').returnc()