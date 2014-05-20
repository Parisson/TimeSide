# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>

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
#
# Author : Guillaume Pellerin <yomguy@parisson.com>


from django.views.generic import *
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import viewsets

import timeside
from timeside.server.models import *
from timeside.server.serializers import *


def stream_from_file(file):
    chunk_size = 0x10000
    f = open(file, 'r')
    while True:
        chunk = f.read(chunk_size)
        if not len(chunk):
            f.close()
            break
        yield chunk


class SelectionViewSet(viewsets.ModelViewSet):

    model = Selection
    serializer_class = SelectionSerializer


class ItemViewSet(viewsets.ModelViewSet):

    model = Item
    serializer_class = ItemSerializer


class ExperienceViewSet(viewsets.ModelViewSet):

    model = Experience
    serializer_class = ExperienceSerializer


class ProcessorViewSet(viewsets.ModelViewSet):

    model = Processor
    serializer_class = ProcessorSerializer


class ResultViewSet(viewsets.ModelViewSet):

    model = Result
    serializer_class = ResultSerializer


class PresetViewSet(viewsets.ModelViewSet):

    model = Preset
    serializer_class = PresetSerializer


class TaskViewSet(viewsets.ModelViewSet):

    model = Task
    serializer_class = TaskSerializer


class UserViewSet(viewsets.ModelViewSet):

    model = User
    serializer_class = UserSerializer


class IndexView(ListView):

    model = Item
    template_name = 'timeside/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ResultAnalyzerView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        container = AnalyzerResultContainer()
        return HttpResponse(container.from_hdf5(result.hdf5.path).to_json(),
                            mimetype='application/json')


class ResultGrapherView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        return HttpResponse(stream_from_file(result.file.path), 
                            mimetype='image/png')

