#!/usr/bin/python3
import h5py
import os
import numpy as np

from timeside.core import get_processor

audio_path = '/srv/media/items/Monks_Dream.flac'
# hdf5_path = '/srv/media/results/Monks_Dream.hdf5'
hdf5_path = '/srv/media/results/e77cd578-7353-46ed-a1d2-fd0e98207d0a/77c9b2ca-4ca1-41f4-92c1-91a12eb195f2.hdf5'

start = 0
stop = 30
nb_pixels = 1024

# dec = get_processor('aubio_decoder')
# d = dec(audio_path)
# a = get_processor('waveform_analyzer')()
# p = (d|a)
# p.run()

# a.results.to_hdf5(hdf5_path)

wav_res = h5py.File(hdf5_path, 'r').get('waveform_analyzer')

duration = wav_res['audio_metadata'].attrs['duration']
samplerate = wav_res['data_object'][
        'frame_metadata'].attrs['samplerate']

if start < 0:
    start = 0
if start > duration:
    raise serializers.ValidationError(
        "start must be less than duration")
if stop == -1:
    stop = duration

if stop > duration:
    stop = duration

# nb_pixel must not be to big to keep minimum 2 samples per pixel
# to ensure 2 different values for min and max
cap_value = int(samplerate * abs(stop - start) / 2)
if nb_pixels > cap_value:
    nb_pixels = cap_value

min_values = np.zeros(nb_pixels)
max_values = np.zeros(nb_pixels)
time_values = np.linspace(
    start=start,
    stop=stop,
    num=nb_pixels + 1,
    endpoint=True
    )

sample_values = np.round(time_values * samplerate).astype('int')

for i in range(nb_pixels):
    values = wav_res['data_object']['value'][
        sample_values[i]:sample_values[i + 1]]
    if values.size:
        min_values[i] = np.min(values)
        max_values[i] = np.max(values)

print({'start': start,
        'stop': stop,
        'nb_pixels': nb_pixels,
        'time': time_values[0:-1],
        'min': min_values,
        'max': max_values}
)

