# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2009 Parisson
# Copyright (c) 2007 Olivier Guilyardi <olivier@samalyse.com>
# Copyright (c) 2007-2009 Guillaume Pellerin <pellerin@parisson.com>
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

from timeside.core import Interface, TimeSideError

class IDecoder(Interface):
    """Decoder driver interface"""

    @staticmethod
    def format():
        """Return the decode/encoding format as a short string 
        Example: "MP3", "OGG", "AVI", ...
        """
   
    @staticmethod
    def description():
        """Return a string describing what this decode format provides, is good 
        for, etc... The description is meant to help the end user decide what 
        format is good for him/her
        """

    @staticmethod
    def file_extension():
        """Return the filename extension corresponding to this decode format"""

    @staticmethod
    def mime_type():
        """Return the mime type corresponding to this decode format"""

    def process(self, source, options=None):
        """Perform the decoding process and stream the result through a generator

        source is the audio/video source file absolute path.

        It is highly recommended that decode drivers implement some sort of
        cache instead of re-encoding each time process() is called.

        It should be possible to make subsequent calls to process() with
        different items, using the same driver instance.
        """


class DecodeProcessError(TimeSideError):

    def __init__(self, message, command, subprocess):
        self.message = message
        self.command = str(command)
        self.subprocess = subprocess

    def __str__(self):
        if self.subprocess.stderr != None:
            error = self.subprocess.stderr.read()
        else:
            error = ''
        return "%s ; command: %s; error: %s" % (self.message,
                                                self.command,
                                                error)
