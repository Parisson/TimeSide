# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2014 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of TimeSide.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

from timeside.server.models import *
from rest_framework import serializers
import django.db.models
from django.contrib.auth.models import User


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        # fields = ('id', 'items', 'selections', 'author')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        # fields = ('id', 'title', 'file', 'mime_type', 'author')


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        # fields = ('id', 'presets', 'experiences', 'is_public', 'author')


class ProcessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Processor
        # fields = ('id', 'pid', 'version')


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        # fields = ('id', 'item', 'preset', 'status', 'hdf5', 'file')


class PresetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preset
        # fields = ('id', 'processor', 'parameters', 'is_public')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        # fields = ('id', 'experience', 'selection', 'status', 'author')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


