"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework import routers
from .view import PersonAPIViewSet, \
                  PTeacherViewSet, \
                  WDTeacherViewSet, \
                  WTHTeacherViewSet, \
                  GroupViewSet, \
                  FrameListAPIView
                  

router = routers.DefaultRouter()
router.register('people', PersonAPIViewSet)
router.register('wd', WDTeacherViewSet)
router.register('programming', PTeacherViewSet)
router.register('wth', WTHTeacherViewSet)
router.register('group', GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),\
    path('api/', include(router.urls)), 
    path('api/frame/<pk>', FrameListAPIView.as_view()),
]
