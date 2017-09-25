import timeside
from timeside.core import get_processor
from timeside.core.tools.test_samples import samples
audio_source = samples['sweep.wav']
decoder = get_processor('file_decoder')(uri=audio_source)
spectrogram = get_processor('spectrogram_analyzer')(input_blocksize=2048,
                                                    input_stepsize=1024)
pipe = (decoder | spectrogram)
pipe.run()
res = spectrogram.results['spectrogram_analyzer']
res.render()