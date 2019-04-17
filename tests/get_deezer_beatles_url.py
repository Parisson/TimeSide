import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

results = requests.get(url='https://api.deezer.com/artist/1/top?limit=10')

tracklist = []
for res in results.json()['data']:
    track = {'title':res['title'],'uri':res['link']}
    tracklist.append(track)
    
token='1fb373f927ffa9e6f99880922810e1eeb0fc926b'

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)
client = Client(auth=auth)

#schema of the API
schema = client.get('https://wasabi.telemeta.org/timeside/api/schema/')

#Getting Provider's uuid and WASABI selection
keys = ['api', 'selections', 'list']
for selec in client.action(schema,keys):
    if selec['title'] == 'WASABI':
        WASABI_selection = selec

selection_uuid = WASABI_selection['uuid']

keys = ['api', 'providers', 'list']
for prv in client.action(schema,keys):
    if prv['name'] == 'deezer':
        deezer_provider = prv

provider_uri = '/timeside/api/providers/' + deezer_provider['uuid'] + '/'


keys_item = ['api', 'items', 'create']
keys_selec = ['api', 'selections', 'update']
params_item = {'title':'','external_uri': '','provider': provider_uri}
item = client.action(schema,keys_item,params_item)
params_selec = {'uuid':selection_uuid, 'items':['']}
for track in tracklist:
    params_item['title'] = track['title']
    params_item['external_uri'] = track['uri']
    #creation of an Item for the current track
    item = client.action(schema,keys_item,params_item)
    params_selec['items'] = ['/timeside/api/items/' + item['uuid'] + '/']
    #adding this track to the WASABI selection
    selec = client.action(schema,keys_selec,params_selec)

#Creating an Experience
keys = ['api', 'experiences', 'create']

aubio_pitch = '/timeside/api/presets/c2de027a-cf4f-4be4-bada-ecb855543398/'
spectrogram = '/timeside/api/presets/2d5334ce-90fa-4d8a-91ff-ba8891cd6f73/'
mean_dc_shift =  '/timeside/api/presets/8d89fcf0-7c54-4d99-9b90-861a836e8201/'

params = {'title':'experience_WASABI', 'presets':[mean_dc_shift, aubio_pitch, spectrogram]}
exp = client.action(schema,keys,params)
exp_uuid = exp['uuid']

#Task
PENDING = 2
keys = ['api', 'tasks', 'create']
params = {'selection' : '/timeside/api/selections/' + selection_uuid + '/', 'experience': '/timeside/api/experiences/' + exp_uuid + '/','status':PENDING}

task = client.action(schema,keys,params)