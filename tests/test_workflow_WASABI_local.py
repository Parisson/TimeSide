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
    if prv['pid'] == 'youtube':
        youtube_provider = prv

provider_uri = '/timeside/api/providers/' + youtube_provider['uuid'] + '/'

#creation of an Item for Michael Jackson's Thriller track using YouTube's URL
keys = ['api', 'items', 'create']
external_youtube_uri = 'https://www.youtube.com/watch?v=sOnqjkJTMaA'
params = {'title':'Thriller','description':'Music from Michael Jackson','external_uri': external_youtube_uri,'provider': provider_uri}
item = client.action(schema,keys,params)

#adding this track to the WASABI selection
keys = ['api', 'selections', 'update']
params = {'uuid':selection_uuid, 'items':['/timeside/api/items/' + item['uuid'] + '/']}
selec = client.action(schema,keys,params)

#Creating an Experience
keys = ['api', 'experiences', 'create']

#aubio_mfcc = '/timeside/api/presets/5b6887c8-b0f7-4798-838d-2771851bff66/'
aubio_pitch = '/timeside/api/presets/445d6bfd-093f-4527-9ce7-8a1afc2e74c3/'
spectrogram = '/timeside/api/presets/35aef627-74e9-46b0-a478-22c7ed603fb4/'
mean_dc_shift =  '/timeside/api/presets/8fc11b9f-5f3f-4bcd-bfc5-19fbf26c92fe/'

params = {'title':'experience_WASABI', 'presets':[mean_dc_shift, aubio_pitch, spectrogram]}
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