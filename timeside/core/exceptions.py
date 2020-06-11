# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 Olivier Guilyardi <olivier@samalyse.com>
#
# This file is part of TimeSide.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Error(Exception):

    """Exception base class for errors in TimeSide."""


class ApiError(Exception):

    """Exception base class for errors in TimeSide."""


class SubProcessError(Error):

    """Exception for reporting errors from a subprocess"""

    def __init__(self, message, command, subprocess):
        self.message = message
        self.command = str(command)
        self.subprocess = subprocess

    def __str__(self):
        if self.subprocess.stderr is not None:
            error = self.subprocess.stderr.read()
        else:
            error = ''
        return "%s ; command: %s; error: %s" % (self.message,
                                                self.command,
                                                error)


class PIDError(KeyError):
    "Exception for reporting missing Processor ID in registered processors"


class VampImportError(ImportError):
    "Can't import module depending on Vamp because vamp host is missing"


class ProviderError(Error):
    """
    Attributes:
        provider_pid -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, provider_pid, external_id=None, external_uri=None):
        self.provider_pid = provider_pid
        self.external_id = external_id
        self.external_uri = external_uri

    def __str__(self):
        if self.external_id:
            return f"'{self.provider_pid}' provider failed on id: '{self.external_id}'"
        elif self.external_uri:
            return f"'{self.provider_pid}' provider failed on uri:'{self.external_uri}'"
        else:
            return f"'{self.provider_pid}' provider failed"
