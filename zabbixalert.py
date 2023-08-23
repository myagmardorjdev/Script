import requests
import json
import base64
import time
from requests.auth import HTTPBasicAuth
from datetime import datetime
sleepsecond = 120
log_path = 'D:/zabbixlog.txt'
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
            'entity' : 24,
            'requesttypes_id': 13,
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
            'output': ['hostid', 'name'],
            'selectInterfaces': ['ip'],
            'filter': {
                'hostid': hostid  # Specific hostid you want to fetch
            }
            # Add more parameters or filters as needed
        },
        'auth': AUTHTOKEN,
        'id': 1
    }

    response = requests.post(ZABBIX_API_URL, json=payload, headers=headers)
    return response.json()['result'][0]['interfaces'][0]['ip']
def log_write(content):
    with open(log_path, 'a') as f:
        now = datetime.now()
        string = '\n'+str(now) + ' '+ content
        f.write(string)

#loop outsides variables
sessiontoken = initsession()
createdtickets = {}


while(1==1):
    now = datetime.now()
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
                                    "selectHosts": ["host", "name",'allowed_hosts','hostid'],
                                    "interfaces" : ['ip','allowed_hosts','hostid'],
                                    "selectAcknowledges": "extend",
                                    "recent": "true",
                                    "sortfield": ["eventid"],
                                    "sortorder": "ASC",
                                    "severity": 5    
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
                #Client pos bolon not restarted 24 hours gdg iig algasaj bna 
                if "Client" not in r3.json().get('result')[0].get('hosts')[0]['host'] and "last 24hours" not in  r3.json().get('result')[0]['name'] and "POS_8080_down" not in r3.json().get('result')[0]['name']:
                    eachdict = {
                        "host" : r3.json().get('result')[0].get('hosts')[0]['host'],
                        "reason" : r3.json().get('result')[0]['name'],
                        "ip_address" : get_hosts_with_ip( r3.json().get('result')[0].get('hosts')[0].get('hostid'))
                    }
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
                print("ticket created   ---" , allproblemdict[x]['host'])
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
            if zorvvodor.days == 2:
                print("")
            else:
               temptickets[cc] = createdtickets[z]
               cc+=1
        createdtickets = temptickets  # tempticketiig tickets rvv hadgalj bna
                
            
    time.sleep(sleepsecond)
    print(now)
    print("sleeping...")
    log_write("looping ...")
