# -*- coding: utf-8 -*-


from django.views.generic import *
from timeside.models import *


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
