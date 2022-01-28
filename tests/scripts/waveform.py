from timeside.core import get_processor

aubio_decoder = get_processor('aubio_decoder')
file_decoder = get_processor('file_decoder')
waveform_analyzer = get_processor('waveform_analyzer')


print('FLAC\n========')

path_full = '/srv/media/items/CASSIUS/01-Cassius_1999_sample.flac'
path_sample = '/srv/media/items/CASSIUS/01-Cassius_1999_sample.flac'

print('  aubio - short file')
d = aubio_decoder(path_sample)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value)

print('  gst - short file')
d = file_decoder(path_sample)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value)

print('  aubio - long file')
d = aubio_decoder(path_full)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])

print('  gst - long file')
d = file_decoder(path_full)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])


print('M4A\n========')

path = '/srv/media/items/Oomph_-_Gekreuzigt_1998_Lyrics_with_English_Translation-TeGAcx9KT5I.m4a'

print('  aubio')
d = aubio_decoder(path)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])

print('  gst')
d = file_decoder(path)
a = waveform_analyzer()
p = (d|a).run()
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])
