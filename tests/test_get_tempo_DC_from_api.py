import requests
import h5py
from numpy import mean, floor

url_tempo = 'http://localhost:9000/media/results/2ff01106-1200-4d8d-a245-6a9f3f8525e6/4395e477-d61c-446b-b2e5-332ed858c9a2.hdf5'
url_dc = 'http://localhost:9000/media/results/2ff01106-1200-4d8d-a245-6a9f3f8525e6/376d888b-9846-4e00-a81c-a9a246147a5a.hdf5'

r = requests.get(url_tempo, allow_redirects=True)
# open('google.ico', 'wb').write(r.content)

temp_file_bpm = h5py.File(r.content)