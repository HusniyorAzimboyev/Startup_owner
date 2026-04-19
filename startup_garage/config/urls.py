"""
URL configuration for startup_garage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from . import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app import views
    2. Add a URL to urlpatterns:  path('', views.Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect


def home_view(request):
    """Redirect root to dashboard or login"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    return redirect('accounts:login')


urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('tasks/', include('apps.tasks.urls')),
    path('mentor/', include('apps.mentor.urls')),
    path('investor/', include('apps.investor.urls')),
    path('progress/', include('apps.progress.urls')),
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
