# -*- coding: utf-8 -*-

from django.views.generic import *
from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import viewsets

import timeside
from timeside.models import *
from timeside.serializers import *


class SelectionViewSet(viewsets.ModelViewSet):
    
    model = Selection
    serializer_class = SelectionSerializer


class ItemViewSet(viewsets.ModelViewSet):
    
    model = Item
    serializer_class = ItemSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    
    model = Experience
    serializer_class = ExperienceSerializer


class ProcessorViewSet(viewsets.ModelViewSet):
    
    model = Processor
    serializer_class = ProcessorSerializer


class ResultViewSet(viewsets.ModelViewSet):
    
    model = Result
    serializer_class = ResultSerializer


class PresetViewSet(viewsets.ModelViewSet):
    
    model = Preset
    serializer_class = PresetSerializer


class TaskViewSet(viewsets.ModelViewSet):
    
    model = Task
    serializer_class = TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    
    model = User
    serializer_class = UserSerializer



def stream_from_file(__file):
    chunk_size = 0x10000
    f = open(__file, 'r')
    while True:
        __chunk = f.read(chunk_size)
        if not len(__chunk):
            f.close()
            break
        yield __chunk


class IndexView(ListView):

    model = Item
    template_name='timeside/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ResultAnalyzerView(View):
    
    model = Result

    def get(self, request, *args, **kwargs):
        result = Result.objects.get(pk=kwargs['pk'])
        container = AnalyzerResultContainer()
        return HttpResponse(container.from_hdf5(result.hdf5.path).to_json(), mimetype='application/json')
    