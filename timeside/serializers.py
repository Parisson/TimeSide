from timeside.models import *
from rest_framework import serializers
import django.db.models
from django.contrib.auth.models import User


class SelectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Selection
        fields = ('id', 'items', 'author')


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'title', 'file', 'mime_type', 'author')


class ExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = ('id', 'processors', 'is_preset', 'author')


class ProcessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Processor
        fields = ('id', 'pid', 'version')


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = ('id', 'item', 'processor', 'status')


class ParametersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameters
        fields = ('id', 'processor', 'parameters', 'is_preset')


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('id', 'experience', 'selection', 'status', 'author')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


