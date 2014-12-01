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
# Authors : Guillaume Pellerin <yomguy@parisson.com>
#           Thomas Fillon <thomas@parisson.com>

from django.http import Http404
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponse

from rest_framework import viewsets

from timeside.server.models import Experience, Item, Result, Processor
from timeside.server.models import Preset, Selection, Task, User
from timeside.server.models import _PENDING
from timeside.server.serializers import ExperienceSerializer, ItemSerializer
from timeside.server.serializers import PresetSerializer
from timeside.server.serializers import ProcessorSerializer
from timeside.server.serializers import ResultSerializer
from timeside.server.serializers import SelectionSerializer
from timeside.server.serializers import TaskSerializer
from timeside.server.serializers import UserSerializer

from timeside.analyzer.core import AnalyzerResultContainer
import os


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


class ResultEncoderView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        return HttpResponse(stream_from_file(result.file.path),
                            mimetype=result.mime_type)


class ItemDetail(DetailView):

    model = Item
    template_name = 'timeside/item_detail.html'


class ItemExport(DetailView, SingleObjectMixin):
    model = Item

    def get(self, request, pk, extension):
        from . utils import TS_ENCODERS_EXT

        if extension not in TS_ENCODERS_EXT:
            raise Http404('Unknown export file extension: %s' % extension)

        encoder = TS_ENCODERS_EXT[extension]
        # Get or Create Processor = encoder
        processor, created = Processor.objects.get_or_create(pid=encoder)
        # Get or Create Preset with processor
        preset, created = Preset.objects.get_or_create(processor=processor)
        # Get Result with preset and item
        item = self.get_object()
        try:
            result = Result.objects.get(item=item, preset=preset)
            if not os.path.exists(result.file.path):
                result.delete()
                return self.get(request, pk, extension)
            return HttpResponse(stream_from_file(result.file.path),
                                mimetype=result.mime_type)
        except Result.DoesNotExist:
            # Result does not exist
            # the corresponding task has to be created and run
            experience = Experience()
            experience.save()
            experience.presets.add(preset)
            selection = Selection()
            selection.save()
            selection.items.add(item)
            task = Task(experience=experience, selection=selection,
                        status=_PENDING)
            task.save()  # save task and run
            # TODO : find a way to stream during task ...
            return self.get(request, pk, extension)
