import requests
import json
import os
import base64
import psycopg2
import pypyodbc as odbc
import time
from requests.auth import HTTPBasicAuth
from datetime import datetime,timedelta
sleepsecond = 120

query_error_check = "SELECT * FROM public.action_pull_sync_line where (current_timestamp - (540 * interval '1 minute')) <= create_date and has_error = true"
log_path = 'B:/zabbixlog.txt'
def initsession():
    url = 'http://10.0.0.14/apirest.php/initSession'
    username = 'zabbix'
    password = 'Aa123456!0@'
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
    return data
    conn.close()

def createticket(session_token,title,content):
    url = 'http://10.0.0.14/apirest.php/Ticket/'

    # Replace 'your_username' and 'your_password' with your actual GLPI credentials
    username = 'zabbix'
    password = 'Aa123456!0@'
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
            'itilcategories_id' : 42,
            'requesttypes_id' : 12,
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

odoodatabases = {0: {'user': 'readonly_c34','password': 'readonly_c34_password','server': '10.34.1.220','port': 5432,'database':'CARREFOURS34_LIVE'},
                1: {'user': 'postgres','password': 'postgres','server': '10.13.1.220','port': 5432,'database':'CARREFOURS13_LIVE'},
                2: {'user': 'readonly_c88','password': 'readonly_c88_password','server': '10.88.1.220','port': 5432,'database':'CARREFOURS88_LIVE'},
                3: {'user': 'readonly_c21','password': 'readonly_c21_password','server': '10.21.1.220','port': 5432,'database':'CARREFOURS21_LIVE'},
                4: {'user': 'readonly_c01','password': 'readonly_c01_password','server': '10.1.1.220',  'port': 5432,'database':'STORE01_LIVE'},
                5: {'user': 'readonly_c42','password': 'readonly_c42_password','server': '10.12.1.220',  'port': 5432,'database':'STORE42_LIVE'},
                6: {'user': 'readonly_c06','password': 'readonly_c06_password','server': '10.6.1.220',  'port': 5432,'database':'STORE06_LIVE'}
}
#server = {"server" : "10.34.1.220","database" :"CARREFOURS34_LIVE","user" : "readonly_c34", "password" : "readonly_c34_password"}
bannedhosts = ['PowerBI2','AJTPowerBI','AUB_Web','itremote','BackupServer','PowerBI2','Ysoft','BSO-Printer']
bannedreasons = ['last 24hours','Client','POS_8080_down','CPU util high','MEM util disaster','CPU util disaster','Free disk']
#loop outsides variables
sessiontoken = initsession()
createdtickets = {}


while(1==1):
    now = datetime.now()

    if now.hour > 8 and now.hour < 20:
        # ? has error checking 
        for i in range(len(odoodatabases)):
            try:
                conp = psycopg2.connect(database=odoodatabases[i]['database'], user=odoodatabases[i]['user'], password=odoodatabases[i]['password'], host=odoodatabases[i]['server'], port= odoodatabases[i]['port'])
                qresult = postg(conp,query_error_check)
            except:
                pass   
            textname = '//192.168.0.25/sync_pull_log/sync_'+ odoodatabases[i]['server'] + '.txt'
            if(qresult == 0):
                log_write_notime("0",textname) 
            else:
                log_write_notime("1",textname) #error toi ved
            time.sleep(1)
        # ? is running 30 minute aas ix baiwal
        seconddate = now + timedelta(days=1)
        tdate = "'"+ str(now)[:10]+ "' and '" +str(seconddate)[:10] +"'"
        is_running_query = "SELECT create_date FROM action_pull_sync_line where  state='in_progress' and create_date between" + tdate + "LIMIT 1"   
        qresult = []
        for i in range(len(odoodatabases)):
            textname = '//192.168.0.25/sync_pull_log/isrun_'+ odoodatabases[i]['server'] + '.txt'      
            try:
                conp = psycopg2.connect(database=odoodatabases[i]['database'], user=odoodatabases[i]['user'], password=odoodatabases[i]['password'], host=odoodatabases[i]['server'], port= odoodatabases[i]['port'])
                qresult = postg_return_value(conp,is_running_query)
                if qresult == []:
                    print('null bna')
                    log_write_notime("0",textname)
                else:
                    print(odoodatabases[i]['database'])
                    zorvvtsag = now - qresult[0][0]
                    if zorvvtsag.seconds/60 > 30:
                        log_write_notime("1",textname) # isrunning more than 30minute
                    else: 
                        log_write_notime("0",textname)
            except:
                pass
            qresult = []

    if now.hour > 8 and now.hour < 24:
        ZABBIX_API_URL = "http://192.168.0.44:8080/zabbix/api_jsonrpc.php"
        UNAME = "myagmardorj"
        PWORD = "Az123456!0@"
        AUTHTOKEN = "56bc1ff73deb2c79145b1e8315a064e8e967251e2d4b60f0d1207c077ea2a5ef"

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
        #print(json.dumps(r2.json(), indent=4, sort_keys=True))
        if now.minute % 10 == 0:
            sessiontoken = initsession()
        jarray = r2.json()["result"]
        #Possible values:0 - not classified;1 - information;2 - warning;3 - average;4 - high;5 - disaster.
        severvalue = 4
        counter=0
        ustgax_day_limit = 2
        allproblemdict = {} 
        for i in range(len(jarray)):
            tmp = int(jarray[i]['severity'])
            if tmp > severvalue:
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
                zorvvtsag = now - eventclock
                # Enabled Disabled item shalgaj bna
                enedisabled = 0
                tempip = get_hosts_with_ip( r3.json().get('result')[0].get('hosts')[0].get('hostid'))
                if tempip == '0':
                    enedisabled = 1

                if all(word not in r3.json().get('result')[0].get('hosts')[0]['host']for word in bannedhosts) and all(word not in r3.json().get('result')[0]['name'] for word in bannedreasons) and zorvvtsag.total_seconds()/60 >= 20 and enedisabled == 0:   # 20 minutaas ix durationtai problem orj irne
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

        counter = len(createdtickets)
        isfind = False
        for x in allproblemdict:
            # 2 dict харьцуулж байгаа үгйүг нь шалгаж байна
            for z in createdtickets:
                if allproblemdict[x]['host'] == createdtickets[z]['host'] and allproblemdict[x]['reason'] == createdtickets[z]['reason']:
                    isfind = True
                    break

            # host created ticket dotor baixgvi baiwal shineer vvsgeed, daraa ni vvssen ticket dotor nemj ogj bna
            if isfind == False:
                tempcontent = allproblemdict[x]['reason'] +' ip:'+ allproblemdict[x]['ip_address'] 
                #createticket(sessiontoken,allproblemdict[x]['host'],tempcontent)
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
