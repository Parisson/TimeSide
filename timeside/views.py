# -*- coding: utf-8 -*-

import timeside

from django.views.generic import *
from timeside.models import *


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
        item = self.get_object()
        context['experiences'] = item.experiences.all().filter(author=self.request.user)
        return context

    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ItemGrapherView(DetailView):

    model = Item
    mime_type = 'image/png'


class ItemAnalyzerView(DetailView):
    
    model = Item

    def results(self):
        item = self.get_object()
        results = AnalyzerResult()
        return results.from_hdf5(self.hdf5).to_json()
    
    def get_context_data(self, **kwargs):
        context = super(ItemJsonAnalyzerView, self).get_context_data(**kwargs)
        return context
    
    