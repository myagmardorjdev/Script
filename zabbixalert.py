import requests
import json
import pyodbc
import os
import re
from datetime import date 
import base64
import psycopg2
import pypyodbc as odbc
import time
from classes import *
from requests.auth import HTTPBasicAuth
from datetime import datetime,timedelta
sleepsecond = 180
query_error_check = "SELECT * FROM public.action_pull_sync_line where (current_timestamp - (30 * interval '1 minute')) <= create_date and has_error = true and now()>=create_date"
queue_job_error_query = "SELECT * FROM queue_job where state = 'failed'"
query_glpi_id_get= "SELECT id  FROM glpi_tickets ORDER BY id desc LIMIT 1"
now = datetime.now()
seconddate = now + timedelta(days=1)
tdate = "'"+ str(now)[:10]+ "' and '" +str(seconddate)[:10] +"'"
query_glpi_tickets = "SELECT t.id, t.NAME, t.solvedate, t.content , u.name as mail FROM glpi_tickets AS t RIGHT JOIN glpi_users AS u ON t.users_id_recipient = u.id WHERE t.is_deleted = 0 and t.solvedate between " + tdate
log_path = 'B:/zabbixlog.txt'
def initsession():
    url = 'http://10.0.0.14/apirest.php/initSession'
    username = 'zabbix'
    password = 'Aa1234%^'
    headers = {
        'Content-Type': 'application/json',
        #'Authorization': 'user_token Lu0XOm1Bm9Aheza2mPsXyEUfa2jP2renomp2P0hD', #zabbix token
        'Authorization': 'Basic ' + base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8'),
        'App-Token': 'dgoT8fOH3UYbYV1bz49N2PrFUhKY6Bqp8bJgrGRP'
    }
    response = requests.get(url, headers=headers)
    print(response)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data['session_token']
    else:
        print("Error:", response.status_code)
def postg(conn,query):
    global stringa;
    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    #print(len(data))
    #for row in data:
        #print(row)
        #stringa = row;
    return len(data)
    conn.close()
def postg_return_value(conn,query):
    global stringa;
    cursor = conn.cursor()
    cursor.execute(query)

    data = cursor.fetchall()
    #print(len(data))
    #for row in data:
        #print(row)
        #stringa = row;
    conn.close()
    return data
def closeticket(session_token, ticket_id):
    url = f'http://10.0.0.14/apirest.php/Ticket/{ticket_id}'

    # Replace 'your_username' and 'your_password' with your actual GLPI credentials
    username = 'zabbix'
    password = 'Aa1234%^'  # Replace with your actual password
    headers = {
        'Content-Type': 'application/json',
        'App-Token': 'dgoT8fOH3UYbYV1bz49N2PrFUhKY6Bqp8bJgrGRP',
        'Session-Token': session_token
    }

    # Data for closing the ticket (if additional data is required, modify this accordingly)
    close_data = {
        'input': {
            'status': 6,  # Status code for "Closed" (adjust based on your GLPI configuration)
            # You may include other relevant data for closing the ticket
        }
    }

    try:
        response = requests.put(url, json=close_data, headers=headers, auth=HTTPBasicAuth(username, password))

        # Check if the request was successful (status code 200 for OK)
        if response.status_code == 200:
            print(f"Ticket {ticket_id} closed successfully.")
        else:
            print(f"Failed to close ticket. Status code: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")     
def createticket(session_token,title,content,category):
    url = 'http://10.0.0.14/apirest.php/Ticket/'

    # Replace 'your_username' and 'your_password' with your actual GLPI credentials
    username = 'zabbix'
    password = 'Aa1234%^'#'Aa123456!0@'
    headers = {
        'Content-Type': 'application/json',
        'App-Token': 'dgoT8fOH3UYbYV1bz49N2PrFUhKY6Bqp8bJgrGRP',
        'Session-Token' : session_token
    }
    # Data for creating the ticket (replace with actual data)
    ticket_data = {
        'input': {
            'name': title,
            'content': content,
            'priority': 3,  # Replace with the appropriate priority level
            'itemtype': 'Ticket',  # If you are creating a ticket
            'itilcategories_id' : category, #42
            'requesttypes_id' : 12
            # Add other relevant data based on your GLPI setup and requirements
        }
    }

    try:
        response = requests.post(url, json=ticket_data,headers=headers, auth=HTTPBasicAuth(username, password))

        # Check if the request was successful (status code 201 for created)
        if response.status_code == 201:
            data = response.json()
            ticket_id = data['id']
            print(f"Ticket created successfully with ID: {ticket_id}")
        else:
            print(f"Failed to create ticket. Status code: {response.status_code}")
            print(response.json())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
def get_hosts_with_ip(hostid):
    
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'jsonrpc': '2.0',
        'method': 'host.get',
        'params': {
            'output': ['hostid', 'name','value','itemid','status'],
            'selectInterfaces': ['ip'],
            'filter': {
                'hostid': hostid , # Specific hostid you want to fetch
                'status': 0  # тухайн хост enabled or disabled iig ni shalgaj bna
            }
            # Add more parameters or filters as needed
        },
        'auth': AUTHTOKEN,
        'id': 1
    }
    try:
        response = requests.post(ZABBIX_API_URL, json=payload, headers=headers)
        return response.json()['result'][0]['interfaces'][0]['ip']
    except:
        return '0'
def log_write(content,path):
    with open(path, 'a') as f:
        now = datetime.now()
        string = '\n'+str(now) + ' '+ content
        f.write(string)
def log_write_notime(content,path):
    with open(path, 'w') as f:
        string = content
        f.write(string)


salbariinid = readtextfile_to_dict('zabbixphone.txt').returnc()
odoodatabases = {'34': {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'},
                '13': {'user': 'postgres','password': 'postgres','server': '10.13.1.220','port': 5432,'database':'CARREFOURS13_LIVE'},
                '88': {'user': 'readonly_c88','password': 'readonly_c88_password','server': '10.88.1.220','port': 5432,'database':'CARREFOURS88_LIVE'},
                '21': {'user': 'readonly_c21','password': 'readonly_c21_password','server': '10.21.1.220','port': 5432,'database':'CARREFOURS21_LIVE'},
                '01': {'user': 'readonly_c01','password': 'readonly_c01_password','server': '10.1.1.220',  'port': 5432,'database':'STORE01_LIVE'},
                '12': {'user': 'readonly_c42','password': 'readonly_c42_password','server': '10.12.1.220',  'port': 5432,'database':'STORE42_LIVE'},
                '06': {'user': 'readonly_c06','password': 'readonly_c06_password','server': '10.6.1.220',  'port': 5432,'database':'STORE06_LIVE'},
                '17': {'user': 'readonly_c17','password': 'readonly_c17_password','server': '10.17.1.220',  'port': 5432,'database':'STORE17_LIVE'},
                '38': {'user': 'readonly_c38','password': 'readonly_c38_password','server': '10.38.1.220',  'port': 5432,'database':'STORE38_LIVE'},
                '25': {'user': 'readonly_c25','password': 'readonly_c25_password','server': '10.25.1.220',  'port': 5432,'database':'STORE25_LIVE'},
                '26': {'user': 'readonly_c26','password': 'readonly_c26_password','server': '10.26.1.220',  'port': 5432,'database':'STORE26_LIVE'},
                '16': {'user': 'readonly_c16','password': 'readonly_c16_password','server': '10.16.1.220',  'port': 5432,'database':'STORE16_LIVE'},
                '22': {'user': 'readonly_c22','password': 'readonly_c22_password','server': '10.22.1.220',  'port': 5432,'database':'STORE22_LIVE'},
                '08': {'user': 'readonly_c08','password': 'readonly_c08_password','server': '10.8.1.220',  'port': 5432,'database':'STORE08_LIVE'},
                '39': {'user': 'readonly_c39','password': 'readonly_c39_password','server': '10.39.1.220',  'port': 5432,'database':'STORE39_LIVE'},
                '32': {'user': 'itid','password': 'it#2016','server': '10.32.1.220',  'port': 5432,'database':'STORE32_LIVE'},
                '61': {'user': 'itid','password': 'it#2016','server': '10.61.1.220',  'port': 5432,'database':'STORE61_LIVE'},
                '62': {'user': 'itid','password': 'it#2016','server': '10.62.1.220',  'port': 5432,'database':'STORE62_LIVE'},
}
#server = {"server" : "10.34.1.220","database" :"CARREFOURS34_LIVE","user" : "readonly_c34", "password" : "readonly_c34_password"}
bannedhosts = ['AUB_Web']#bannedhosts = ['AJTPowerBI','AUB_Web','itremote','BackupServer','Ysoft','BSO-Printer']
bannedreasons = ['last 24hours']#bannedreasons = ['last 24hours','Client','POS_8320_down','CPU util high','MEM util disaster','CPU util disaster','Free disk']
#loop outsides variables
sessiontoken = initsession()
createdtickets = {}
isrunning_aldaa = {'13':0 , '01':0, '06':0, '08':0 , '16':0 , '17':0 , '21':0, '22':0, '25':0, '26':0, '32':0 , '33':0 , '34':0, '38':0, '39':0,'42':0, '61':0, '62':0}
# ? test 

while(1==1):
    now = datetime.now()
    #print(json.dumps(r2.json(), indent=4, sort_keys=True))
    if now.minute % 10 == 0:
        try:
            sessiontoken = initsession()
        except:
            pass
    # ! glpi solved ticket to teams notifiction 
    if now.hour >=8 and now.hour < 22:
        glpi_tickets_result = ticket_mysql_select(query_glpi_tickets).returnc()
        for i in glpi_tickets_result:
            ticket_title=i[1]
            ticket_content = (i[3]).split(';')[2]
            ticket_mail = i[4] + "@altanjoloo.mn"
            tquery = "select id from dbo.glpi_solved_tickets where id = " + str(i[0])
            tresult = execute_sql_server_select('WIN-3RGEU5J9BNE','callpro','glpi_solved_tickets','sa','SpawnGG123',tquery).returnc()
            if len(tresult) == 0:
                tinsertquery = f"INSERT INTO dbo.glpi_solved_tickets (usermail, title, isSend, body, id,solveddate) VALUES ('" + ticket_mail +"',N'"+i[1]+"',0,N'"+ticket_content+"',"+str(i[0])+",'" +str(now)[:10] +" "+ str(now.hour) + ":"+str(now.minute) +"')"
                execute_sql_server_insert('WIN-3RGEU5J9BNE','callpro','sa','SpawnGG123',tinsertquery)

    # ! callpro call to GLPI ticket bolgoj bna
    if now.hour >=8 and now.hour < 22:
        callprolist=connect_sql_server_select('10.0.99.40','callpro','calllogs','sa','SpawnGG123').returnc()
        for i in range(len(callprolist)):
            last_id = ticket_mysql_select(query_glpi_id_get).returnc()[0][0]+1
            salbarid = 0
            if 'Left' in callprolist[i][0]:
                #zvvnrvv 
                tdata = callprolist[i][1][:62]
                numbers = re.findall(r'\d+', tdata)
                numbers = list(map(int, numbers)) # list shvv
                tempcontent = "Call Pro-гоос : "  + str(numbers[0])
                createticket(sessiontoken,"ЗҮҮН",tempcontent,85)
                if str(numbers[0]) in salbariinid:
                    salbarid = salbariinid[str(numbers[0])]
                ticket_mysql_insert(last_id,"ЗҮҮН",tempcontent,salbarid,85)
                connect_sql_server_update('10.0.99.40','callpro','calllogs','sa','SpawnGG123','Value1',callprolist[i][4])
               
            else:
                tdata = callprolist[i][1][:62]
                numbers = re.findall(r'\d+', tdata)
                numbers = list(map(int, numbers))
                tempcontent = "Call Pro-гоос : "  + str(numbers[0])
                #createticket(sessiontoken,"ЗҮҮН",tempcontent,85)
                if str(numbers[0]) in salbariinid:
                    salbarid = salbariinid[str(numbers[0])]
                ticket_mysql_insert(last_id,"БАРУУН",tempcontent,salbarid,85)

                connect_sql_server_update('10.0.99.40','callpro','calllogs','sa','SpawnGG123','Value1',callprolist[i][4])
                            
    if now.hour >= 8 and now.hour < 22:
        print('Odooo')
        # ? has queue error checking 
        for i in odoodatabases:
            try:
                conp = psycopg2.connect(database=odoodatabases[i]['database'], user=odoodatabases[i]['user'], password=odoodatabases[i]['password'], host=odoodatabases[i]['server'], port= odoodatabases[i]['port'])
                qresult = postg(conp,queue_job_error_query)
            except:
                qresult=0
                pass   
            textname = '//192.168.0.25/sync_pull_log/queuejob_'+ odoodatabases[i]['server'] + '.txt'
            if(qresult == 0):
                log_write_notime("0",textname) 
            else:
                log_write_notime("1",textname) #error toi ved
            time.sleep(1)
        # ? has error checking 
        for i in odoodatabases:
            try:
                conp = psycopg2.connect(database=odoodatabases[i]['database'], user=odoodatabases[i]['user'], password=odoodatabases[i]['password'], host=odoodatabases[i]['server'], port= odoodatabases[i]['port'])
                qresult = postg(conp,query_error_check)
            except:
                qresult = 0
                pass   
            textname = '//192.168.0.25/sync_pull_log/sync_'+ odoodatabases[i]['server'] + '.txt'
            if(qresult == 0):
                log_write_notime("0",textname) 
            else:
                log_write_notime("1",textname) #error toi ved
            time.sleep(1)
        # ? is running 30 minute aas ix baiwal
        is_running_query = "SELECT create_date FROM action_pull_sync_line where  state='in_progress'"# and create_date between" + tdate + "LIMIT 1"   

        for i in odoodatabases:
            now = datetime.now()
            textname = '//192.168.0.25/sync_pull_log/isrun_'+ odoodatabases[i]['server'] + '.txt'     
            try:
                conp = psycopg2.connect(database=odoodatabases[i]['database'], user=odoodatabases[i]['user'], password=odoodatabases[i]['password'], host=odoodatabases[i]['server'], port= odoodatabases[i]['port'])
                qresult = postg_return_value(conp,is_running_query)
                if qresult == []:
                    log_write_notime("0",textname)
                else:
                    # ! baaziin tsag 8 tsagiin zorvvtei baidag bolxoor teriig arilgaj bna
                    qresult2 = qresult[0][0] + timedelta(hours=8)
                    zorvvtsag = now - qresult2
                    if zorvvtsag.total_seconds()/60 >= 5:  # isrunning more than 30minute
                        print("is run for 6 minute: C",i)
                        isrunning_aldaa[i] = isrunning_aldaa[i] + 1

                    if isrunning_aldaa[i] > 10:
                        log_write_notime("1",textname) # isrunning more than 30minute
                    else: 
                        log_write_notime("0",textname)
            except:
                pass
            qresult = []

    if now.hour > 8 and now.hour < 24:
        ZABBIX_API_URL = "http://192.168.0.44:8080/api_jsonrpc.php"
        UNAME = "myagmardorj"
        PWORD = "Az123456!0@"
        AUTHTOKEN = "5bdfed41876263450731478cb62c9826b591bf5c0bba12c0c79eee5e8ec8a979"
        try:
            r = requests.post(ZABBIX_API_URL,
                            json={
                                "jsonrpc": "2.0",
                                "method": "user.login",
                                "params": {
                                    "user": UNAME,
                                    "password": PWORD},
                                "id": 1
                            })
            AUTHTOKEN = r.json()["result"]
        except:
            pass
        
        try:
            r2 = requests.post(ZABBIX_API_URL,
                            json={     
                                "jsonrpc": "2.0",     
                                "method":"problem.get",     
                                "params": {         
                                    #"output": "extend",         "selectDServices": "extend",         "druleids": "19"
                                        "output": "extend",
                                        "selectHosts": ["host", "name",'allowed_hosts','hostid','clock','itemid'],
                                        "interfaces" : ['ip','allowed_hosts','hostid'],
                                        "selectAcknowledges": "extend",
                                        "recent": "true",
                                        "sortfield": ["eventid"],
                                        "sortorder": "ASC",
                                        "severity": 5,
                                    }  ,
                                
                                    "id": 2 ,
                                    "auth": AUTHTOKEN
                            })
            jarray = r2.json()["result"]
        except: 
            pass
        
        
        #Possible values:0 - not classified;1 - information;2 - warning;3 - average;4 - high;5 - disaster.
        severvalue = 4
        counter=0
        ustgax_day_limit = 2
        allproblemdict = {} 
        for i in range(len(jarray)):
            tmp = int(jarray[i]['severity'])
            if tmp > severvalue:
                try:
                    r3 = requests.post(ZABBIX_API_URL,
                                json={     
                                    "jsonrpc": "2.0",     
                                    "method":"event.get",     
                                    "params": {         
                                            "output": ['eventid', 'hostid','name','clock','severity','ip'],
                                            'selectHosts': ['hostid', 'host'],
                                            "select_acknowledges": "extend",         
                                            "selectTags": "extend",        
                                            "eventids": jarray[i]['eventid'] 
                                        }  ,     
                                        "id": 2 ,
                                        "auth": AUTHTOKEN
                                })
                    #print(json.dumps(r3.json(), indent=4, sort_keys=True))
                    
                    eventclock = datetime.fromtimestamp(int(r3.json().get('result')[0]['clock']))
                    now = datetime.now()
                    zorvvtsag = now - eventclock
                    #print(r3.json().get('result')[0]['name'] + ">>>>>>>")

                    # Enabled Disabled item shalgaj bna
                    enedisabled = 0
                    tempip = get_hosts_with_ip( r3.json().get('result')[0].get('hosts')[0].get('hostid'))
                    if tempip == '0':
                        enedisabled = 1                                                                                                                                                                                                     #enedisabled == 0:
                    if all(word not in r3.json().get('result')[0].get('hosts')[0]['host'] for word in bannedhosts) and all(word not in r3.json().get('result')[0]['name'] for word in bannedreasons) and zorvvtsag.total_seconds()/60 >= 15:  # 15 minutaas ix duration problem orj irne
                    
                        eachdict = {
                            "host" : r3.json().get('result')[0].get('hosts')[0]['host'],
                            "reason" : r3.json().get('result')[0]['name'],
                            "ip_address" : tempip
                        }
                    
                        hostname = eachdict['host'][:6]    # salbaraar yalgaj bna
                        if hostname.find('NVR') != -1:     # NVR iig neg salbart olon garj irwel 1 eer duudlaga bvrtgene
                            itsbna = 0
                            for z1 in allproblemdict:
                                if hostname in allproblemdict[z1]['host']:
                                    itsbna = 1
                                    print("host dawxardsan ---- ",hostname," versus ",allproblemdict[z1]['host'])
                                    allproblemdict[z1]['reason'] = allproblemdict[z1]['reason'] + " another host ip:" + eachdict['host']
                                    break
                            if itsbna == 0:
                                counter+=1
                                allproblemdict[counter] = eachdict
                        else:
                            counter+=1
                            allproblemdict[counter] = eachdict
                except:
                    pass
        counter = len(createdtickets)
        isfind = False
        for x in allproblemdict:
            # 2 dict харьцуулж байгаа үгйүг нь шалгаж байна
            for z in createdtickets:
                if allproblemdict[x]['host'] == createdtickets[z]['host'] and allproblemdict[x]['reason'] == createdtickets[z]['reason']:
                    isfind = True
                    break

            # host created ticket dotor baixgvi baiwal shineer vvsgeed, daraa ni vvssen ticket dotor nemj ogj bna
            if isfind == False and ('sync has' in allproblemdict[x]['reason'] or 'isrunning' in allproblemdict[x]['reason']):
                tempcontent = allproblemdict[x]['reason'] +' ip:'+ allproblemdict[x]['ip_address'] 
                if 'sync has' in allproblemdict[x]['reason'] or 'isrunning' in allproblemdict[x]['reason']:
                    title = allproblemdict[x]['reason']
                else: 
                    title = allproblemdict[x]['host']
                #createticket(sessiontoken,title,tempcontent,42)
                print("ticket created   ---" , allproblemdict[x]['host'], ' ', allproblemdict[x]['reason'])
                eachdict1 ={
                    "host" : allproblemdict[x]['host'],
                    "reason" : allproblemdict[x]['reason'],
                    "day": now.day,
                    "ip" : allproblemdict[x]['ip_address'],
                    "hour" : now.hour,
                    "date" : now
                }
                createdtickets[counter] = eachdict1
                counter+=1

            isfind = False
        
        #createdtickets ees hugatsaa ni bolson ticketvvdiig ustgaj bna
        temptickets = {}
        cc = 0
        for z in createdtickets:
            tdate = createdtickets[z]['date']
            zorvvodor = now - tdate
            if zorvvodor.days == 3:
                print("")
            else:
               temptickets[cc] = createdtickets[z]
               cc+=1
        createdtickets = temptickets  # tempticketiig tickets rvv hadgalj bna
                
           
    time.sleep(sleepsecond)
    print(now)
    print("sleeping...")
    log_write("looping ...",log_path)

    if now.hour <= 8:
         isrunning_aldaa = {'13':0 , '01':0, '06':0, '08':0 , '16':0 , '17':0 , '21':0, '22':0, '25':0, '26':0, '32':0 , '33':0 , '34':0, '38':0, '39':0,'42':0, '61':0, '62':0}
