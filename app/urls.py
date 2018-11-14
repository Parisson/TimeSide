from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
import django.contrib.auth.urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/timeside/')),
    url(r'^timeside/', include('timeside.server.urls')),

    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Default login page
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'timeside/login.html'},
        name='timeside-login'),
    url(r'^accounts/logout/$', auth_views.logout, name='timeside-logout'),
    #url('^', include('django.contrib.auth.urls'))
]
