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


class SelectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Selection
        # fields = ('id', 'items', 'selections', 'author')


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    waveform_url = serializers.SerializerMethodField('get_waveform_url')
    
    class Meta:
        model = Item
        fields = ('url', 'title', 'description', 'mime_type', 'source_file', 'source_url', 'waveform_url')

    def get_url(self,obj):
        from rest_framework.reverse import reverse
        request = self.context['request']
        return reverse('item-detail',kwargs={'pk':obj.pk},request=request)
    
    def get_waveform_url(self, obj):
        return (self.get_url(obj)+'waveform/')

    
class ItemWaveformSerializer(ItemSerializer):

    item_url = serializers.SerializerMethodField('get_url')
    waveform = serializers.SerializerMethodField('get_waveform')
    
    class Meta:
        model = Item
        fields = ('item_url', 'title', 'waveform_url', 'waveform')
    
    def get_waveform(self, obj):
        request = self.context['request']
        start = request.GET.get('start', 0)
        stop = request.GET.get('stop', -1)
        nb_pixels = request.GET.get('nb_pixels', 1024)

        #plop = self.context['plop']

        import numpy as np
        from scipy import signal
        t = np.linspace(-1, 1, nb_pixels, endpoint=False)
        sig = abs(signal.gausspulse(t, fc=5))
                              
        return {'start': start,
                'stop': stop,
                'nb_pixels': nb_pixels,
                'min': -sig,
                'max': sig}


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Experience
        # fields = ('id', 'presets', 'experiences', 'is_public', 'author')


class ProcessorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Processor
        # fields = ('id', 'pid', 'version')


class ResultSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Result
        # fields = ('id', 'item', 'preset', 'status', 'hdf5', 'file')


class Result_ReadableSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Result
        fields = ('id', 'preset', 'hdf5', 'file', 'mime_type')
        read_only_fields = fields
        depth = 2
        

class PresetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Preset
        #fields = ('id', 'processor', 'parameters', 'is_public')

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


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        # fields = ('id', 'experience', 'selection', 'status', 'author')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
