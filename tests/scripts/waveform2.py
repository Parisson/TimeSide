from timeside.core import get_processor

path = '/srv/media/items/download/David_Bowie_-_Lazarus_Video-y-JqH1M4Ya8.opus'

dec = get_processor('aubio_decoder')
d = dec(path)
a = get_processor('waveform_analyzer')()
p = (d|a)
p.run()
print('aubio_decoder')
print(a.results['waveform_analyzer'].data_object.value)
print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])

# dec = get_processor('file_decoder')
# d = dec(path)
# a = get_processor('waveform_analyzer')()
# p = (d|a)
# p.run()
# print('file_decoder')
# print(a.results['waveform_analyzer'].data_object.value)
# print(a.results['waveform_analyzer'].data_object.value[1264600:1323000])


