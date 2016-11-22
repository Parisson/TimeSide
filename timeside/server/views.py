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

import json

from django.http import Http404
from django.views.generic.base import View, TemplateView
from django.views.generic import DetailView, ListView
from django.http import HttpResponse, StreamingHttpResponse
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy

from . import models
from . import serializers

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

    model = models.Selection
    queryset = model.objects.all()
    serializer_class = serializers.SelectionSerializer


class ItemViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Item
    queryset = models.Item.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ItemListSerializer
        return serializers.ItemSerializer


class AnnotationTrackViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.AnnotationTrack
    queryset = model.objects.all()
    serializer_class = serializers.AnnotationTrackSerializer


class AnnotationViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Annotation
    queryset = model.objects.all()
    serializer_class = serializers.AnnotationSerializer


class ItemWaveView(UUIDViewSetMixin, generics.RetrieveAPIView):

    model = models.Item
    queryset = model.objects.all()
    serializer_class = serializers.ItemWaveformSerializer

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemWaveView, self).get_context_data(**kwargs)
        # Here we can modify the context
        # context['plop'] = 'plop'
        return context

    def get_serializer_context(self):
        """
        pass request attribute to serializer
        """
        context = super(ItemWaveView, self).get_serializer_context()
        # context['plop'] = 92
        return context


class ExperienceViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Experience
    queryset = model.objects.all()
    serializer_class = serializers.ExperienceSerializer


class ProcessorViewSet(viewsets.ModelViewSet):

    model = models.Processor
    queryset = model.objects.all()
    serializer_class = serializers.ProcessorSerializer
    lookup_field = 'pid'
    lookup_value_regex = '[0-9a-z_]+'


class SubProcessorViewSet(viewsets.ModelViewSet):

    model = models.SubProcessor
    queryset = model.objects.all()
    serializer_class = serializers.SubProcessorSerializer
    lookup_field = 'sub_processor_id'
    lookup_value_regex = '[0-9a-z_.]+'


class ResultViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Result
    queryset = model.objects.all()
    serializer_class = serializers.ResultSerializer


class PNGRenderer(renderers.BaseRenderer):
    media_type = 'image/png'
    format = 'png'
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class ResultVisualizationViewSet(UUIDViewSetMixin, generics.RetrieveAPIView):

    model = models.Result
    queryset = model.objects.all()
    serializer_class = serializers.ResultVisualizationSerializer

    renderer_classes = (PNGRenderer,)  # renderers.JSONRenderer,


class PresetViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Preset
    queryset = model.objects.all()
    serializer_class = serializers.PresetSerializer


class TaskViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Task
    queryset = model.objects.all()
    serializer_class = serializers.TaskSerializer


class UserViewSet(viewsets.ModelViewSet):

    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class AnalysisViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Analysis
    queryset = model.objects.all()
    serializer_class = serializers.AnalysisSerializer


class AnalysisTrackViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.AnalysisTrack
    queryset = model.objects.all()
    serializer_class = serializers.AnalysisTrackSerializer


class ResultAnalyzerView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(pk=kwargs['pk'])
        container = AnalyzerResultContainer()
        container.from_hdf5(result.hdf5.path)
        return HttpResponse(container.to_json(),
                            content_type='application/json')


class ResultAnalyzerToElanView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(pk=kwargs['pk'])
        res_id = kwargs['res_id']
        container = AnalyzerResultContainer()
        container.from_hdf5(result.hdf5.path)

        segment_result = container[res_id]
        import tempfile
        tmp_dir = tempfile.mkdtemp(suffix=res_id + '_eaf')
        # Pympi will not overwrite the file
        audio_file = os.path.basename(segment_result.audio_metadata.uri)
        tmp_eaf_file = os.path.splitext(audio_file)[0] + '_' + res_id + '.eaf'
        abs_tmp_eaf_file = os.path.join(tmp_dir, tmp_eaf_file)
        segment_result.data_object.to_elan(elan_file=abs_tmp_eaf_file,
                                           media_file=audio_file)
        file_size = os.path.getsize(abs_tmp_eaf_file)
        # read file
        with open(abs_tmp_eaf_file, "rb") as f:
            eaf_data = f.read()
        import shutil
        shutil.rmtree(tmp_dir)

        response = HttpResponse(eaf_data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + \
            '\"' + tmp_eaf_file + '\"'
        response['Content-Length'] = file_size
        return response


class ResultAnalyzerToSVView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(pk=kwargs['pk'])
        res_id = kwargs['res_id']
        container = AnalyzerResultContainer()
        container.from_hdf5(result.hdf5.path)

        segment_result = container[res_id]
        import tempfile
        tmp_dir = tempfile.mkdtemp(suffix=res_id + '_sv')
        # Pympi will not overwrite the file
        audio_file = os.path.abspath(result.item.file.name)
        tmp_sv_file = os.path.splitext(os.path.basename(audio_file))[
            0] + '_' + res_id + '.sv'
        abs_tmp_sv_file = os.path.join(tmp_dir, tmp_sv_file)
        segment_result.data_object.to_sonic_visualiser(svenv_file=abs_tmp_sv_file,
                                                       audio_file=audio_file)
        file_size = os.path.getsize(abs_tmp_sv_file)
        # read file
        with open(abs_tmp_sv_file, "rb") as f:
            sv_data = f.read()
        import shutil
        shutil.rmtree(tmp_dir)

        response = HttpResponse(sv_data, content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + \
            '\"' + tmp_sv_file + '\"'
        response['Content-Length'] = file_size
        return response


class ResultGrapherView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(pk=kwargs['pk'])
        return HttpResponse(stream_from_file(result.file.path),
                            content_type='image/png')


class ResultEncoderView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(pk=kwargs['pk'])
        return StreamingHttpResponse(stream_from_file(result.file.path),
                                     content_type=result.mime_type)


class ItemDetailExport(DetailView):

    model = models.Item
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
                Results[proc_id]['list'] = {}
            elif result.mime_type:
                Results[proc_id]['audio'] = ('audio' in result.mime_type) | (
                    'ogg' in result.mime_type)
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


class ItemList(ListView):

    model = models.Item
    template_name = 'timeside/item_list.html'

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        return super(ItemList, self).dispatch(*args, **kwargs)


class ItemDetail(DetailView):

    model = models.Item
    template_name = 'timeside/item_detail.html'

    def get_object(self):
        return get_object_or_404(models.Item, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        ts_item = {'ts_api_root': str(reverse_lazy('api-root', request=self.request)),
                   'ts_item_uuid': self.get_object().uuid
                   }
        context['ts_item'] = json.dumps(ts_item)
        return context


class ItemTranscode(DetailView):
    model = models.Item

    def get_object(self):
        return get_object_or_404(models.Item, uuid=self.kwargs.get("uuid"))

    def transcode_segment(self, uri, start, duration, encoder_pid, mime_type):
        decoder = timeside.core.get_processor('file_decoder')(uri, start=start, duration=duration)
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            encoder = timeside.core.get_processor(encoder_pid)(tmp_file.name, overwrite=True)
            pipe = (decoder | encoder)
            pipe.run()

            return FileResponse(open(tmp_file.name, 'rb'),
                                content_type=mime_type)

    def get(self, request, uuid, extension):
        from . utils import TS_ENCODERS_EXT

        if extension not in TS_ENCODERS_EXT:
            raise Http404('Unknown export file extension: %s' % extension)

        # Extract transcoding parameters from request
        start = float(request.GET.get('start', 0))
        stop = float(request.GET.get('stop', -1))
        if stop > start:
            duration = stop - start
        else:
            duration = None
        parameters = {'start': start, 'duration': duration}

        encoder = TS_ENCODERS_EXT[extension]
        mime_type = timeside.core.get_processor(encoder).mime_type()

        if (start, duration) != (0, None):
            uri = self.get_object().get_uri()
            return self.transcode_segment(uri=uri,
                                          start=start,
                                          duration=duration,
                                          encoder_pid=encoder,
                                          mime_type=mime_type)
        # Get or Create Processor = encoder
        processor, created = models.Processor.objects.get_or_create(pid=encoder)
        # Get or Create Preset with processor
        preset, created = models.Preset.objects.get_or_create(processor=processor)
        # Get Result with preset and item
        item = self.get_object()
        try:
            result = models.Result.objects.get(item=item, preset=preset)
            if not os.path.exists(result.file.path):
                # Result exists but not file (may have been deleted)
                result.delete()
                return self.get(request, uuid, extension)
            # Result and file exist --> OK
            return FileResponse(open(result.file.path, 'rb'),
                                content_type=result.mime_type)
        except models.Result.DoesNotExist:
            # Result does not exist
            # the corresponding task has to be created and run
            task, created = models.Task.objects.get_or_create(
                experience=preset.get_single_experience(),
                selection=item.get_single_selection())
            task.run(wait=True)
            return self.get(request, uuid, extension)
            # response = StreamingHttpResponse(streaming_content=stream_from_task(task),
            #                                 content_type=mime_type)
            # return response


class PlayerView(TemplateView):
    template_name = "timeside/player.html"
