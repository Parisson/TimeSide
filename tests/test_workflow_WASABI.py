import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication
from numpy import mean

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
youtube_provider = '/timeside/api/providers/042d0121-456a-4b7d-a993-f8b040f6fc9c/'
external_youtube_uri = 'https://www.youtube.com/watch?v=sOnqjkJTMaA'
params = {'title':'Thriller','description':'Music from Michael Jackson','external_uri': external_youtube_uri,'provider': youtube_provider}
item = client.action(schema,keys,params)

#Ajout dans la selection WASABI
keys = ['api', 'selections', 'update']
WASABI_Selection_uuid = '3c58f084-a16d-470a-afc3-4a2341c46e40'
params = {'uuid':WASABI_Selection_uuid, 'items':['/timeside/api/items/' + item['uuid'] + '/']}
selec = client.action(schema,keys,params)

#Experience
keys = ['api', 'experiences', 'create']
params = {'title':'aubio_temporal', 'presets':['/timeside/api/presets/b6f0deab-e39f-4df3-b586-2c0554101a34/']}
exp = client.action(schema,keys,params)
exp_uuid = exp['uuid']

#Task
keys = ['api', 'tasks', 'create']
params = {'item' : '/timeside/api/items/' + item['uuid'] + '/', 'experience': '/timeside/api/experiences/' + exp_uuid + '/','status':2} # 2  --> pending ???

task = client.action(schema,keys,params)

time.sleep(20)

#Results
keys = ['api', 'results', 'list']
params = {'search' : item['uuid']}

result = client.action(schema,keys,params)

result_json_url = 'http://localhost:9000/timeside/results/' + result[0]['uuid'] + '/json/'

result_json = requests.get(result_json_url, headers={'Authorization': token}).json()

mean(result_json[4]['data_object']['value']['numpyArray'][1500:])
