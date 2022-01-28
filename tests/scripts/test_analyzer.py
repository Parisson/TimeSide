from timeside.core import get_processor

analyzer = get_processor('vamp_spectral_slope')
decoder = get_processor('aubio_decoder')

path = '/srv/media/items/tests/sweep.wav'

d = decoder(path)
a = analyzer()
p = (d|a).run()

print(a.results)
