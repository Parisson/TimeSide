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

external_uri = 'https://www.youtube.com/watch?v=Zi_XLOBDo_Y'


#http://www.youtube.com/watch?v=h_D3VFfhvs4

#youtube_dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     rfile = ydl.download(external_uri)

# print(rfile)


import youtube_dl
external_uri = 'https://www.youtube.com/watch?v=Zi_XLOBDo_Y'

ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': unicode('/srv/media/items/download/%(title)s-%(id)s.%(ext)s'),
    'postprocessors': [{'key':'FFmpegExtractAudio'}],
    'restrictfilenames':True,
}
        
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(external_uri, download=True)