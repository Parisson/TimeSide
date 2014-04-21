# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from timeside import views

admin.autodiscover()

api_router = routers.DefaultRouter()
api_router.register(r'items', views.ItemViewSet)
api_router.register(r'selections', views.SelectionViewSet)

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name="timeside-index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api_router.urls)),
)
