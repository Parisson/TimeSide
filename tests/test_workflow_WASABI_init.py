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


#Provider
keys = ['api', 'providers', 'create']
params = {'name':'youtube','url':'https://www.youtube.com/'}
provider = client.action(schema,keys,params)
print('UUID YouTube Provider :' + provider['uuid'])

#WASABI Selection
keys = ['api', 'selections', 'create']
params = {'title':'WASABI'}
selec = client.action(schema,keys,params)
print('UUID Selection WASABI :' + selec['uuid'])