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
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics

from timeside.server.models import Experience, Item, Result, Processor, SubProcessor
from timeside.server.models import Preset, Selection, Task, User
from timeside.server.models import AnalysisTrack
from timeside.server.models import _DRAFT, _DONE, _RUNNING
from timeside.server.serializers import ExperienceSerializer, ItemSerializer, ItemWaveformSerializer
from timeside.server.serializers import PresetSerializer
from timeside.server.serializers import ProcessorSerializer
from timeside.server.serializers import SubProcessorSerializer
from timeside.server.serializers import ResultSerializer, Result_ReadableSerializer
from timeside.server.serializers import SelectionSerializer
from timeside.server.serializers import TaskSerializer
from timeside.server.serializers import UserSerializer
from timeside.server.serializers import AnalysisSerializer

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


class UUIDViewSetMixin(object):

    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-z-]+'


class SelectionViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Selection
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer


class ItemViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Item
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemWaveView(UUIDViewSetMixin, generics.RetrieveAPIView):

    model = Item
    queryset = Item.objects.all()
    serializer_class = ItemWaveformSerializer

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemWaveView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['plop'] = 91
        return context
    def get_serializer_context(self):
        """
        pass request attribute to serializer
        """
        context = super(ItemWaveView, self).get_serializer_context()
        #context['plop'] = 92
        return context


class ExperienceViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Experience
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ProcessorViewSet(viewsets.ModelViewSet):

    model = Processor
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    lookup_field = 'pid'
    lookup_value_regex = '[0-9a-z_]+'


class SubProcessorViewSet(viewsets.ModelViewSet):

    model = SubProcessor
    queryset = SubProcessor.objects.all()
    serializer_class = SubProcessorSerializer
    lookup_field = 'sub_processor_id'
    lookup_value_regex = '[0-9a-z_.]+'


class ResultViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Result
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class PresetViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Preset
    queryset = Preset.objects.all()
    serializer_class = PresetSerializer


class TaskViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    
class AnalysisViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = AnalysisTrack
    queryset = AnalysisTrack.objects.all()
    serializer_class = AnalysisSerializer




    
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


class ResultAnalyzerToElanView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        res_id = kwargs['res_id']
        container = AnalyzerResultContainer()
        container.from_hdf5(result.hdf5.path)

        segment_result = container[res_id]
        import tempfile
        tmp_dir = tempfile.mkdtemp(suffix=res_id+'_eaf')
        # Pympi will not overwrite the file
        audio_file = os.path.basename(segment_result.audio_metadata.uri)
        tmp_eaf_file = os.path.splitext(audio_file)[0] + '_' + res_id + '.eaf'
        abs_tmp_eaf_file = os.path.join(tmp_dir,tmp_eaf_file)
        segment_result.data_object.to_elan(elan_file=abs_tmp_eaf_file,
                                           media_file=audio_file)
        file_size = os.path.getsize(abs_tmp_eaf_file)
        # read file
        with open(abs_tmp_eaf_file, "rb") as f:
            eaf_data = f.read()
        import shutil
        shutil.rmtree(tmp_dir)

        response = HttpResponse(eaf_data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + '\"' + tmp_eaf_file +'\"'
        response['Content-Length'] = file_size
        return response


class ResultAnalyzerToSVView(View):

    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        res_id = kwargs['res_id']
        container = AnalyzerResultContainer()
        container.from_hdf5(result.hdf5.path)

        segment_result = container[res_id]
        import tempfile
        tmp_dir = tempfile.mkdtemp(suffix=res_id+'_sv')
        # Pympi will not overwrite the file
        audio_file = os.path.abspath(result.item.file.name)
        tmp_sv_file = os.path.splitext(os.path.basename(audio_file))[0] + '_' + res_id + '.sv'
        abs_tmp_sv_file = os.path.join(tmp_dir,tmp_sv_file)
        segment_result.data_object.to_sonic_visualiser(svenv_file=abs_tmp_sv_file,
                                                       audio_file=audio_file)
        file_size = os.path.getsize(abs_tmp_sv_file)
        # read file
        with open(abs_tmp_sv_file, "rb") as f:
            sv_data = f.read()
        import shutil
        shutil.rmtree(tmp_dir)

        response = HttpResponse(sv_data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + '\"' + tmp_sv_file +'\"'
        response['Content-Length'] = file_size
        return response


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

class ItemDetailExport(DetailView):

    model = Item
    template_name = 'timeside/item_detail_export.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailExport, self).get_context_data(**kwargs)
        context['Result'] = 'Result'
        Results = {}

        for result in self.get_object().results.all():
            proc_id = result.preset.processor.pid
            Results[proc_id] = {'id': result.id}
            if result.hdf5:
                container = AnalyzerResultContainer()
                container.from_hdf5(result.hdf5.path)
                Results[proc_id]['json'] = True
                Results[proc_id]['list']= {}
            elif result.mime_type:
                Results[proc_id]['audio'] = ('audio' in result.mime_type) | ('ogg' in result.mime_type)
                Results[proc_id]['image'] = ('image' in result.mime_type)
                Results[proc_id]['video'] = ('video' in result.mime_type)
                container = {}

            for res_id, res in container.items():
                if res.time_mode == 'segment':
                    if res.data_mode == 'label':
                        Results[proc_id]['list'][res_id] = {'elan': True,
                                                            'sv': True,
                                                            'Parameters': res.parameters,
                                                            'name': res.name}
                if res.time_mode == 'framewise':
                    if res.data_mode == 'value':
                        Results[proc_id]['list'][res_id] = {'elan': False,
                                                            'sv': True,
                                                            'Parameters': res.parameters,
                                                            'name': res.name}
        context['Results'] = Results

        return context


class ItemDetailAngular(DetailView):

    model = Item
    template_name = 'timeside/item_detail_angular.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailAngular, self).get_context_data(**kwargs)

        context['Result'] = 'Result'
        Results = {}

        for result in self.get_object().results.all():
            if result.hdf5:
                container = AnalyzerResultContainer()
                container.from_hdf5(result.hdf5.path)
            else:
                container = {}

            for name, res in container.items():
                 if res.time_mode == 'segment':
                    if res.data_mode == 'label':

                        Results[result.id] = name
            context['Results'] = Results

        return context


class ItemDetail(DetailView):

    model = Item
    template_name = 'timeside/item_detail.html'

    def get_object(self):
        return get_object_or_404(Item, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        context['Result'] = 'Result'
        Results = {}
        return context


class ItemTranscode(DetailView):
    model = Item

    def get_object(self):
        return get_object_or_404(Item, uuid=self.kwargs.get("uuid"))

    def get(self, request, uuid, extension):
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
                return self.get(request, uuid, extension)
            # Result and file exist --> OK
            return StreamingHttpResponse(stream_from_file(result.file.path),
                                         content_type=result.mime_type)
        except Result.DoesNotExist:
            # Result does not exist
            # the corresponding task has to be created and run
            task, created = Task.objects.get_or_create(experience=preset.get_single_experience(),
                                                       selection=item.get_single_selection())
            task.run(wait=True)
            return self.get(request, uuid, extension)
            #response = StreamingHttpResponse(streaming_content=stream_from_task(task),
            #                                 content_type=mime_type)
            #return response


class ItemResultsList(generics.ListAPIView):
    model = Result
    queryset = Result.objects.all()
    serializer_class = Result_ReadableSerializer

    def get_queryset(self):
        queryset = super(ItemResultsList, self).get_queryset()
        return queryset.filter(item__uuid=self.kwargs.get('uuid'), status=_DONE)
