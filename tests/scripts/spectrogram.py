from timeside.core import get_processor
from timeside.plugins.grapher.spectrogram_lin import SpectrogramLinear
from timeside.plugins.grapher.spectrogram_log import SpectrogramLog
import tempfile

aubio_decoder = get_processor('aubio_decoder')
file_decoder = get_processor('aubio_decoder')
spectrogram_analyzer = get_processor('spectrogram_analyzer')


path_full = '/srv/media/items/CASSIUS/01-Cassius_1999.flac'
path_sample = '/srv/media/items/CASSIUS/01-Cassius_1999_sample.flac'

image = "/srv/media/results/spectrogram_lin-CASSIUS.png"
decoder = aubio_decoder(path_sample)
grapher = SpectrogramLinear(width=1024,
    height=256,
    bg_color=(0, 0, 0),
    color_scheme='default')
(decoder | grapher).run()
grapher.render(image)


image = "/srv/media/results/spectrogram_log-CASSIUS.png"
decoder = aubio_decoder(path_sample)
grapher = SpectrogramLog(width=1024,
    height=256,
    bg_color=(0, 0, 0),
    color_scheme='default')
(decoder | grapher).run()
grapher.render(image)



path_full = '/srv/media/items/'
path_sample = '/srv/media/items/2022/03/16/StreetGroove_20-01.wav'

image = "/srv/media/results/spectrogram_lin-STREET.png"
decoder = aubio_decoder(path_sample)
grapher = SpectrogramLinear(width=1024,
    height=256,
    bg_color=(0, 0, 0),
    color_scheme='default')
(decoder | grapher).run()
grapher.render(image)


image = "/srv/media/results/spectrogram_log-STREET.png"
decoder = aubio_decoder(path_sample)
grapher = SpectrogramLog(width=1024,
    height=256,
    bg_color=(0, 0, 0),
    color_scheme='default')
(decoder | grapher).run()
grapher.render(image)

