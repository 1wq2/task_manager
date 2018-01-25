"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from tasks.views import TaskViewSet, UserViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'notes', TaskViewSet, 'Note')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^tasks/', include('tasks.urls')),
    url(r'^', include('tasks.urls_visitor')),

    url(r'^api/', include(router.urls)), #rest api
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]
# urlpatterns = format_suffix_patterns(urlpatterns)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


