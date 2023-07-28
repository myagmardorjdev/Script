import requests
import json
from requests.auth import HTTPBasicAuth

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
def createticket(session_token):
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

print(json.dumps(r.json(), indent=4, sort_keys=True))
AUTHTOKEN = r.json()["result"]
print("\nRetrieve a list of problems")
r2 = requests.post(ZABBIX_API_URL,
                json={     
                    "jsonrpc": "2.0",     
                    "method":"problem.get",     
                    "params": {         
                          #"output": "extend",         "selectDServices": "extend",         "druleids": "19"
                            "output": "extend",
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

jarray = r2.json()["result"]
print("Төрөл: ",type(jarray))
print("Урт: ", len(jarray))
#Possible values:0 - not classified;1 - information;2 - warning;3 - average;4 - high;5 - disaster.
severvalue = 4
counter=0
allproblemdict = {} 
for i in range(len(jarray)):
    tmp = int(jarray[i]['severity'])
    if tmp > severvalue:
        r3 = requests.post(ZABBIX_API_URL,
                    json={     
                        "jsonrpc": "2.0",     
                        "method":"event.get",     
                        "params": {         
                                "output": ['eventid', 'hostid','name','clock','severity'],
                                'selectHosts': ['hostid', 'host','ip'],
                                'selectInterfaces': ['ip'],
                                "select_acknowledges": "extend",         
                                "selectTags": "extend",        
                                "eventids": jarray[i]['eventid']
                                
                            }  ,     
                            "id": 2 ,
                            "auth": AUTHTOKEN
                    })
        print(json.dumps(r3.json(), indent=5, sort_keys=True))
        eachdict = {
            "reason" : r3.json().get('result')[0]['name'],
            "host" : r3.json().get('result')[0].get('hosts')[0]['host'] 
        }
        allproblemdict[counter] = eachdict
        counter+=1

print(counter)
#


#sessiontoken = initsession()

#createticket(sessiontoken)

