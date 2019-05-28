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

#Getting uuid of Provider and WASABI selection
keys = ['api', 'selections', 'list']
for selec in client.action(schema,keys):
    if selec['title'] == 'WASABI':
        WASABI_selection = selec

selection_uuid = WASABI_selection['uuid']

keys = ['api', 'providers', 'list']
for prv in client.action(schema,keys):
    if prv['pid'] == 'deezer':
        deezer_provider = prv

provider_uri = '/timeside/api/providers/' + deezer_provider['uuid'] + '/'

#creation of an Item for Michael Jackson's Thriller track using Deezer's URL
keys = ['api', 'items', 'create']
external_deezer_uri = 'https://www.deezer.com/track/4315684'
params = {'title':'take me out','description':'Music from franz ferdinand','external_uri': external_deezer_uri,'provider': provider_uri}
item = client.action(schema,keys,params)

#adding this track to the WASABI selection
keys = ['api', 'selections', 'update']
params = {'uuid':selection_uuid, 'items':['/timeside/api/items/' + item['uuid'] + '/']}
selec = client.action(schema,keys,params)

#Creating an Experience
keys = ['api', 'experiences', 'create']

spectrogram = '/timeside/api/presets/a1a9cd99-8168-4853-b096-00187ac05ca4/'

params = {'title':'experience_WASABI', 'presets':[spectrogram]}
exp = client.action(schema,keys,params)
exp_uuid = exp['uuid']

#Task
PENDING = 2
keys = ['api', 'tasks', 'create']
params = {'item' : '/timeside/api/items/' + item['uuid'] + '/', 'experience': '/timeside/api/experiences/' + exp_uuid + '/','status':PENDING}

task = client.action(schema,keys,params)

time.sleep(20)

#Results
keys = ['api', 'results', 'list']
params = {'search' : item['uuid']}

result = client.action(schema,keys,params)

for r in result:
    print('http://localhost:9000/timeside/results/' + r['uuid'] + '/json/')