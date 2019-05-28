import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication
from numpy import mean

token='1da6798f2700556e81d9ab32db77e4ea9aa4ca52'

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

spectrogram = '/timeside/api/presets/3d67b9b3-6f27-4fb9-af97-23e67dbd4a6e/'
mean_dc_shift =  '/timeside/api/presets/72465383-4bcb-453b-9d0c-dd07eaa3da5e/'

params = {'title':'experience_WASABI', 'presets':[mean_dc_shift, spectrogram]}
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