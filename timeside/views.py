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
        return context

    #@method_decorator(permission_required('is_superuser'))
    #@method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ItemGrapherView(DetailView):

	model = Item
	mime_type = 'image/png'
	

class ItemJsonAnalyzerView(DetailView):

	model = Item

    def results(self):
    	item = self.get_object()
    	experience = Experience.objects.get(id=experience_id)
        results = AnalyzerResult()
        return results.from_hdf5(self.hdf5).to_json()
        
    def get_context_data(self, **kwargs):
        context = super(ItemJsonAnalyzerView, self).get_context_data(**kwargs)
        item = self.get_object()
        context['experiences'] = item.experiences.all().filter(author=self.request.user)
        return context

    def render_to_response(self, context):
        mimetype = mimetypes.guess_type(document.file.path)[0]
        extension = mimetypes.guess_extension(mimetype)
        response = HttpResponse(results, mimetype=mimetype)
        response['Content-Disposition'] = "attachment; filename=%s%s" % \
                                             (document.title.encode('utf8'), extension)
        return response

    @jsonrpc_method('timeside.stop_conference'):
    def stop(request, public_id):
