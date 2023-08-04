import requests
import json
import time
from requests.auth import HTTPBasicAuth
from datetime import datetime

def initsession():
    url = 'http://10.0.0.14/apirest.php/initSession'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'user_token gbx24bStlmOLnf7PxANoU6h9KgaPSpEeOeogmqWW',
        'App-Token': 'dgoT8fOH3UYbYV1bz49N2PrFUhKY6Bqp8bJgrGRP'
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return data['session_token']
    else:
        print("Error:", response.status_code)
def createticket(session_token,title,content):
    url = 'http://10.0.0.14/apirest.php/Ticket/'

    # Replace 'your_username' and 'your_password' with your actual GLPI credentials
    username = 'myagmardorj'
    password = 'Az123456!0@'
    headers = {
        'Content-Type': 'application/json',
        'App-Token': 'dgoT8fOH3UYbYV1bz49N2PrFUhKY6Bqp8bJgrGRP',
        'Session-Token' : session_token
    }
    # Data for creating the ticket (replace with actual data)
    ticket_data = {
        'input': {
            'name': 'Your Ticket Title',
            'content': 'Your ticket description goes here',
            'priority': 3,  # Replace with the appropriate priority level
            'itemtype': 'Ticket',  # If you are creating a ticket
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

#loop outsides variables
createdtickets = {}

while(1==1):
    now = datetime.now()
    if now.hour > 8 and now.hour < 24:
        ZABBIX_API_URL = "https://zbx.altanjoloo.mn/zabbix/api_jsonrpc.php"
        UNAME = "Myagmardorj"
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
                if "Client" not in r3.json().get('result')[0].get('hosts')[0]['host'] and "last 24hours" not in  r3.json().get('result')[0]['name']:
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
                #createticket(sessiontoken,ticket,content)
                print("ticket created   ---" , allproblemdict[x]['host'])
                eachdict1 ={
                    "host" : allproblemdict[x]['host'],
                    "reason" : allproblemdict[x]['reason'],
                    "day": now.day,
                    "hour" : now.hour,
                    "date" : now
                }
                createdtickets[counter] = eachdict1
                counter+=1

            isfind = False
        
        #createdtickets ees hugatsaa ni bolson ticketvvdiig ustgaj bna
        for z in createdtickets:
            tdate = createdtickets[z]['date']
            zorvvodor = now - tdate
            if zorvvodor.days == 0:
                print(print(f'Difference is {zorvvodor.days} days'))
            if zorvvodor.days == 2:
                createdtickets.pop(z)
            
    time.sleep(15)
    print(now)
    print("sleeping...")

