from timeside.models import *
from rest_framework import serializers
import django.db.models
from django.contrib.auth.models import User


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ('id', 'items', 'selections', 'author')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'file', 'mime_type', 'author')


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ('id', 'presets', 'experiences', 'is_public', 'author')


class ProcessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Processor
        fields = ('id', 'pid', 'version')


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ('id', 'item', 'preset', 'status', 'hdf5', 'file')


class PresetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preset
        fields = ('id', 'processor', 'parameters', 'is_public')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'experience', 'selection', 'status', 'author')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


