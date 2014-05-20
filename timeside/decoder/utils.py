# -*- coding: utf-8 -*-

# Copyright (c) 2007-2013 Parisson
# Copyright (c) 2007-2013 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (c) 2010-2013 Paul Brossier <piem@piem.org>
#
# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Authors:
# Paul Brossier <piem@piem.org>
# Guillaume Pellerin <yomguy@parisson.com>
# Thomas Fillon <thomas@parisson.com>

from __future__ import division

import numpy as np


class Noise(object):

    """A class that mimics audiolab.sndfile but generates noise instead of reading
    a wave file. Additionally it can be told to have a "broken" header and thus crashing
    in the middle of the file. Also useful for testing ultra-short files of 20 samples."""

    def __init__(self, num_frames, has_broken_header=False):
        self.seekpoint = 0
        self.num_frames = num_frames
        self.has_broken_header = has_broken_header

    def seek(self, seekpoint):
        self.seekpoint = seekpoint

    def get_nframes(self):
        return self.num_frames

    def get_samplerate(self):
        return 44100

    def get_channels(self):
        return 1

    def read_frames(self, frames_to_read):
        if self.has_broken_header and self.seekpoint + frames_to_read > self.num_frames // 2:
            raise IOError()

        num_frames_left = self.num_frames - self.seekpoint
        if num_frames_left < frames_to_read:
            will_read = num_frames_left
        else:
            will_read = frames_to_read
        self.seekpoint += will_read
        return np.random.random(will_read) * 2 - 1


def path2uri(path):
    """
    Return a valid uri (file scheme) from absolute path name of a file

    >>> path2uri('/home/john/my_file.wav')
    'file:///home/john/my_file.wav'

    >>> path2uri('C:\Windows\my_file.wav')
    'file:///C%3A%5CWindows%5Cmy_file.wav'
    """
    import urlparse
    import urllib

    return urlparse.urljoin('file:', urllib.pathname2url(path))


def source_info(source):
    import os.path

    src_info = {'is_file': False,
                'uri': '',
                'pathname': ''}

    if os.path.exists(source):
        src_info['is_file'] = True
        # get the absolute path
        src_info['pathname'] = os.path.abspath(source)
        # and make a uri of it
        src_info['uri'] = path2uri(src_info['pathname'])
    return src_info


def get_uri(source):
    """
    Check a media source as a valid file or uri and return the proper uri
    """

    import gst

    src_info = source_info(source)

    if src_info['is_file']:  # Is this a file?
        return get_uri(src_info['uri'])

    elif gst.uri_is_valid(source):  # Is this a valid URI source for Gstreamer
        uri_protocol = gst.uri_get_protocol(source)
        if gst.uri_protocol_is_supported(gst.URI_SRC, uri_protocol):
            return source
        else:
            raise IOError('Invalid URI source for Gstreamer')
    else:
        raise IOError('Failed getting uri for path %s: no such file' % source)


def get_media_uri_info(uri):

    from gst.pbutils import Discoverer
    from gst import SECOND as GST_SECOND
    from glib import GError
    #import gobject
    GST_DISCOVER_TIMEOUT = 5000000000L
    uri_discoverer = Discoverer(GST_DISCOVER_TIMEOUT)
    try:
        uri_info = uri_discoverer.discover_uri(uri)
    except GError as e:
        raise IOError(e)
    info = dict()

    # Duration in seconds
    info['duration'] = uri_info.get_duration() / GST_SECOND

    audio_streams = uri_info.get_audio_streams()
    info['streams'] = []
    for stream in audio_streams:
        stream_info = {'bitrate': stream.get_bitrate(),
                       'channels': stream.get_channels(),
                       'depth': stream.get_depth(),
                       'max_bitrate': stream.get_max_bitrate(),
                       'samplerate': stream.get_sample_rate()
                       }
        info['streams'].append(stream_info)

    return info


def stack(process_func):

    import functools

    @functools.wraps(process_func)
    def wrapper(decoder):
        # Processing
        if not decoder.from_stack:
            frames, eod = process_func(decoder)
            if decoder.stack:
                decoder.process_pipe.frames_stack.append((frames, eod))
            return frames, eod
        else:
            return decoder._frames_iterator.next()

    return wrapper


def get_sha1(source):
    src_info = source_info(source)

    if src_info['is_file']:  # Is this a file?
        return sha1sum_file(src_info['pathname'])
    else:  # Then it should be an url
        return sha1sum_url(source)


def sha1sum_file(filename):
    '''
    Return the secure hash digest with sha1 algorithm for a given file

    >>> wav_file = 'tests/samples/guitar.wav' # doctest: +SKIP
    >>> print sha1sum_file(wav_file) # doctest: +SKIP
    #08301c3f9a8d60926f31e253825cc74263e52ad1
    '''
    import hashlib
    import io

    sha1 = hashlib.sha1()
    chunk_size = sha1.block_size * io.DEFAULT_BUFFER_SIZE

    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            sha1.update(chunk)
    return sha1.hexdigest()


def sha1sum_url(url):
    '''Return the secure hash digest with sha1 algorithm for a given url

    >>> url = 'https://github.com/yomguy/timeside-samples/raw/master/samples/guitar.wav'
    >>> print sha1sum_url(url)
    08301c3f9a8d60926f31e253825cc74263e52ad1
    >>> wav_file = 'tests/samples/guitar.wav' # doctest: +SKIP
    >>> uri = get_uri(wav_file)
    >>> print sha1sum_url(uri)
    08301c3f9a8d60926f31e253825cc74263e52ad1

    '''
    import hashlib
    import urllib
    from contextlib import closing

    sha1 = hashlib.sha1()
    chunk_size = sha1.block_size * 8192

    max_file_size = 10 * 1024 * 1024  # 10Mo limit in case of very large file

    total_read = 0
    with closing(urllib.urlopen(url)) as url_obj:
        for chunk in iter(lambda: url_obj.read(chunk_size), b''):
            sha1.update(chunk)
            total_read += chunk_size
            if total_read > max_file_size:
                break

    return sha1.hexdigest()


def sha1sum_numpy(np_array):
    '''
    Return the secure hash digest with sha1 algorithm for a numpy array
    '''
    import hashlib
    return hashlib.sha1(np_array.view(np.uint8)).hexdigest()


# Define global variables for use with doctest
DOCTEST_ALIAS = {'wav_file':
                 'https://github.com/yomguy/timeside-samples/raw/master/samples/guitar.wav'}

if __name__ == "__main__":
    import doctest

    doctest.testmod(extraglobs=DOCTEST_ALIAS)
