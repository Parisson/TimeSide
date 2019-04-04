import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

# """ http post http://localhost:9000/timeside/api-token-auth/ username=admin password=admin """
url = 'http://localhost:9000/timeside/api-token-auth/'
auth={'username':'admin', 'password':'admin'}
r = requests.post(url, data=auth)
token=r.json()['token']

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)
client = Client(auth=auth)

#schema of the API
schema = client.get('http://localhost:9000/timeside/api/schema/')

#Item
keys = ['api', 'items', 'create']
params = {'title':'Billie Jean','description':'Music from Michael Jackson','external_uri':'http://www.youtube.com/watch?v=Zi_XLOBDo_Y','provider': '/timeside/api/providers/042d0121-456a-4b7d-a993-f8b040f6fc9c/'}
item = client.action(schema,keys,params)

#Ajout dans la selection WASABI
keys = ['api', 'selections', 'partial_update']
params = {'uuid':'3c58f084-a16d-470a-afc3-4a2341c46e40','items':['/timeside/api/items/' + item['uuid'] + '/']}
selec = client.action(schema,keys,params)

#Experience
keys = ['api', 'experiences', 'create']
params = {'title':'spectrogramme_test', 'presets':['/timeside/api/presets/eaccfb5b-e1cb-4b66-a49f-831564e4c789/']}
exp = client.action(schema,keys,params)
exp_uuid = exp['uuid']

#Selec
keys = ['api', 'selections', 'create']
params = {'items' : ['/timeside/api/items/' + item['uuid'] + '/']}
selec = client.action(schema,keys,params)

#Task
keys = ['api', 'tasks', 'create']
params = {'selection' : '/timeside/api/selections/' + selec['uuid'] + '/', 'experience': '/timeside/api/experiences/' + exp['uuid'] + '/','status':2} # 2  --> pending ???

task = client.action(schema,keys,params)

time.sleep(10)

#Results
keys = ['api', 'results', 'list']
params = {'search' : item['uuid']}

results = client.action(schema,keys,params)
print(results)