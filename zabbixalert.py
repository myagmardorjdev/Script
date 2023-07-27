import requests
import json


ZABBIX_API_URL = "https://zbx.altanjoloo.mn/zabbix/api_jsonrpc.php"
UNAME = "Myagmardorj"
PWORD = "Aa1234567"
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
severvalue = 3
counter=0
for i in range(len(jarray)):
    tmp = int(jarray[i]['severity'])
    if tmp > severvalue:
        counter+=1
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
        print(json.dumps(r3.json(), indent=4, sort_keys=True))
   
print(counter)
#glpitoker - NckBv0PbYGQJ5sK1YEDVmwHPjKOlt58WbBQbgjKg

#curl.exe -X POST -H 'Content-Type: application/json' -H "Session-Token: xxxxxxxx" -d '{"input": {"name": "Ticket Name", "content": "Ticket Desc"}}' 'http://glpiserver/apirest.php/Ticket/'