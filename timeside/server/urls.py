# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from timeside.server import views
from timeside.server.utils import TS_ENCODERS_EXT

EXPORT_EXT = "|".join(TS_ENCODERS_EXT.keys())

admin.autodiscover()

api_router = routers.DefaultRouter()
api_router.register(r'selections', views.SelectionViewSet)
api_router.register(r'items', views.ItemViewSet)
api_router.register(r'experiences', views.ExperienceViewSet)
api_router.register(r'processors', views.ProcessorViewSet)
api_router.register(r'results', views.ResultViewSet)
api_router.register(r'presets', views.PresetViewSet)
api_router.register(r'tasks', views.TaskViewSet)
api_router.register(r'users', views.UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_router.urls)),
    url(r'^$', views.IndexView.as_view(), name="timeside-index"),
    # Items
    # ex: /item/5/
    url(r'^items/(?P<pk>\d+)/$', views.ItemDetail.as_view(),
        name='timeside-item-detail'),
    # Get transcoded audio
    # Ex: /item/5/download/ogg
    url(r'^items/(?P<pk>\d+)/download/(?P<extension>' + EXPORT_EXT + ')$',
        views.ItemExport.as_view(), name="item-export"),
    # Results
    url(r'^results/(?P<pk>.*)/json/$', views.ResultAnalyzerView.as_view(),
        name="timeside-result-json"),
    url(r'^results/(?P<pk>.*)/png/$', views.ResultGrapherView.as_view(),
        name="timeside-result-png"),
    url(r'^results/(?P<pk>.*)/audio/$', views.ResultEncoderView.as_view(),
        name="timeside-result-audio"),
    )
