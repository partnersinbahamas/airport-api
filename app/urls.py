from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from debug_toolbar.toolbar import debug_toolbar_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

BASE_URL = settings.BASE_API_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{BASE_URL}/user/', include('user.urls',  namespace='user')),

    path(f'{BASE_URL}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{BASE_URL}/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
