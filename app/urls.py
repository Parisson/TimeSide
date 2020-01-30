from django.conf.urls import include, url
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView
import django.contrib.auth.urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/timeside/')),
    url(r'^timeside/', include('timeside.server.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    # Default login page
    url(r'^accounts/login/$',
        LoginView.as_view(template_name='timeside/login.html'),
        name='timeside-login'
        ),
    url(r'^accounts/logout/$', LogoutView.as_view(),
        name='timeside-logout'
        ),
    #url('^', include('django.contrib.auth.urls'))
]
