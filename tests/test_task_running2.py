import time
import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

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

#Task
keys = ['api', 'tasks', 'create']
params = {'item' : '/timeside/api/items/' + '2ff01106-1200-4d8d-a245-6a9f3f8525e6' + '/', 'experience': '/timeside/api/experiences/' + '72075fbf-7818-4f30-a4e0-582c9fe6a2d0' + '/','status':2} # 2  --> pending ???

task = client.action(schema,keys,params)

time.sleep(10)

#Results
keys = ['api', 'results', 'list']
params = {'search' : '2ff01106-1200-4d8d-a245-6a9f3f8525e6'}

results = client.action(schema,keys,params)
print(results)