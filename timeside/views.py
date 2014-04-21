# -*- coding: utf-8 -*-

import timeside
from timeside.models import *
from rest_framework import viewsets
from django.views.generic import *
from timeside.serializers import *


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


class ItemAnalyzerView(DetailView):
    
    model = Item

    def results(self):
        item = self.get_object()
        results = AnalyzerResult()
        return results.from_hdf5(self.hdf5).to_json()
    
    def get_context_data(self, **kwargs):
        context = super(ItemJsonAnalyzerView, self).get_context_data(**kwargs)
        return context
    


class ItemViewSet(viewsets.ModelViewSet):
    
    model = Item
    serializer_class = ItemSerializer


class SelectionViewSet(viewsets.ModelViewSet):
    
    model = Selection
    serializer_class = SelectionSerializer



