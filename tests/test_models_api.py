import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

# """ http post http://localhost:9000/timeside/api-token-auth/ username=admin password=admin """
# url = 'http://localhost:9000/timeside/api-token-auth/'

api_token_url = 'http://localhost:9000/timeside/api-token-auth/'
api_schema_url = 'http://localhost:9000/timeside/api/schema/'

auth={'username':'admin', 'password':'admin'}
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

#item
schema = client.get(api_schema_url)

keys = ['api', 'items', 'create']
params = {'title':'foo_test'}
item = client.action(schema,keys,params)

print(item)

keys = ['api', 'items', 'read']
params = {'uuid': item['uuid']}
item2 = client.action(schema,keys,params)

print(item2)

keys = ['api', 'items', 'list']
data = client.action(schema,keys)
print('list of items')
for item in data:
    print(item['title'] + '   ' + item['uuid'])

#task
schema = client.get(api_schema_url)

keys = ['api', 'tasks', 'create']
params = {}
task = client.action(schema,keys,params)

print(task)

keys = ['api', 'tasks', 'read']
params = {'uuid': task['uuid']}
task2 = client.action(schema,keys,params)

print(task2)

keys = ['api', 'tasks', 'list']
data = client.action(schema,keys)
print('list of task')
for task in data:
    print('task' + '   ' + task['uuid'])


#experience
schema = client.get(api_schema_url)

keys = ['api', 'experiences', 'create']
params = {}
exp = client.action(schema,keys,params)

print(exp)

keys = ['api', 'experiences', 'read']
params = {'uuid': exp['uuid']}
exp2 = client.action(schema,keys,params)

print(exp2)

keys = ['api', 'experiences', 'list']
data = client.action(schema,keys)
for exp in data:
    print('experience' + '   ' + exp['uuid'])

#selection
schema = client.get(api_schema_url)

keys = ['api', 'selections', 'create']
params = {}
selec = client.action(schema,keys,params)

print(selec)

keys = ['api', 'selections', 'read']
params = {'uuid': selec['uuid']}
selec2 = client.action(schema,keys,params)

print(selec2)

keys = ['api', 'selections', 'list']
data = client.action(schema,keys)
for selec in data:
    print('selection' + '   ' + selec['uuid'])