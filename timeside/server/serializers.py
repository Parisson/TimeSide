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

import timeside.server as ts
from timeside.server.models import _DRAFT, _DONE, _RUNNING, _PENDING

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.reverse import reverse

import django.db.models
from django.contrib.auth.models import User

import numpy as np
import os


class ItemSerializer(serializers.HyperlinkedModelSerializer):

    waveform_url = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()
    analysis_url = serializers.SerializerMethodField()
    audio_duration = serializers.SerializerMethodField()


    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'title', 'description', 'mime_type', 'source_file',
                    'source_url', 'waveform_url', 'analysis_url', 'audio_url', 'audio_duration')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
            }

    def get_url(self, obj):
        request = self.context['request']
        return reverse('item-detail', kwargs={'uuid': obj.uuid}, request=request)

    def get_waveform_url(self, obj):
        return (self.get_url(obj)+'waveform/')

    def get_analysis_url(self, obj):
        return (self.get_url(obj)+'analysis/')

    def get_audio_url(self, obj):
        obj_url = self.get_url(obj)
        return {'mp3': obj_url + 'download/mp3',
                'ogg': obj_url + 'download/ogg'}

    def get_audio_duration(self, obj):
        return obj.get_audio_duration()


class ItemWaveformSerializer(ItemSerializer):

    item_url = serializers.SerializerMethodField('get_url')
    waveform = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
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

class ItemAnalysisSerializer(serializers.HyperlinkedModelSerializer):

    analysis_url = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'analysis_url')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
            }

    def get_url(self, obj):
        from rest_framework.reverse import reverse
        request = self.context['request']
        return reverse('item-detail', kwargs={'uuid': obj.uuid}, request=request)

    def get_analysis_url(self, obj):
        analysis_url = self.get_url(obj) + 'analysis/'
        analysis = ts.models.Analysis.objects.all()
        
        return { a.title: analysis_url + a.uuid for a in analysis}

def get_result(item, preset, wait=True):
    # Get Result with preset and item
    try:
        result = ts.models.Result.objects.get(item=item, preset=preset)
        if not os.path.exists(result.hdf5.path):
            # Result exists but there is no file (may have been deleted)
            result.delete()
            return get_result(item=item, preset=preset)
        return result
    except ts.models.Result.DoesNotExist:
        # Result does not exist
        # the corresponding task has to be created and run
        task, created = ts.models.Task.objects.get_or_create(experience=preset.get_single_experience(),
                                                   selection=item.get_single_selection())
        if created:
            task.run(wait=False)
        elif task.status == _RUNNING:
            return 'Task Running'
        else:
            # Result does not exist but task exist and is done, draft or pending
            task.status = _PENDING
            task.save()
        return 'Task Created and launched'

    
class ItemAnalysisResultSerializer(serializers.HyperlinkedModelSerializer):

    #analysis_url = serializers.HyperlinkedRelatedField(read_only=True,
    #                                                   
    #    )
    audio_duration = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()
    analysis_uuid = serializers.SerializerMethodField()

    class Meta:
        model = ts.models.Item
        fields = ('uuid', 'url', 'audio_duration', 'analysis_uuid', 'analysis_url', 'result')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'}
            }

    def get_url(self, obj):
        from rest_framework.reverse import reverse
        request = self.context['request']
        return reverse('item-detail', kwargs={'uuid': obj.uuid}, request=request)

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
            analysis, c = ts.models.Analysis.objects.get(uuid = analysis_uuid)
        except ts.models.Analysis.DoesNotExist:
            return {'Unknown analysis': analysis_uuid}

        preset = analysis.preset
 
        result = get_result(item=obj, preset=preset)
        if isinstance(result, ts.models.Result):
            res_msg = result.uuid
        else:
            res_msg = result
        return {'analysis': analysis.uuid,
                'item': item.uuid}

    
class SelectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Selection
        fields = ('uuid', 'items', 'selections', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'selections': {'lookup_field': 'uuid'},
            'items': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
            }


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Experience
        fields = ('uuid', 'presets', 'is_public', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'presets': {'lookup_field': 'uuid'},
            'author': {'lookup_field': 'username'}
            }

class ProcessorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Processor
        fields = ('url', 'pid', 'version')
        extra_kwargs = {
            'url': {'lookup_field': 'pid'}
            }


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
        model = ts.models.Result
        fields = ('uuid', 'item', 'preset', 'status', 'hdf5', 'file')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'preset':  {'lookup_field': 'uuid'}}


class Result_ReadableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Result
        fields = ('uuid', 'preset', 'hdf5', 'file', 'mime_type')
        read_only_fields = fields
        depth = 2


class ResultVisualizationSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that deals with subprocessor results
    """
    def to_representation(self, obj):
        subprocessor_id = self.context.get('request').query_params.get('id')

        start = float(self.context.get('request').query_params.get('start', 0))
        stop = float(self.context.get('request').query_params.get('stop', -1))
        width = int(self.context.get('request').query_params.get('width', 1024))
        height = int(self.context.get('request').query_params.get('height', 128))

        import h5py
        sub_result = h5py.File(obj.hdf5.path, 'r').get(subprocessor_id)

        duration = sub_result['audio_metadata'].attrs['duration']
        
        if start < 0:
            start = 0
        if start > duration:
            raise serializers.ValidationError("start must be less than duration")
        if stop == -1:
            stop = duration

        if stop > duration:
            stop = duration

        def display_dummy_image(start, stop, duration, width, height) :
            from matplotlib import pyplot as plt
            import numpy as np
            import StringIO
            import PIL
 
            t = np.linspace(start, stop, width)
            DPI = 96
            fig = plt.figure(figsize=(width/float(DPI), height/float(DPI)), dpi=DPI, frameon=False)
            #fig.set_tight_layout(True)
            #ax1 = plt.Axes(fig, [0., 0., 1., 1.])
            #ax1 = fig.add_subplot(111)
            ax1 = plt.axes([0,0,1,1])
            ax1.plot(t, t, 'b-', linewidth=2)
            ax1.axis([start, stop, 0, duration])
            ax1.set_axis_off()
                        
            buffer = StringIO.StringIO()
            canvas = plt.get_current_fig_manager().canvas
            canvas.draw()
            pil_image = PIL.Image.frombytes('RGB', canvas.get_width_height(), 
                                             canvas.tostring_rgb())
            pil_image.save(buffer, 'PNG')
            plt.close()
            # Django's HttpResponse reads the buffer and extracts the image
            return buffer.getvalue()

       

        return display_dummy_image(start, stop, duration, width, height)
    #{
    #        'id': subprocessor_id,
    #        'start': start,
    #        'stop': stop,
    #        'nb_pixels': nb_pixels
    #        }
    

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Task
        fields = ('url', 'uuid', 'experience', 'selection', 'status', 'author')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'experience': {'lookup_field': 'uuid'},
            'selection':  {'lookup_field': 'uuid'},
            'author' : {'lookup_field': 'username'}}


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.User
        fields = ('url', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
            }

class AnalysisSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ts.models.Analysis
        fields = ('url', 'uuid', 'title', 'preset', 'sub_processor')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'preset': {'lookup_field': 'uuid'},
            'sub_processor': {'lookup_field': 'sub_processor_id'}
            }
            

#class AnalysisTrackSerializer(serializers.HyperlinkedModelSerializer):
#
#    class Meta:
#        model = ts.models.AnalysisTrack
#        fields = ('url', 'uuid', 'analysis', 'item')

class AnalysisTrackSerializer(serializers.HyperlinkedModelSerializer):

    #result_uuid = serializers.SerializerMethodField()
    result_url = serializers.SerializerMethodField()
     
    class Meta:
        model = ts.models.AnalysisTrack
        fields = ('url', 'uuid', 'analysis', 'item', 'result_url')
        extra_kwargs = {
            'url': {'lookup_field': 'uuid'},
            'item': {'lookup_field': 'uuid'},
            'analysis': {'lookup_field': 'uuid'},
            }
        read_only_fields = ('uuid',)


    def create(self, validated_data):
        item = validated_data['item']
        analysis = validated_data['analysis']

        preset = analysis.preset

        result = get_result(item=item, preset=preset)
        
        #if isinstance(result, Result):
        #    res_msg = result.uuid
        #else:
        #    res_msg = result
        #return {'analysis': analysis.uuid,
        #        'item': item.uuid}
        
        return super(AnalysisTrackSerializer, self).create(validated_data)

    def get_result_uuid(self, obj):
        result =  get_result(item=obj.item, preset=obj.analysis.preset)
        if isinstance(result, ts.models.Result):
            self._result_uuid = result.uuid
            return result.uuid
        else:
            self._result_uuid = None
        return  self._result_uuid
    

    def get_result_url(self, obj):
        self.get_result_uuid(obj)
        if self._result_uuid is not None:
            url_kwargs = {'uuid': self._result_uuid}
            request = self.context['request']
            parameters = '?id=%s' % obj.analysis.sub_processor
            return reverse('timeside-result-visualization', kwargs=url_kwargs, request=request) + parameters 
        else:
            return 'Task running'
        
    ## def get_url(self, obj, view_name, request, format):
    ##     url_kwargs = {
    ##         'item_uuid': obj.item.uuid,
    ##         'analysis_uuid': obj.analysis.uuid.pk
    ##     }
    ##     return reverse(view_name, kwargs=url_kwargs, request=request, format=format)
