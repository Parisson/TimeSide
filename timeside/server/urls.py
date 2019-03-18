# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
#from django.core.urlresolvers import reverse
from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from rest_framework.documentation import include_docs_urls

from timeside.server import views
from timeside.server.utils import TS_ENCODERS_EXT
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view

EXPORT_EXT = "|".join(TS_ENCODERS_EXT.keys())

admin.autodiscover()

schema_view = get_schema_view(title="TimeSide API")

api_router = routers.DefaultRouter()
api_router.register(r'selections', views.SelectionViewSet)
api_router.register(r'items', views.ItemViewSet)
api_router.register(r'experiences', views.ExperienceViewSet)
api_router.register(r'processors', views.ProcessorViewSet)
api_router.register(r'subprocessors', views.SubProcessorViewSet)
api_router.register(r'results', views.ResultViewSet)
api_router.register(r'presets', views.PresetViewSet)
api_router.register(r'tasks', views.TaskViewSet)
api_router.register(r'users', views.UserViewSet)
api_router.register(r'analysis', views.AnalysisViewSet)
api_router.register(r'analysis_tracks', views.AnalysisTrackViewSet,
                    base_name='analysistrack')
api_router.register(r'annotation_tracks', views.AnnotationTrackViewSet)
api_router.register(r'annotations', views.AnnotationViewSet)
api_router.register(r'providers', views.ProviderViewSet)
# api_router.register(r'provider_identifiers', views.ProviderIdentifierViewSet,
#                     base_name='provideridentifier')


urlpatterns = [
    # ----- API ---------
    url(r'^api/', include(api_router.urls)),
    # Docs
    url(r'^api/docs/', include_docs_urls(title='Timeside Web API')),
    # API endpoint for Generating Authentification token
    url(r'^api/token-auth/', authtoken_views.obtain_auth_token),
    # Temporary Endpoint to get CSRF Token
    url(r'^api/token-csrf/', views.Csrf_Token.as_view({'get': 'list'}), name='get_csrf_token'),
    # Items
    url(r'^api-token-auth/', obtain_auth_token, name='api_token_auth'),
    url('^api/schema/$', schema_view),
    url(r'^api/items/(?P<uuid>[0-9a-z-]+)/', include([
        url(r'^waveform/', views.ItemWaveView.as_view(), name="item-waveform"),
        # Get transcoded audio
        # Ex: /api/item/--<uuid>--/download/ogg
        url(r'^download/(?P<extension>' + EXPORT_EXT + ')$',
            views.ItemTranscode.as_view(), name="item-transcode-api"),
    ]),
    ),
    # ----- Timeside ------
    url(r'^$', views.ItemList.as_view(), name="timeside-item-list"),
    # Items
    # ex: /item/5/
    url(r'^items/(?P<uuid>[0-9a-z-]+)/', include([
        url(r'^$', views.ItemDetail.as_view(), name="timeside-item-detail"),

        url(r'^export/$', views.ItemDetailExport.as_view(),
            name='timeside-item-export'),
        url(r'^download/(?P<extension>' + EXPORT_EXT + ')$',
            views.ItemTranscode.as_view(), name="item-transcode"),
    ])
    ),
    # Results
    url(r'^api/results/(?P<uuid>[0-9a-z-]+)/visual/',
        views.ResultVisualizationViewSet.as_view(), name="timeside-result-visualization"),
    url(r'^results/(?P<uuid>[0-9a-z-]+)/json/$',
        views.ResultAnalyzerView.as_view(), name="timeside-result-json"),
    url(r'^results/(?P<pk>.*)/png/$',
        views.ResultGrapherView.as_view(), name="timeside-result-png"),
    url(r'^results/(?P<pk>.*)/audio/$',
        views.ResultEncoderView.as_view(), name="timeside-result-audio"),
    url(r'^results/(?P<pk>.*)/(?P<res_id>.*)/elan/$',
        views.ResultAnalyzerToElanView.as_view(), name="timeside-result-elan"),
    url(r'^results/(?P<pk>.*)/(?P<res_id>.*)/sonic/$',
        views.ResultAnalyzerToSVView.as_view(), name="timeside-result-sonic"),
    # Player
    url(r'^player/$', views.PlayerView.as_view(), name="timeside-player"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
