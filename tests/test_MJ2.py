import requests
from coreapi import Client
from coreapi.auth import TokenAuthentication
import youtube_dl

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

#testing several request to the TimeSide core API
schema = client.get('http://localhost:9000/timeside/api/schema/')

keys = ['api', 'items', 'create']
params = {'title':'Beat It','description':'Music from Michael Jackson','external_uri':'https://www.youtube.com/watch?v=oRdxUFDoQe0','provider':'youtube'}
item = client.action(schema,keys,params)

#youtube_dl

ydl_opts = {
    'format': 'bestaudio',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(
        mj['source_url'], download=False)
    source_file_url = info['formats'][0]['url']
    # print(info['formats'][0]['url'])

# source_file = requests.get(source_file_url)

# with open('./source_file', 'wb') as f:  
#     f.write(source_file.content)

# print(source_file)

# uuid = mj['uuid']
# keys = ['api', 'items', 'update']
# params = {'uuid' : uuid, 'source_file':source_file}
# mj = client.action(schema,keys,params)

keys = ['api', 'items', 'update']
params = {'uuid':mj['uuid'],'source_url':info['formats'][0]['url']}
mj = client.action(schema,keys,params)

keys = ['api', 'selections', 'create']
items = [mj['url']]
params = {'items':items,'title':'SelectionTest'}
selec = client.action(schema,keys,params)