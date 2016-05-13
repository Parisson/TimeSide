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

    class Meta:
        model = Item
        fields = ('url', 'title', 'description', 'mime_type', 'source_file', 'source_url')


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
