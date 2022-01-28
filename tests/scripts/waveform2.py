from timeside.core import get_processor

path = '/srv/media/items/Oomph_-_Gekreuzigt_1998_Lyrics_with_English_Translation-TeGAcx9KT5I.m4a'

dec = get_processor('aubio_decoder')
d = dec(path)
a = get_processor('waveform_analyzer')()
p = (d|a)
p.run()
print('aubio_decoder')
print(a.results['waveform_analyzer'].data_object.value)
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])

dec = get_processor('file_decoder')
d = dec(path)
a = get_processor('waveform_analyzer')()
p = (d|a)
p.run()
print('file_decoder')
print(a.results['waveform_analyzer'].data_object.value)
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])


