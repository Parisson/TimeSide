# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2013 Parisson SARL
# Copyright (c) 2009-2012 Guillaume Pellerin <pellerin@parisson.com>
# Copyright (C) 2008 MUSIC TECHNOLOGY GROUP (MTG)
#                    UNIVERSITAT POMPEU FABRA

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
#   Bram de Jong <bram.dejong at domain.com where domain in gmail>
#   Guillaume Pellerin <yomguy@parisson.com>

try:
    from PIL import Image, ImageDraw, ImageColor, ImageEnhance
except ImportError:
    import Image
    import ImageDraw
    import ImageColor
    import ImageEnhance

import numpy


def interpolate_colors(colors, flat=False, num_colors=256):
    """ Given a list of colors, create a larger list of colors interpolating
    the first one. If flatten is True a list of numers will be returned. If
    False, a list of (r,g,b) tuples. num_colors is the number of colors wanted
    in the final list """

    palette = []

    for i in range(num_colors):
        index = (i * (len(colors) - 1)) / (num_colors - 1.0)
        index_int = int(index)
        alpha = index - float(index_int)

        if alpha > 0:
            r = (1.0 - alpha) * colors[index_int][
                0] + alpha * colors[index_int + 1][0]
            g = (1.0 - alpha) * colors[index_int][
                1] + alpha * colors[index_int + 1][1]
            b = (1.0 - alpha) * colors[index_int][
                2] + alpha * colors[index_int + 1][2]
        else:
            r = (1.0 - alpha) * colors[index_int][0]
            g = (1.0 - alpha) * colors[index_int][1]
            b = (1.0 - alpha) * colors[index_int][2]

        if flat:
            palette.extend((int(r), int(g), int(b)))
        else:
            palette.append((int(r), int(g), int(b)))

    return palette


def downsample(vector, factor):
    """
    downsample(vector, factor):
        Downsample (by averaging) a vector by an integer factor.
    """
    if (len(vector) % factor):
        print "Length of 'vector' is not divisible by 'factor'=%d!" % factor
        return 0
    vector.shape = (len(vector) / factor, factor)
    return numpy.mean(vector, axis=1)


def smooth(x, window_len=10, window='hanning'):
    """
    Smooth the data using a window with requested size.

    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    Parameters
    ----------
    x : numpy.array
        the input signal
    window_len : int
        the dimension of the smoothing window
    window : str
        the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
        flat window will produce a moving average smoothing.

    Returns
    -------
    The smoothed signal

    See Also
    -------

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    Examples
    --------

    >>> import numpy as np
    >>> from timeside.grapher.utils import smooth
    >>> t = np.arange(-2,2,0.1)
    >>> x = np.sin(t)+np.random.randn(len(t))*0.1
    >>> y = smooth(x)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(x) # doctest: +SKIP
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.plot(y) # doctest: +SKIP
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.legend(['Source signal', 'Smoothed signal']) # doctest: +SKIP
    <matplotlib.legend.Legend object at 0x...>
    >>> plt.show() # doctest: +SKIP
    """

    # TODO: the window parameter could be the window itself if an array
    # instead of a string

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")
    if window_len < 3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = numpy.r_[2 * x[0] - x[window_len:1:-1],
                 x, 2 * x[-1] - x[-1:-window_len:-1]]

    if window == 'flat':  # moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = getattr(numpy, window)(window_len)

    y = numpy.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def im_watermark(im, inputtext, font=None, color=None, opacity=.6, margin=(30, 30)):
    """imprints a PIL image with the indicated text in lower-right corner"""
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    textlayer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    textdraw = ImageDraw.Draw(textlayer)
    textsize = textdraw.textsize(inputtext, font=font)
    textpos = [im.size[i] - textsize[i] - margin[i] for i in [0, 1]]
    textdraw.text(textpos, inputtext, font=font, fill=color)
    if opacity != 1:
        textlayer = reduce_opacity(textlayer, opacity)
    return Image.composite(textlayer, im, textlayer)


def peaks(samples):
    """ Find the minimum and maximum peak of the samples.
    Returns that pair in the order they were found.
    So if min was found first, it returns (min, max) else the other way around. """
    max_index = numpy.argmax(samples)
    max_value = samples[max_index]

    min_index = numpy.argmin(samples)
    min_value = samples[min_index]

    if min_index < max_index:
        return (min_value, max_value)
    else:
        return (max_value, min_value)


def color_from_value(self, value):
    """ given a value between 0 and 1, return an (r,g,b) tuple """
    return ImageColor.getrgb("hsl(%d,%d%%,%d%%)" % (int((1.0 - value) * 360), 80, 50))


def mean(samples):
    return numpy.mean(samples)


def normalize(contour):
    contour = contour - min(contour)
    return contour / max(contour)
