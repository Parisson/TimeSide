from requests import get
from coreapi import Client
from coreapi.auth import TokenAuthentication
from StringIO import StringIO
from PIL import Image
import numpy as np

token='1fb373f927ffa9e6f99880922810e1eeb0fc926b'

#coreapi client with the right token
auth = TokenAuthentication(
    scheme='Token',
    token=token
)
client = Client(auth=auth)

#schema of the API
schema = client.get('https://wasabi.telemeta.org/timeside/api/schema/')

#Example mfcc (list of lists) 
json_url = 'https://wasabi.telemeta.org/timeside/results/030d8b0a-5512-4db8-9183-22dd2b4e377d/json/'
result_json = get(json_url, headers={'Authorization': token}).json()
result = result_json[0]['data_object']['value']
mfcc = np.array(result['numpyArray'] , dtype=result['dtype'])
print 'MFCC matrix type:  ' + str(mfcc.shape)

#Example spectrogram (png image)
png_url = 'https://wasabi.telemeta.org/media/results/47467956-081a-408e-8be6-851bd89e78ba/b16ced21-3a7c-41b3-9589-df6df4507c66.png'
result_png = get(png_url, headers={'Authorization': token})
img = Image.open(StringIO(result_png.content))
img.show()

#Example numeric value (DC)
json_url = 'https://wasabi.telemeta.org/timeside/results/0da0ff03-270f-4a75-a636-99d9c2cee39e/json/'
result_json = get(json_url, headers={'Authorization': token}).json()
result_json = result_json[0]
print 'DC: ' + str(result_json['data_object']['value']['numpyArray'][0])