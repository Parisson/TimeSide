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

from timeside.server.models import *
from rest_framework import serializers
import django.db.models
from django.contrib.auth.models import User

import numpy as np


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    waveform_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    audio_duration = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('uuid', 'url', 'title', 'description', 'mime_type', 'source_file',
                    'source_url', 'waveform_url', 'audio_url', 'audio_duration')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
            }

    def get_url(self, obj):
        from rest_framework.reverse import reverse
        request = self.context['request']
        return reverse('item-detail', kwargs={'uuid': obj.uuid}, request=request)

    def get_waveform_url(self, obj):
        return (self.get_url(obj)+'waveform/')

    def get_audio_url(self, obj):
        obj_url = self.get_url(obj)
        return {'mp3': obj_url + 'download/mp3',
                'ogg': obj_url + 'download/ogg'}

    def get_audio_duration(self, obj):
        import timeside.core as ts_core
        decoder = ts_core.get_processor('file_decoder')(uri=obj.get_source()[0])
        return decoder.uri_total_duration


class ItemWaveformSerializer(ItemSerializer):

    item_url = serializers.SerializerMethodField('get_url')
    waveform = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ('item_url', 'title', 'waveform_url', 'waveform')

    def get_waveform(self, obj):
        request = self.context['request']
        start = float(request.GET.get('start', 0))
        stop = float(request.GET.get('stop', -1))
        nb_pixels = int(request.GET.get('nb_pixels', 1024))
        #plop = self.context['plop']

        from .utils import get_or_run_proc_result
        result = get_or_run_proc_result('waveform_analyzer', item=obj)
        import h5py

        result_id = 'waveform_analyzer'
        wav_res = h5py.File(result.hdf5.path, 'r').get(result_id)

        duration = wav_res['audio_metadata'].attrs['duration']
        samplerate = wav_res['data_object']['frame_metadata'].attrs['samplerate']

        if start < 0:
            start = 0
        if start > duration:
            raise serializers.ValidationError("start must be less than duration")
        if stop == -1:
            stop = duration

        if stop > duration:
            stop = duration

        min_values = np.zeros(nb_pixels)
        max_values = np.zeros(nb_pixels)
        time_values = np.linspace(start=start, stop=stop, num=nb_pixels+1,
                                  endpoint=True)

        sample_values =  np.round(time_values*samplerate).astype('int')

        for i in xrange(nb_pixels):
            values = wav_res['data_object']['value'][sample_values[i]:sample_values[i+1]]
            min_values[i] = np.min(values)
            max_values[i] = np.max(values)

        return {'start': start,
                'stop': stop,
                'nb_pixels': nb_pixels,
                'time': time_values[0:-1],
                'min': min_values,
                'max': max_values}


class SelectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Selection
        fields = ('uuid', 'items', 'selections', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'selections': {'lookup_field': 'uuid'},
            'items': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
            }


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Experience
        fields = ('uuid', 'presets', 'is_public', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'presets': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
            }

class ProcessorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Processor
        fields = ('url', 'pid', 'version')
        extra_kwargs = {
            'url': {'lookup_field': 'pid'}
            }


class SubProcessorSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = SubProcessor
        fields = ('url', 'name', 'processor', 'sub_processor_id')
        extra_kwargs = {
            'url': {'lookup_field': 'sub_processor_id'},
            'processor': {'lookup_field': 'pid'}
            }

            
class PresetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Preset
        fields = ('url', 'uuid', 'processor', 'parameters')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'processor': {'lookup_field': 'pid'}
            }

    def validate_parameters(self, attrs, source):

        import timeside.core
        proc = timeside.core.get_processor(attrs['processor'].pid)
        if proc.type == 'analyzer':
            processor = proc()
            default_params = processor.get_parameters()
            default_msg = "Defaut parameters:\n%s" % default_params

            try:
                processor.validate_parameters(attrs[source])
            except ValueError as e:
                msg = '\n'.join([str(e), default_msg])
                raise serializers.ValidationError(msg)
            except KeyError as e:
                msg = '\n'.join(['KeyError :' + unicode(e), default_msg])
                raise serializers.ValidationError(msg)

            processor.set_parameters(attrs[source])
            attrs[source] =  processor.get_parameters()
        return attrs


class ResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Result
        fields = ('uuid', 'item', 'preset', 'status', 'hdf5', 'file')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'preset':  {'lookup_field': 'uuid'}}


class Result_ReadableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Result
        fields = ('uuid', 'preset', 'hdf5', 'file', 'mime_type')
        read_only_fields = fields
        depth = 2


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ('url', 'uuid', 'experience', 'selection', 'status', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'experience': {'lookup_field': 'uuid'},
            'selection':  {'lookup_field': 'uuid'},
            'author' : {'lookup_field': 'username'}}


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
            }

class AnalysisSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AnalysisTrack
        fields = ('url', 'title', 'preset', 'sub_processor')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'preset': {'lookup_field': 'uuid'},
            'sub_processor': {'lookup_field': 'sub_processor_id'}
            }
            



