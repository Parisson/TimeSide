# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from timeside.views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="timeside-index"),

)
