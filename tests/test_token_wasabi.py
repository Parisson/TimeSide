import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

# """ http post http://localhost:9000/timeside/api-token-auth/ username=admin password=admin """
# url = 'http://localhost:9000/timeside/api-token-auth/'

api_token_url = 'https://wasabi.telemeta.org/timeside/api-token-auth/'
api_schema_url = 'https://wasabi.telemeta.org/timeside/api/schema/'

auth={'username':'wasabi', 'password':' '}
r = requests.post(api_token_url, data=auth)
token=r.json()['token']

print(token)

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)

client = Client(auth=auth)

#testing several request to the TimeSide core API
schema = client.get(api_schema_url)

keys = ['api', 'items', 'create']
params = {'title':'foo_test', 'source_url': 'https://www.youtube.com/watch?v=WFyC4bCYkJM', 'external_id': 'WFyC4bCYkJM'}
item = client.action(schema,keys,params)

print(item)

keys = ['api', 'items', 'read']
params = {'uuid': item['uuid']}
item = client.action(schema,keys,params)

print(item)

# keys = ['api', 'items', 'delete']
# params = {'uuid': item['uuid']}
# item = client.action(schema,keys,params)

keys = ['api', 'items', 'list']
data = client.action(schema,keys)
for item in data:
    print(item['title'] + '   ' + item['uuid'])

