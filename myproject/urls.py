"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse, FileResponse, Http404
import os

def serve_media(request, file_path):
    """Serve media files in production."""
    if not settings.DEBUG:
        # In production, try to serve from staticfiles (where collectstatic puts media files)
        full_path = os.path.join(settings.STATIC_ROOT, 'media', file_path)
        if os.path.exists(full_path):
            return FileResponse(open(full_path, 'rb'))
    
    # Fallback to media root
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(full_path):
        return FileResponse(open(full_path, 'rb'))
    
    raise Http404("Media file not found")

# Import the admin creation view
from create_admin_view import create_admin_now
from test_email_view import test_email_now
from debug_email import debug_email_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('setup-admin/', create_admin_now, name='create_admin_now'),
    path('test-email/', test_email_now, name='test_email_now'),
    path('debug-email/', debug_email_view, name='debug_email'),
]

# Serve media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path('media/<path:file_path>', serve_media, name='serve_media'),
    ]
