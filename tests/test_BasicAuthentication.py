import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication
from coreapi.auth import BasicAuthentication

# """ http post http://localhost:9000/timeside/api-token-auth/ username=admin password=admin """
url = 'http://localhost:9000/timeside/api-token-auth/'
auth={'username':'admin', 'password':'admin'}
r = requests.post(url, data=auth)
token=r.json()['token']

#coreapi client with the right token
auth = BasicAuthentication(
    username='admin',
    pssword='admin'
)
client = Client(auth=auth)

#testing several request to the TimeSide core API
schema = client.get('http://localhost:9000/timeside/api/schema/')

keys = ['api', 'items', 'create']
params = {'title':'fooTest'}
client.action(schema,keys,params)

keys = ['api', 'items', 'list']
data = client.action(schema,keys)
for item in data:
    print(item['title'] + '   ' + item['uuid'])