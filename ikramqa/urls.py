"""
URL configuration for certificate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static

from django.urls import path, include

from ikramqa import settings
from .api import api
from users.models import CityAutocomplete

urlpatterns = [
    path('portal/', admin.site.urls),
    path(
        'city-autocomplete/',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),
    path('accounts/', include("allauth.urls")),
    path("", include("frontend_settings.urls")),
    path("", include("users.urls")),
    path("cert/", include("certificate.urls")),
    path('summernote/', include('django_summernote.urls')),
    path("api/", api.urls),
]

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
