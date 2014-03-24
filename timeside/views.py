# -*- coding: utf-8 -*-

import timeside

from django.views.generic import *
from timeside.models import *


decoders = timeside.core.processors(timeside.api.IDecoder)
analyzers = timeside.core.processors(timeside.api.IAnalyzer)
graphers = timeside.core.processors(timeside.api.IGrapher)
encoders = timeside.core.processors(timeside.api.IEncoder)
value_analyzers = timeside.core.processors(timeside.api.IValueAnalyzer)


class IndexView(ListView):

    model = Item
    template_name='timeside/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    #@method_decorator(permission_required('is_superuser'))
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ItemGrapherView(DetailView):

	model = Item

