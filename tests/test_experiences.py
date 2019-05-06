import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication

# """ http post http://localhost:9000/timeside/api-token-auth/ username=admin password=admin """
# url = 'http://localhost:9000/timeside/api-token-auth/'

api_token_url = 'https://wasabi.telemeta.org/timeside/api-token-auth/'
api_schema_url = 'https://wasabi.telemeta.org/timeside/api/schema/'

auth={'username':'wasabi', 'password':'Dywyept_ock0'}
r = requests.post(api_token_url, data=auth)
token=r.json()['token']

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)

client = Client(auth=auth)

#testing several request to the TimeSide core API
schema = client.get(api_schema_url)

keys = ['api', 'experiences', 'update']
params = {'title':'experience-test','uuid':'95ce1dcc-610d-4092-ac3a-aa035b30048d'}
client.action(schema,keys,params)