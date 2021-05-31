# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2014 Guillaume Pellerin <yomguy@parisson.com>

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

import os

import numpy as np
from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response
# from builtins import str

from django.contrib.sites.models import Site

import timeside.server as ts
from timeside.server.models import _RUNNING, _PENDING

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from jsonschema import ValidationError
import json
import h5py

from timeside.core.analyzer import AnalyzerResult

from .utils import get_result


class ItemPlayableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ts.models.Item
        fields = ('player_url')

    def get_player_url(self, obj):
        current_site = Site.objects.get_current()
        return 'https://'                   \
            + current_site.domain           \
            + reverse('timeside-player')    \
            + '#item/' + str(obj.uuid)      \
            + '/'


class ItemListSerializer(ItemPlayableSerializer):

    player_url = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'title', 'description', 'player_url',
                  'source_file', 'source_url', 'mime_type')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }

    def get_url(self, obj):
        print(self.context.keys())
        request = self.context['request']
        return reverse(
            'item-detail',
            kwargs={'uuid': obj.uuid},
            request=request
            )


class AudioUrlSerializer(serializers.Serializer):

    mp3 = serializers.URLField(read_only=True)
    ogg = serializers.URLField(read_only=True)
    flac = serializers.URLField(read_only=True)

    def to_representation(self, instance):
        print(self.context.keys())
        request = self.context['request']
        extensions = ['mp3', 'ogg', 'flac']
        self.audio_url = {
            ext:
            reverse(
                'item-transcode-api',
                kwargs={'uuid': instance.uuid, 'extension': ext},
                request=request
                )
            for ext in extensions
            }
        return self.audio_url


class ItemSerializer(ItemPlayableSerializer):

    waveform_url = serializers.SerializerMethodField()
    player_url = serializers.SerializerMethodField()
    audio_url = AudioUrlSerializer(
        source='*',
        many=False,
        read_only=True,
    )
    annotation_tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='annotationtrack-detail',
        lookup_field='uuid'
    )
    analysis_tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='analysistrack-detail',
        lookup_field='uuid'
    )

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'player_url',
                  'title', 'description',
                  'source_file', 'source_url', 'mime_type',
                  'audio_url', 'audio_duration', 'samplerate',
                  'external_uri',
                  'external_id',
                  'waveform_url',
                  'annotation_tracks',
                  'analysis_tracks',
                  'provider',
                  )
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'provider': {'lookup_field': 'uuid'}
        }

        read_only_fields = (
            'url', 'uuid',
            'audio_duration', 'samplerate',
            'player_url',
            )

    def get_url(self, obj):
        request = self.context['request']
        return reverse(
            'item-detail',
            kwargs={'uuid': obj.uuid},
            request=request
            )

    def get_waveform_url(self, obj):
        request = self.context['request']
        return reverse(
            'item-waveform',
            kwargs={'uuid': obj.uuid},
            request=request
            )


class WaveformSerializer(serializers.Serializer):
    """Populate waveform"""
    start = serializers.IntegerField(default=0)
    stop = serializers.IntegerField(default=-1)
    nb_pixels = serializers.IntegerField(min_value=0)
    min = serializers.ListField(
        child=serializers.FloatField(read_only=True)
        )
    max = serializers.ListField(
        child=serializers.FloatField(read_only=True)
        )
    time = serializers.ListField(
        child=serializers.IntegerField(read_only=True)
        )

    def to_representation(self, instance):
        request = self.context['request']
        self.start = float(request.GET.get('start', 0))
        self.stop = float(request.GET.get('stop', -1))
        self.nb_pixels = int(request.GET.get('nb_pixels', 1024))

        from .utils import get_or_run_proc_result
        result = get_or_run_proc_result(
            'waveform_analyzer',
            item=instance,
            user=request.user
        )
        import h5py

        result_id = 'waveform_analyzer'
        wav_res = h5py.File(result.hdf5.path, 'r').get(result_id)

        duration = wav_res['audio_metadata'].attrs['duration']
        samplerate = wav_res['data_object'][
                'frame_metadata'].attrs['samplerate']

        if self.start < 0:
            self.start = 0
        if self.start > duration:
            raise serializers.ValidationError(
                "start must be less than duration")
        if self.stop == -1:
            self.stop = duration

        if self.stop > duration:
            self.stop = duration

        # nb_pixel must not be to big to keep minimum 2 samples per pixel
        # to ensure 2 different values for min and max
        cap_value = int(samplerate * abs(self.stop - self.start) / 2)
        if self.nb_pixels > cap_value:
            self.nb_pixels = cap_value

        self.min_values = np.zeros(self.nb_pixels)
        self.max_values = np.zeros(self.nb_pixels)
        self.time_values = np.linspace(
            start=self.start,
            stop=self.stop,
            num=self.nb_pixels + 1,
            endpoint=True
            )

        sample_values = np.round(self.time_values * samplerate).astype('int')

        for i in range(self.nb_pixels):
            values = wav_res['data_object']['value'][
                sample_values[i]:sample_values[i + 1]]
            if values.size:
                self.min_values[i] = np.min(values)
                self.max_values[i] = np.max(values)

        return {'start': self.start,
                'stop': self.stop,
                'nb_pixels': self.nb_pixels,
                'time': self.time_values[0:-1],
                'min': self.min_values,
                'max': self.max_values}


class ItemWaveformSerializer(ItemSerializer):

    item_url = serializers.SerializerMethodField('get_url')
    waveform = WaveformSerializer(
        source='*',
        many=False,
        read_only=True,
        )
    waveform_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('item_url', 'title', 'waveform_url',
                  'waveform', 'waveform_image_url')
        # depth = 2
        # extra_kwargs

    def get_waveform_image_url(self, obj):
        request = self.context['request']
        from .utils import get_or_run_proc_result
        result = get_or_run_proc_result(
            'waveform_analyzer',
            item=obj,
            user=request.user
        )
        return reverse('timeside-result-visualization',
                       kwargs={'uuid': result.uuid},
                       request=request)+'?id=waveform_analyzer'


class ItemAnalysisSerializer(serializers.HyperlinkedModelSerializer):

    analysis_url = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'analysis_url')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }

    def get_url(self, obj):
        request = self.context['request']
        return reverse('item-detail', kwargs={'uuid': obj.uuid},
                       request=request)

    def get_analysis_url(self, obj):
        analysis_url = self.get_url(obj) + 'analysis/'
        analysis = ts.models.Analysis.objects.all()

        return {a.title: analysis_url + a.uuid for a in analysis}


class ItemAnnotationsSerializer(serializers.HyperlinkedModelSerializer):

    annotations_url = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'annotations_url')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }

    def get_url(self, obj):
        request = self.context['request']
        return reverse(
            'item-detail',
            kwargs={'uuid': obj.uuid},
            request=request
            )

    def get_annotations_url(self, obj):
        annotations_url = self.get_url(obj) + 'annotations/'
        annotations = ts.models.Annotation.objects.all()

        return {a.title: annotations_url + a.uuid for a in annotations}


class ItemAnalysisResultSerializer(serializers.HyperlinkedModelSerializer):

    # analysis_url = serializers.HyperlinkedRelatedField(read_only=True,
    #
    #    )
    audio_duration = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    analysis_uuid = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'audio_duration',
                  'analysis_uuid', 'analysis_url', 'result')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
        }

    def get_url(self, obj):
        request = self.context['request']
        return reverse(
            'item-detail',
            kwargs={'uuid': obj.uuid},
            request=request
            )

    def get_analysis_uuid(self, obj):
        return self.lookup_url_kwarg['analysis_uuid']

    def get_analysis_url(self, obj):
        analysis_url = self.get_url(obj) + 'analysis/'
        analysis_uuid = self.get_analysis_uuid(obj)

        return analysis_url + analysis_uuid

    def get_audio_duration(self, obj):
        return obj.get_audio_duration()

    def get_result(self, obj):
        analysis_uuid = self.get_analysis_uuid(obj)
        try:
            analysis, c = ts.models.Analysis.objects.get(uuid=analysis_uuid)
        except ts.models.Analysis.DoesNotExist:
            return {'Unknown analysis': analysis_uuid}

        preset = analysis.preset

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        result = get_result(item=obj, preset=preset, user=user)
        if isinstance(result, ts.models.Result):
            res_msg = result.uuid
        else:
            res_msg = result
        return {'analysis': analysis.uuid,
                'item': item.uuid}


class SelectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Selection
        fields = ('title', 'uuid', 'url', 'items', 'selections', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'selections': {'lookup_field': 'uuid'},
            'items': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
        }
        read_only_fields = ('url', 'uuid', 'title')

    def update(self, instance, validated_data):
        instance.author = validated_data.get('title', instance.author)
        instance.title = validated_data.get('title', instance.title)
        selections = validated_data.get('selections')
        if selections:
            for selection in selections:
                instance.selections.add(selection)
        items = validated_data.get('items')
        if items:
            for item in items:
                instance.items.add(item)
        instance.save()

        return instance


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Experience
        fields = ('title', 'uuid', 'url', 'presets', 'is_public', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'presets': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
        }
        read_only_fields = ('url', 'uuid',)


class ProcessorSerializer(serializers.HyperlinkedModelSerializer):

    pid = serializers.ChoiceField(choices=ts.models.get_processor_pids())
    parameters_schema = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Processor
        fields = ('name', 'pid', 'url', 'version', 'parameters_schema')
        extra_kwargs = {
            'url': {'lookup_field': 'pid'}
        }

    def get_parameters_schema(self, obj):
        return obj.get_parameters_schema()


class ProcessorListSerializer(serializers.HyperlinkedModelSerializer):

    pid = serializers.ChoiceField(choices=ts.models.get_processor_pids())

    class Meta:
        model = ts.models.Processor
        fields = ('name', 'pid', 'url', 'version')
        extra_kwargs = {
            'url': {'lookup_field': 'pid'}
        }


class ParametersSchemaSerializer(serializers.HyperlinkedModelSerializer):

    parameters_schema = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Processor
        fields = ('parameters_schema',)

    def get_parameters_schema(self, obj):
        return obj.get_parameters_schema()


class ParametersDefaultSerializer(serializers.HyperlinkedModelSerializer):

    parameters_default = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Processor
        fields = ('parameters_default',)

    def get_parameters_default(self, obj):
        return obj.get_parameters_default()


class SubProcessorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.SubProcessor
        fields = ('url', 'name', 'processor', 'sub_processor_id')
        extra_kwargs = {
            'url': {'lookup_field': 'sub_processor_id'},
            'processor': {'lookup_field': 'pid'}
        }


class PresetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Preset
        fields = ('url', 'uuid', 'processor', 'parameters')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'processor': {'lookup_field': 'pid'}
        }
        read_only_fields = ('url', 'uuid',)

    def validate(self, data):

        import timeside.core
        proc = timeside.core.get_processor(data['processor'].pid)
        if proc.type == 'analyzer':
            processor = proc()
            default_params = processor.get_parameters()
            default_msg = "Defaut parameters:\n%s" % default_params

            if not data['parameters']:
                data['parameters'] = '{}'
            try:
                processor.validate_parameters(json.loads(data['parameters']))
            except ValidationError as e:
                msg = '\n'.join([str(e), default_msg])
                raise serializers.ValidationError(msg)
            except KeyError as e:
                msg = '\n'.join(['KeyError :' + str(e), default_msg])
                raise serializers.ValidationError(msg)

            processor = proc(**json.loads(data['parameters']))
            data['parameters'] = json.dumps(processor.get_parameters())
        return data


class ResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Result
        fields = ('uuid', 'url', 'item', 'preset', 'status',
                  'mime_type', 'hdf5', 'file', 'run_time')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'preset': {'lookup_field': 'uuid'}
        }
        read_only_fields = ('uuid',)


class VisualizationSerializer(serializers.Serializer):
    """
    A read-only serializer that deals with subprocessor results
    """
    subprocessor_id = serializers.SerializerMethodField()
    start = serializers.FloatField(default=0)
    stop = serializers.FloatField(default=-1)
    width = serializers.IntegerField(default=1024)
    height = serializers.IntegerField(default=128)

    def to_representation(self, obj):
        request = self.context['request']
        self.subprocessor_id = str(request.GET.get('subprocessor_id', ''))
        self.start = float(request.GET.get('start', 0))
        self.stop = float(request.GET.get('stop', -1))
        self.width = int(float(request.GET.get('width', 1024)))
        self.height = int(float(request.GET.get('height', 128)))

        if not self.subprocessor_id:
            self.subprocessor_id = self.get_subprocessor_id(obj)

        if not obj.has_hdf5():
            raise serializers.ValidationError(
                    "result must have an hdf5 file to be visualized")

        hdf5_result = h5py.File(obj.hdf5.path, 'r').get(self.subprocessor_id)
        result = AnalyzerResult().from_hdf5(hdf5_result)
        duration = hdf5_result['audio_metadata'].attrs['duration']
        samplerate = hdf5_result['data_object'][
            'frame_metadata'].attrs['samplerate']

        if self.start < 0:
            self.start = 0
        if self.start > duration:
            raise serializers.ValidationError(
                "start must be less than duration")
        if self.stop == -1:
            self.stop = duration

            if self.stop > duration:
                self.stop = duration

        # following same cap_value for width
        # as for waveform's nb_pixel serialization
        cap_value = int(samplerate * abs(self.stop - self.start) / 2)
        if self.width > cap_value:
            self.width = cap_value

        from io import BytesIO
        pil_image = result._render_PIL(
            size=(self.width, self.height),
            dpi=80, xlim=(self.start, self.stop)
            )
        image_buffer = BytesIO()
        pil_image.save(image_buffer, 'PNG')
        return image_buffer.getvalue()

    def get_subprocessor_id(self, obj):
        request = self.context['request']
        subprocessor_id = request.GET.get('subprocessor_id', '')
        if subprocessor_id:
            return subprocessor_id
        else:
            if not obj.has_hdf5():
                raise serializers.ValidationError(
                    "result must have an hdf5 file to be visualized")
            hdf5_file = h5py.File(obj.hdf5.path, 'r')
            if len(hdf5_file.keys()) > 1:
                raise serializers.ValidationError(
                        """a subprocessor id must be specified
                        for result with multiple ids"""
                        )
            else:
                for key in hdf5_file.keys():
                    return key


class ResultVisualizationSerializer(serializers.HyperlinkedModelSerializer):
    visualization = VisualizationSerializer(
        source='*',
        many=False,
        read_only=True,
        )

    class Meta:
        model = ts.models.Result
        fields = ('visualization',)


class AnalysisResultContentSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that deals with analyzers hdf5 content
    """

    def to_representation(self, obj):
        # subprocessor_id = self.context.get('request').query_params.get('id')

        # start = float(self.context.get('request').query_params.get('start', 0))
        # stop = float(self.context.get('request').query_params.get('stop', -1))
        # width = int(self.context.get(
        #     'request'
        #     ).query_params.get('width', 1024))
        # height = int(self.context.get(
        #     'request'
        #     ).query_params.get('height', 128))

        # import h5py
        # hdf5_result = h5py.File(obj.hdf5.path, 'r').get(subprocessor_id)
        # from timeside.core.analyzer import AnalyzerResult
        # result = AnalyzerResult().from_hdf5(hdf5_result)
        # duration = hdf5_result['audio_metadata'].attrs['duration']

        # if start < 0:
        #     start = 0
        # if start > duration:
        #     raise serializers.ValidationError(
        #         "start must be less than duration")
        # if stop == -1:
        #     stop = duration

        #     if stop > duration:
        #         stop = duration
        subprocessor_id = self.context.get('request').query_params.get('id')
        import h5py
        hdf5_file = h5py.File(obj.hdf5.path, 'r')
        if subprocessor_id:
            hdf5_result = h5py.File(obj.hdf5.path, 'r').get(subprocessor_id)
        else:
            hdf5_result = hdf5_file.visit(hdf5_file.get)
        from timeside.core.analyzer import AnalyzerResult
        result = AnalyzerResult().from_hdf5(hdf5_result)
        return result.as_dict()
        # from timeside.core.analyzer import AnalyzerResult
        # container = AnalyzerResult().from_hdf5(obj.hdf5.path)
        # return container  # container.to_json()
        # # SMELLS to_json did double serialization


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Task
        fields = ('url', 'uuid', 'experience',
                  'selection', 'status', 'author', 'item')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'experience': {'lookup_field': 'uuid'},
            'selection': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'},
            'item': {'lookup_field': 'uuid'}
            }


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.User
        fields = ('url', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):

    parameters_schema = serializers.JSONField()

    class Meta:
        model = ts.models.Analysis
        fields = ('url', 'uuid',
                  'title', 'description', 'render_type',
                  'preset', 'sub_processor',
                  'parameters_schema')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'preset': {'lookup_field': 'uuid'},
            'sub_processor': {'lookup_field': 'sub_processor_id'}
        }
        read_only_fields = ('url', 'uuid',)


class AnalysisTrackSerializer(serializers.HyperlinkedModelSerializer):

    result_url = serializers.SerializerMethodField()
    parameters_schema = serializers.SerializerMethodField()
    parameters_default = serializers.SerializerMethodField()
    parametrizable = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.AnalysisTrack
        fields = ('url', 'uuid',
                  'title', 'description',
                  'analysis', 'item', 'result_url',
                  'parameters_schema', 'parameters_default',
                  'parametrizable')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'analysis': {'lookup_field': 'uuid'},
        }
        read_only_fields = ('url', 'uuid',)

    # def create(self, validated_data):
    #     item = validated_data['item']
    #     analysis = validated_data['analysis']

    #     preset = analysis.preset

    #     result = get_result(item=item, preset=preset)

    #     if isinstance(result, Result):
    #        res_msg = result.uuid
    #     else:
    #        res_msg = result
    #     return {'analysis': analysis.uuid,
    #            'item': item.uuid}

    #     return super(AnalysisTrackSerializer, self).create(validated_data)

    def get_result_uuid(self, obj):

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        result = get_result(
            item=obj.item, 
            preset=obj.analysis.preset,
            user=user,
            test=obj.analysis.test
        )
        if isinstance(result, ts.models.Result):
            self._result_uuid = result.uuid
            return result.uuid
        else:
            self._result_uuid = None
        return self._result_uuid

    def get_result_url(self, obj):
        self.get_result_uuid(obj)
        if self._result_uuid is not None:

            url_kwargs = {'uuid': self._result_uuid}
            request = self.context['request']
            return reverse(
                'result-detail',
                kwargs=url_kwargs,
                request=request
                )
        else:
            return 'Task running'

    def get_parameters_schema(self, obj):
        return obj.analysis.parameters_schema

    def get_parameters_default(self, obj):
        return obj.analysis.preset.processor.get_parameters_default()

    def get_parametrizable(self, obj):
        schema = self.get_parameters_schema(obj)
        if not schema or not schema['properties']:
            return False
        # TODO : Manage User permission to parametrize Analysis
        return True

    # def get_url(self, obj, view_name, request, format):
    # url_kwargs = {
    # 'item_uuid': obj.item.uuid,
    # 'analysis_uuid': obj.analysis.uuid.pk
    # }
    # return reverse(view_name, kwargs=url_kwargs, request=request,
    # format=format)


class AnnotationSerializer_inTrack(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Annotation
        fields = ('url', 'uuid',
                  'title', 'description',
                  'start_time', 'stop_time')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'track': {'lookup_field': 'uuid'},
        }
        read_only_fields = ('url', 'uuid',)


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Annotation
        fields = ('url', 'uuid', 'track',
                  'title', 'description',
                  'start_time', 'stop_time')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'track': {'lookup_field': 'uuid'},
        }
        read_only_fields = ('uuid',)


class AnnotationTrackSerializer(serializers.HyperlinkedModelSerializer):

    annotations = AnnotationSerializer_inTrack(many=True, read_only=True)

    class Meta:
        model = ts.models.AnnotationTrack
        fields = ('url', 'uuid', 'item',
                  'title', 'description',
                  'author',
                  'is_public',
                  'overlapping',
                  'annotations')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'},
            'annotations': {'lookup_field': 'uuid'},
        }
        read_only_fields = ('uuid',)


class ProviderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Provider
        fields = ('pid', 'uuid', 'source_access')
        read_only_fields = ('uuid',)
