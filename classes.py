from datetime import date 
import base64
from datetime import datetime,timedelta
import pyodbc
import mysql.connector
import psycopg2

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
        self.conn.close()
class now_date_to_text_date():
    def __init__(self):
        self.now = datetime.now()
        self.value = str(self.now.year) + "-" + str(self.now.month) +'-'+str(self.now.day)+' '+str(self.now.hour)+':'+str(self.now.minute)+':'+str(self.now.second)
    def returnc(self):
        return self.value
class ticket_mysql_select():
    def __init__(self,query):
        self.query_get_lastid_glpi = query
        self.data = []
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

            connection.commit()
            # Fetch and print the inserted data
            cursor.execute(self.query_get_lastid_glpi)
            records = cursor.fetchall()
            for row in records:
                self.data.append(row)
        except mysql.connector.Error as error:
            print("Error: {}".format(error))

        finally:
            # Close the cursor and connection
            if connection.is_connected():
                cursor.close()
                connection.close() 

    def returnc(self):
        return self.data
        pass
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

