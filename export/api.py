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

class IExporter(Interface):
    """Export driver interface"""

    # Remark: the method prototypes do not include any self or cls argument 
    # because an interface is meant to show what methods a class must expose 
    # from the caller's point of view. However, when implementing the class 
    # you'll obviously want to include this extra argument.

    def get_format():
        """Return the export/encoding format as a short string 
        Example: "MP3", "OGG", "AVI", ...
        """
   
    def get_description():
        """Return a string describing what this export format provides, is good 
        for, etc... The description is meant to help the end user decide what 
        format is good for him/her
        """

    def get_file_extension():
        """Return the filename extension corresponding to this export format"""

    def get_mime_type():
        """Return the mime type corresponding to this export format"""

    def set_cache_dir(path):
        """Set the directory where cached files should be stored. Does nothing
        if the exporter doesn't support caching. 
       
        The driver shouldn't assume that this method will always get called. A
        temporary directory should be used if that's not the case.
        """

    def process(item_id, source, metadata, options=None):
        """Perform the exporting process and return the absolute path 
        to the resulting file.

        item_id is the media item id that uniquely identifies this audio/video
        resource

        source is the audio/video source file absolute path. For audio that
        should be a WAV file

        metadata is a tuple containing tuples for each descriptor return by
        the dc.Ressource of the item, in the model order :
        ((name1, value1),(name2, value2),(name1, value3), ...)

        The returned file path is not meant to be permanent in any way, it 
        should be considered temporary/volatile by the caller.

        It is highly recommended that export drivers implement some sort of
        cache instead of re-encoding each time process() is called.

        It should be possible to make subsequent calls to process() with
        different items, using the same driver instance.
        """

class ExportProcessError(TimeSideError):

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
