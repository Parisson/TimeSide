import os
import urllib


def check_samples():
    url = 'http://github.com/yomguy/timeside-samples/raw/master/samples/'
    samples = ['guitar.wav', 'sweep.wav', 'sweep_mono.wav', 'sweep_32000.wav', 'sweep.flac', 'sweep.ogg', 'sweep.mp3', 'sweep_source.wav']
    path = os.path.normpath(os.path.dirname(__file__))
    dir = path + os.sep + 'samples'

    if not os.path.exists(dir):
        os.makedirs(dir)

    for sample in samples:
        path = dir + os.sep + sample
        if not os.path.exists(path):
            print 'downloading: ' + sample
            f = open(path, 'w')
            u = urllib.urlopen(url+sample)
            f.write(u.read())
            f.close()
