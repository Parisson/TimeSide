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


class ItemGraphView(DetailView):



    def item_visualize(self, request, public_id, grapher_id, width, height):
        item = MediaItem.objects.get(public_id=public_id)
        mime_type = 'image/png'
        grapher = self.get_grapher(grapher_id)
        
        if grapher.id() != grapher_id:
            raise Http404

        size = width + '_' + height
        image_file = '.'.join([public_id, grapher_id, size, 'png'])

        # FIX waveform grapher name change
        old_image_file = '.'.join([public_id, 'waveform', size, 'png'])
        if 'waveform_centroid' in grapher_id and self.cache_data.exists(old_image_file):
            image_file = old_image_file

        if not self.cache_data.exists(image_file):
            source = item.get_source()
            if source:
                path = self.cache_data.dir + os.sep + image_file
                decoder  = timeside.decoder.FileDecoder(source)
                graph = grapher(width = int(width), height = int(height))
                (decoder | graph).run()
                graph.watermark('timeside', opacity=.6, margin=(5,5))
                f = open(path, 'w')
                graph.render(output=path)
                f.close()

        response = HttpResponse(self.cache_data.read_stream_bin(image_file), mimetype=mime_type)
        return response