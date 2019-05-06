import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication
from numpy import mean

token='1fb373f927ffa9e6f99880922810e1eeb0fc926b'

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)
client = Client(auth=auth)

#schema of the API
schema = client.get('https://wasabi.telemeta.org/timeside/api/schema/')

#Getting uuid of Provider and WASABI selection
keys = ['api', 'selections', 'list']
for selec in client.action(schema,keys):
    if selec['title'] == 'WASABI':
        WASABI_selection = selec

selection_uuid = WASABI_selection['uuid']

keys = ['api', 'providers', 'list']
for prv in client.action(schema,keys):
    if prv['name'] == 'youtube':
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

aubio_mfcc = '/timeside/api/presets/fe7087c2-69eb-456f-839a-4b62ab34e9e1/'
aubio_pitch = '/timeside/api/presets/d6a9a974-4299-4871-8717-784c96023d18/'
spectrogram = '/timeside/api/presets/ca1e45ff-4688-44fa-8522-8338596d5833/'
mean_dc_shift =  '/timeside/api/presets/e11fd333-6e5d-4c6d-a5ef-8dcce548daca/'

params = {'title':'experience_WASABI', 'presets':[mean_dc_shift, aubio_pitch, spectrogram, aubio_mfcc]}
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
    print('https://wasabi.telemeta.org/timeside/results/' + r['uuid'] + '/json/')