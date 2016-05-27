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


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    waveform_url = serializers.SerializerMethodField('get_waveform_url')
    
    class Meta:
        model = Item
        lookup_field='uuid'
        fields = ('url', 'title', 'description', 'mime_type', 'source_file', 'source_url', 'waveform_url')

    def get_url(self,obj):
        from rest_framework.reverse import reverse
        request = self.context['request']
        return reverse('item-detail',kwargs={'uuid':obj.uuid},request=request)
    
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
        start = float(request.GET.get('start', 0))
        stop = float(request.GET.get('stop', -1))
        nb_pixels = int(request.GET.get('nb_pixels', 1024))
        #plop = self.context['plop']

        from rest_framework import status
        from rest_framework.response import Response
        # Dummy signal
        # Gaussian pulse of 10s at 16000 Hz 
        import numpy as np
        from scipy import signal
        duration = 10
        t = np.linspace(-1, 1, duration * 16000, endpoint=False)
        sig = abs(signal.gausspulse(t, fc=5)) * np.random.randn(duration * 16000)
        t = (t + 1)/2 * duration
                
        if start > duration:
            raise serializers.ValidationError("start must be less than duration")
        if stop == -1:
            stop = duration

        indexes = (t>=start) & (t<stop)
        sig = sig[indexes]
        t = t[indexes]
        missing_samples = len(sig) % nb_pixels
        if missing_samples != 0:
            sig = np.append(sig, np.zeros(missing_samples))
            
        blocksize = len(sig) // nb_pixels

        min_values = []
        max_values = []
        time_values = []
        for i in xrange(0,nb_pixels):
            min_values.append(min(sig[i*blocksize:(i+1)*blocksize]))
            max_values.append(max(sig[i*blocksize:(i+1)*blocksize]))
            time_values.append(t[i*blocksize])
        return {'start': start,
                'stop': stop,
                'nb_pixels': nb_pixels,
                'time': time_values,
                'min': min_values,
                'max': max_values}


class SelectionSerializer(serializers.HyperlinkedModelSerializer):

    items = serializers.HyperlinkedRelatedField(many=True,
                                                view_name='item-detail',
                                                lookup_field='uuid')

    class Meta:
        model = Selection
        #lookup_field='uuid'
        # fields = ('id', 'items', 'selections', 'author')


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Experience
        
        # fields = ('id', 'presets', 'experiences', 'is_public', 'author')


class ProcessorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Processor
        lookup_field='pid'

        #fields = ('id', 'pid', 'version')


class PresetSerializer(serializers.HyperlinkedModelSerializer):

    processor = serializers.HyperlinkedRelatedField(view_name='processor-detail',
                                                    lookup_field='pid')

    
    class Meta:
        model = Preset
        #lookup_field='uuid'
        
        fields = ('url', 'uuid', 'processor', 'parameters')

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

    item = serializers.HyperlinkedRelatedField(read_only=True,
                                               view_name='item-detail',
                                               lookup_field='uuid')
        
    class Meta:
        model = Result
        
        # fields = ('id', 'item', 'preset', 'status', 'hdf5', 'file')


class Result_ReadableSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Result
        fields = ('id', 'preset', 'hdf5', 'file', 'mime_type')
        read_only_fields = fields
        depth = 2
        

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        # fields = ('id', 'experience', 'selection', 'status', 'author')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
