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
from rest_framework_nested import routers
from .view import PersonAPIViewSet, \
                  DeviceViewSet, \
                  GroupViewSet, \
                  MouseDragViewSet, \
                  ReadOnlyFrameAPIViewSet, \
                  InferenceModelViewSet, \
                  TeacherViewSet
                  
router = routers.DefaultRouter()
router.register('frames', ReadOnlyFrameAPIViewSet)
router.register('people', PersonAPIViewSet)
router.register('devices', DeviceViewSet)
router.register('groups', GroupViewSet)
router.register("models", InferenceModelViewSet)

groups_router = routers.NestedDefaultRouter(router, "groups", lookup="group")
groups_router.register("drags", MouseDragViewSet)
models_router = routers.NestedDefaultRouter(router, "models", lookup="model")
models_router.register("teachers", TeacherViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),\
    path('api/', include(router.urls)),
    path('api/', include(groups_router.urls)),
    path("api/", include(models_router.urls))
]
