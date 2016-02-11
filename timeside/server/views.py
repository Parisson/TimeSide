# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Parisson SARL
# Copyright (c) 2014 Guillaume Pellerin <yomguy@parisson.com>

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
#
# Authors : Guillaume Pellerin <yomguy@parisson.com>
#           Thomas Fillon <thomas@parisson.com>

from django.http import Http404
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, StreamingHttpResponse

from rest_framework import viewsets, generics

from timeside.server.models import Experience, Item, Result, Processor
from timeside.server.models import Preset, Selection, Task, User
from timeside.server.models import _DRAFT, _DONE
from timeside.server.serializers import ExperienceSerializer, ItemSerializer
from timeside.server.serializers import PresetSerializer
from timeside.server.serializers import ProcessorSerializer
from timeside.server.serializers import ResultSerializer, Result_ReadableSerializer
from timeside.server.serializers import SelectionSerializer
from timeside.server.serializers import TaskSerializer
from timeside.server.serializers import UserSerializer

import timeside.core
from timeside.core.analyzer import AnalyzerResultContainer
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


def stream_from_task(task):
    for chunk in task.run(streaming=True):
        yield chunk
    task.save()


class SelectionViewSet(viewsets.ModelViewSet):

    model = Selection
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer


class ItemViewSet(viewsets.ModelViewSet):

    model = Item
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ExperienceViewSet(viewsets.ModelViewSet):

    model = Experience
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProcessorViewSet(viewsets.ModelViewSet):

    model = Processor
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer


class ResultViewSet(viewsets.ModelViewSet):

    model = Result
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class PresetViewSet(viewsets.ModelViewSet):

    model = Preset
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class TaskViewSet(viewsets.ModelViewSet):

    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()
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
        container.from_hdf5(result.hdf5.path)
        return HttpResponse(container.to_json(),
                            content_type='application/json')


class ResultGrapherView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        return HttpResponse(stream_from_file(result.file.path),
                            content_type='image/png')


class ResultEncoderView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        return StreamingHttpResponse(stream_from_file(result.file.path),
                            content_type=result.mime_type)


class ItemDetail(DetailView):

    model = Item
    template_name = 'timeside/item_detail.html'


class ItemExport(DetailView):
    model = Item

    def get(self, request, pk, extension):
        from . utils import TS_ENCODERS_EXT

        if extension not in TS_ENCODERS_EXT:
            raise Http404('Unknown export file extension: %s' % extension)

        encoder = TS_ENCODERS_EXT[extension]
        mime_type = timeside.core.get_processor(encoder).mime_type()
        # Get or Create Processor = encoder
        processor, created = Processor.objects.get_or_create(pid=encoder)
        # Get or Create Preset with processor
        preset, created = Preset.objects.get_or_create(processor=processor)
        # Get Result with preset and item
        item = self.get_object()
        try:
            result = Result.objects.get(item=item, preset=preset)
            if not os.path.exists(result.file.path):
                # Result exists but not file (may have been deleted)
                result.delete()
                return self.get(request, pk, extension)
            # Result and file exist --> OK
            return StreamingHttpResponse(stream_from_file(result.file.path),
                                         content_type=result.mime_type)
        except Result.DoesNotExist:
            # Result does not exist
            # the corresponding task has to be created and run
            exp_title = "Transcode to %s" % extension
            exp_description = ("Experience for transcoding an item to %s\n"
                               "Automatically generated by the TimeSide "
                               "application.") % mime_type
            experience, created = Experience.objects.get_or_create(
                title=exp_title,
                description=exp_description)
            if created:
                experience.save()
                experience.presets.add(preset)

            sel_title = "Singleton selection for item %d" % item.id
            sel_description = ("Singleton selection for item %d\n"
                               "Automatically generated by the TimeSide "
                               "application.") % item.id
            selection, created = Selection.objects.get_or_create(
                title=sel_title,
                description=sel_description)
            if created:
                selection.save()
                selection.items.add(item)
            task, created = Task.objects.get_or_create(experience=experience,
                                                       selection=selection)

            response = StreamingHttpResponse(streaming_content=stream_from_task(task),
                                             content_type=mime_type)
            return response

class ItemResultsList(generics.ListAPIView):
    model = Result
    queryset = Result.objects.all()
    serializer_class = Result_ReadableSerializer

    def get_queryset(self):
        queryset = super(ItemResultsList, self).get_queryset()
        return queryset.filter(item__pk=self.kwargs.get('pk'), status=_DONE)

