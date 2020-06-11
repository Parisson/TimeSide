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
from django.conf import settings
from django.middleware.csrf import get_token as get_csrf_token

from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.schemas import get_schema_view
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.schemas.openapi import SchemaGenerator
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
# from django.core.urlresolvers import reverse
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.decorators import action
import django_filters.rest_framework as filters


from . import models
from . import serializers
from .utils import (
    get_or_run_proc_result,
    AudioRenderer,
    PNGRenderer,
)

import timeside.core
from timeside.core.analyzer import AnalyzerResultContainer
import os


def stream_from_task(task):
    for chunk in task.run(streaming=True):
        yield chunk
    task.save()


class UUIDViewSetMixin(object):

    lookup_field = 'uuid'
    lookup_value_regex = '[0-9a-z-]+'


class SelectionViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):
    """Set of items and other selections."""
    model = models.Selection
    queryset = model.objects.all()
    serializer_class = serializers.SelectionSerializer


class ItemFilter(filters.FilterSet):
    provider_pid = filters.CharFilter(field_name="provider__pid")

    class Meta:
        model = models.Item
        fields = ['provider_pid', 'external_id']


class ItemViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Item
    queryset = models.Item.objects.all()
    filterset_class = ItemFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ItemListSerializer
        return serializers.ItemSerializer


class AnnotationTrackFilter(filters.FilterSet):
    item_uuid = filters.UUIDFilter(field_name="item__uuid")

    class Meta:
        model = models.AnnotationTrack
        fields = ['item_uuid']


class AnnotationTrackViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.AnnotationTrack
    queryset = model.objects.all()
    serializer_class = serializers.AnnotationTrackSerializer
    filterset_class = AnnotationTrackFilter


class AnnotationFilter(filters.FilterSet):
    track_uuid = filters.UUIDFilter(field_name="track__uuid")

    class Meta:
        model = models.Annotation
        fields = ['track_uuid']


class AnnotationViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Annotation
    queryset = model.objects.all()
    serializer_class = serializers.AnnotationSerializer
    filterset_class = AnnotationFilter


class ItemWaveViewFilter:
    """
    Empty filter used for schema generation

    Adapted from :
    https://github.com/encode/django-rest-framework/blob/8cba4f87ca8e785d1a8c022a7a8ea9649e049c11/rest_framework/filters.py#L19
    """
    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        return queryset

    # For CoreAPI (not used / deprecated)
    def get_schema_fields(self, view):
        return []

    # For OpenAPI
    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'start',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                },
            },
            {
                'name': 'stop',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                },
            },
            {
                'name': 'nb_pixels',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                },
            },
        ]


class ItemWaveView(UUIDViewSetMixin, generics.RetrieveAPIView):
    """Gives audio waveform of an item."""
    schema = AutoSchema(operation_id_base='ItemWaveform')
    model = models.Item
    queryset = model.objects.all()
    serializer_class = serializers.ItemWaveformSerializer
    filter_backends = [ItemWaveViewFilter]

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemWaveView, self).get_context_data(**kwargs)
        # Here we can modify the context
        # context['plop'] = 'plop'
        return context

    def get_serializer_context(self):
        """pass request attribute to serializer"""
        context = super(ItemWaveView, self).get_serializer_context()
        # context['plop'] = 92
        return context


class ExperienceViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):
    """Set of presets and other experiences."""
    model = models.Experience
    queryset = model.objects.all()
    serializer_class = serializers.ExperienceSerializer


class ProcessorViewSet(viewsets.ReadOnlyModelViewSet):
    """Audio process to compute on items given potential parameters"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = models.Processor
    queryset = model.objects.all()
    serializer_class = serializers.ProcessorSerializer
    lookup_field = 'pid'
    lookup_value_regex = '[0-9a-z_]+'

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProcessorListSerializer
        return serializers.ProcessorSerializer

    @action(detail=True, methods=['get'])
    def parameters_schema(self, request, pid=None):
        serializer = serializers.ParametersSchemaSerializer(self.get_object())
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def parameters_default(self, request, pid=None):
        serializer = serializers.ParametersDefaultSerializer(self.get_object())
        return Response(serializer.data)


class SubProcessorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Store a result id associated with a given Processor,
    i.e. the id of one of the different process it does.
    """
    model = models.SubProcessor
    queryset = model.objects.all()
    serializer_class = serializers.SubProcessorSerializer
    lookup_field = 'sub_processor_id'
    lookup_value_regex = '[0-9a-z_.]+'


class ResultFilter(filters.FilterSet):
    item_uuid = filters.UUIDFilter(field_name="item__uuid")
    preset_uuid = filters.UUIDFilter(field_name="preset__uuid")

    class Meta:
        model = models.Result
        fields = ['item_uuid', 'preset_uuid']


class ResultViewSet(UUIDViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """Result of processing on items."""
    model = models.Result
    queryset = model.objects.all()
    serializer_class = serializers.ResultSerializer
    filterset_class = ResultFilter

    # def get_queryset(self): TODO
    #     return self.queryset \
    #         .filter(item__uuid=self.kwargs.get('project_id')) \
    #         .filter(author=self.request.user)


class ResultVisualizationViewFilter:
    """
    Empty filter used for schema generation

    Adapted from :
    https://github.com/encode/django-rest-framework/blob/8cba4f87ca8e785d1a8c022a7a8ea9649e049c11/rest_framework/filters.py#L19
    """
    def filter_queryset(self, request, queryset, view):
        """
        Return a filtered queryset.
        """
        return queryset

    # For CoreAPI (not used / deprecated)
    def get_schema_fields(self, view):
        return []

    # For OpenAPI
    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'subprocessor_id',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                },
            },
            {
                'name': 'start',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                    'default': 0,
                },
            },
            {
                'name': 'stop',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                    'default': 0,
                },
            },
            {
                'name': 'width',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                    'default': 1024,
                },
            },
            {
                'name': 'height',
                'required': False,
                'in': 'query',
                'description': '',
                'schema': {
                    'type': 'number',
                    'default': 128,
                },
            },
        ]


class ResultVisualizationViewSet(UUIDViewSetMixin, generics.RetrieveAPIView):
    """PNG rendering of 2D numerical data (example: a spectrogram)."""

    model = models.Result
    schema = AutoSchema(operation_id_base='ResultVisualization')
    queryset = model.objects.all()
    filter_backends = [ResultVisualizationViewFilter]
    serializer_class = serializers.ResultVisualizationSerializer
    renderer_classes = (PNGRenderer, )

    def get(self, request, *args, **kwargs):
        try:
            result = models.Result.objects.get(uuid=kwargs['uuid'])
            serializer = serializers.ResultVisualizationSerializer(
                result,
                context={'request': request}
                )
            return Response(
                serializer.data['visualization'],
                content_type='image/png',
                )
        except ValidationError as e:
            return Response(
                serializer.data,
                content_type='application/json',
                )


class PresetViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):
    """Processor with its potential parameters."""
    model = models.Preset
    queryset = model.objects.all()
    serializer_class = serializers.PresetSerializer


class TaskViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):
    """Experience applied to a selection or a single item."""
    model = models.Task
    queryset = model.objects.all()
    serializer_class = serializers.TaskSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Users of the API able to share data."""
    model = models.User
    queryset = model.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class AnalysisViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.Analysis
    queryset = model.objects.all()
    serializer_class = serializers.AnalysisSerializer


class AnalysisTrackFilter(filters.FilterSet):
    item_uuid = filters.UUIDFilter(field_name="item__uuid")

    class Meta:
        model = models.Result
        fields = ['item_uuid']


class AnalysisTrackViewSet(UUIDViewSetMixin, viewsets.ModelViewSet):

    model = models.AnalysisTrack
    serializer_class = serializers.AnalysisTrackSerializer
    filterset_class = AnalysisTrackFilter

    def get_queryset(self):
        """
        Optionally restricts the returned purchases analysis track to
        a given analysis and/or a given item,
        by filtering against `analysis` and `item` query parameters in the URL.
        Query parameters values should be analysis' or of the item's uuid.
        """
        queryset = self.model.objects.all()
        analysis_uuid = self.request.query_params.get('analysis', None)
        item_uuid = self.request.query_params.get('item', None)
        if analysis_uuid is not None:
            queryset = queryset.filter(
                analysis__uuid__startswith=analysis_uuid
                )
        if item_uuid is not None:
            queryset = queryset.filter(item__uuid__startswith=item_uuid)

        return queryset

    @action(detail=True, methods=['post'])
    def set_parameters(self, request, uuid=None):
        # Get current Analysis track Preset
        track = self.get_object()
        context = {'request': request}
        preset_data = serializers.PresetSerializer(track.analysis.preset,
                                                   context=context).data
        # Create a new Preset from parameters post in request data
        preset_data['parameters'] = json.dumps(request.data)
        preset_serializer = serializers.PresetSerializer(data=preset_data,
                                                         context=context)
        if preset_serializer.is_valid():
            preset = preset_serializer.save()
            return Response(
                data='Preset is Valid but method not implemented yet',
                status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
        else:
            return Response(data=preset_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # Create a new Analysis with this Preset
        analysis_data = serializers.AnalysisSerializer(track.analysis,
                                                       context=context).data
        # Update preset field
        analysis_data['preset'] = preset_serializer.data['url']

        analysis_serializer = serializers.AnalysisSerializer(
            data=analysis_data,
            context=context
            )
        if analysis_serializer.is_valid():
            analysis = analysis_serializer.save()
        else:
            return Response(data=analysis_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        # Update Analysis track with partial data
        new_analysis = {'analysis': analysis_serializer.data['url']}
        serializer_track = self.serializer_class(track,
                                                 data=new_analysis,
                                                 context=context,
                                                 partial=True)

        # Return Analysis Track data as response to POST request
        if serializer_track.is_valid():
            serializer_track.save()
            return Response(data=serializer_track.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(data=serializer_track.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def parameters_default(self, request, uuid=None):
        serializer = serializers.ParametersDefaultSerializer(self.get_object())
        return Response(serializer.data)


class ResultAnalyzerView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(uuid=kwargs['uuid'])
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
        segment_result.data_object.to_sonic_visualiser(
            svenv_file=abs_tmp_sv_file,
            audio_file=audio_file
            )
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
        result = models.Result.objects.get(uuid=kwargs['uuid'])
        return FileResponse(open(result.file.path, 'rb'),
                            content_type='image/png')


class ResultEncoderView(View):

    model = models.Result

    def get(self, request, *args, **kwargs):
        result = models.Result.objects.get(uuid=kwargs['uuid'])
        return FileResponse(open(result.file.path, 'rb'),
                            content_type=result.mime_type)


class ItemDetailExport(DetailView):
    """Export all results of an item."""
    model = models.Item
    template_name = 'timeside/item_detail_export.html'

    def get_object(self):
        return get_object_or_404(models.Item, uuid=self.kwargs.get("uuid"))

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

                for res_id, res in container.items():
                    if res.time_mode == 'segment':
                        if res.data_mode == 'label':
                            Results[proc_id]['list'][res_id] = {
                                'elan': True,
                                'sv': True,
                                'Parameters': res.parameters,
                                'name': res.name}
                            if res.time_mode == 'framewise':
                                if res.data_mode == 'value':
                                    Results[proc_id]['list'][res_id] = {
                                        'elan': False,
                                        'sv': True,
                                        'Parameters': res.parameters,
                                        'name': res.name}
            elif result.mime_type:
                Results[proc_id]['audio'] = ('audio' in result.mime_type) | (
                    'ogg' in result.mime_type)
                Results[proc_id]['image'] = ('image' in result.mime_type)
                Results[proc_id]['video'] = ('video' in result.mime_type)

        context['Results'] = Results

        return context


class ItemList(ListView):

    model = models.Item
    template_name = 'timeside/item_list.html'


class ItemDetail(DetailView):

    model = models.Item
    template_name = 'timeside/item_detail.html'

    def get_object(self):
        return get_object_or_404(models.Item, uuid=self.kwargs.get("uuid"))

    def get_context_data(self, **kwargs):
        context = super(ItemDetail, self).get_context_data(**kwargs)
        ts_item = {
            'ts_api_root': str(reverse_lazy(
                'api-root', request=self.request
                )),
            'ts_item_uuid': str(self.get_object().uuid)
            }
        context['ts_item'] = json.dumps(ts_item)
        return context


def serve_media(filename, content_type="", buffering=True):
    if not settings.DEBUG:
        return nginx_media_accel(filename,
                                 content_type=content_type,
                                 buffering=buffering)
    else:
        response = FileResponse(open(filename, 'rb'))
        response['Content-Disposition'] = 'attachment; filename=' + filename
        response['Content-Type'] = content_type
        return response


def nginx_media_accel(media_path, content_type="", buffering=True):
    """Send a protected media file through nginx with X-Accel-Redirect"""

    response = HttpResponse()
    url = settings.MEDIA_URL + os.path.relpath(media_path, settings.MEDIA_ROOT)
    filename = os.path.basename(media_path)
    response['Content-Disposition'] = "attachment; filename=%s" % (filename)
    response['Content-Type'] = content_type
    response['X-Accel-Redirect'] = url

    if not buffering:
        response['X-Accel-Buffering'] = 'no'
        # response['X-Accel-Limit-Rate'] = 524288

    return response


class ItemTranscode(DetailView):
    """Transcode an item's audio in a different format."""
    model = models.Item
    renderer_classes = (AudioRenderer,)

    def get_object(self):
        return get_object_or_404(models.Item, uuid=self.kwargs.get("uuid"))

    def transcode_segment(self, uri, start, duration, encoder_pid, mime_type):
        decoder = timeside.core.get_processor('file_decoder')(
            uri, start=start, duration=duration
            )
        import tempfile
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            encoder = timeside.core.get_processor(encoder_pid)(
                tmp_file.name, overwrite=True
                )
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
        else:
            item = self.get_object()
            result = get_or_run_proc_result(encoder, item)
            return serve_media(filename=result.file.path,
                               content_type=result.mime_type)


class PlayerView(TemplateView):
    template_name = "timeside/player.html"


class CsrfToken(viewsets.ViewSet):
    def list(self, request):
        return Response({'csrftoken': get_csrf_token(request)})


class ProviderViewSet(UUIDViewSetMixin, viewsets.ReadOnlyModelViewSet):
    """Audio providers available in the API."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = models.Provider
    queryset = model.objects.all()
    serializer_class = serializers.ProviderSerializer
    search_fields = ('pid')


class ReDocView(TemplateView):
    """TemplateView to serve ReDoc template."""
    permission_classes = [AllowAny]
    template_name = "timeside/redoc.html"
    # `extra_context` provided with view name of `SchemaView`
    extra_context = {'schema_url': 'openapi-schema'}


class CustomSchemaGenerator(SchemaGenerator):
    """
    Generate an OpenAPI v3 schema providing server's prod and staging urls.
    """
    def get_schema(self, request=None, public=False):
        # Adding production and staging server urls ton title and version infos
        schema = super().get_schema()

        # Add production and staging urls to schema
        schema['servers'] = [
                {
                    "url": "https://wasabi.telemeta.org/",
                    "description": "Production server"
                },
                {
                    "url": "https://sandbox.wasabi.telemeta.org/",
                    "description": "Staging server"
                }
        ]

        # Redefine JWT shema fixing the one produced
        # by djangorestframework-simplejwt roots
        schema['security'] = [
                {
                    "bearerAuth": []
                }
        ]
        schema['components']['securitySchemes'] = {
            'bearerAuth':
            {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
        schema['components']['schemas']['TokenObtainPair'] = {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'writeOnly': True},
                'password': {'type': 'string', 'writeOnly': True},
                'refresh': {'type': 'string', 'readOnly': True},
                'access': {'type': 'string', 'readOnly': True},
            },
            'required': ['username', 'password']
            }
        schema['components']['schemas']['TokenRefresh'] = {
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string', 'writeOnly': True},
                'access': {'type': 'string', 'readOnly': True},
                },
            'required': ['refresh']
        }
        schema['components']['schemas']['TokenVerify'] = {
            'type': 'object',
            'properties': {'token': {'type': 'string', 'writeOnly': True}},
            'required': ['token']
        }

        return schema


schema_view = get_schema_view(
    title="TimeSide API",
    description=("RESTful API of TimeSide, "
                 "a scalable audio processing framework."),
    version="1.0.0",
    generator_class=CustomSchemaGenerator,
    permission_classes=[AllowAny],
)
