# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
#from django.core.urlresolvers import reverse

from timeside.server import views
from timeside.server.utils import TS_ENCODERS_EXT

from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from rest_framework.schemas.openapi import SchemaGenerator
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

EXPORT_EXT = "|".join(TS_ENCODERS_EXT.keys())

admin.autodiscover()

class SchemaWithServerInfoGeneraror(SchemaGenerator):
     def get_schema(self, request=None, public=False):
        # Adding production and staging server urls ton title and version infos
        schema = super().get_schema()
        schema['servers'] = [
                {
                    "url": "https://wasabi.telemeta.org/",
                    "description": "Production server"
                },
                {
                    "url": "https://sandbox.wasabi.telemeta.org/",
                    "description": "Staging server"
                }
        ]
        return schema

schema_view = get_schema_view(
    title="TimeSide API",
    description="RESTful API of TimeSide, a scalable audio processing framework",
    version="1.0.0",
    # url="https://wasabi.telemeta.org/",
    generator_class=SchemaWithServerInfoGeneraror,
    )

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
                    basename='analysistrack')
api_router.register(r'annotation_tracks', views.AnnotationTrackViewSet)
api_router.register(r'annotations', views.AnnotationViewSet)
api_router.register(r'providers', views.ProviderViewSet)


urlpatterns = [
    # docs
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='timeside/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    # Route TemplateView to serve the ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('redoc/', TemplateView.as_view(
        template_name='timeside/redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
    # ----- API ---------
    url(r'^api/', include(api_router.urls)),
    # API endpoint for Generating Simple Web Token
    url(r'^api-token-auth/', obtain_auth_token, name='api_token_auth'),
    # API endpoints for Generating access and refresh JSON Web Token (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Verify JWT without having access to signing key
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Temporary Endpoint to get CSRF Token
    url(r'^api/token-csrf/', views.Csrf_Token.as_view({'get': 'list'}), name='get_csrf_token'),
    # Items
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
    url(r'^results/(?P<uuid>.*)/png/$',
        views.ResultGrapherView.as_view(), name="timeside-result-png"),
    url(r'^results/(?P<uuid>.*)/audio/$',
        views.ResultEncoderView.as_view(), name="timeside-result-audio"),
    url(r'^results/(?P<uuid>.*)/(?P<res_id>.*)/elan/$',
        views.ResultAnalyzerToElanView.as_view(), name="timeside-result-elan"),
    url(r'^results/(?P<uuid>.*)/(?P<res_id>.*)/sonic/$',
        views.ResultAnalyzerToSVView.as_view(), name="timeside-result-sonic"),
    # Player
    url(r'^player/$', views.PlayerView.as_view(), name="timeside-player"),
    # Schema
    url(r'^api/schema/$', schema_view, name="openapi-schema"),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
