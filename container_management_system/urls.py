"""
URL configuration for container_management_system projects.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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


from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from system.views import DepartmentViewSet, RoleViewSet, UserViewSet
# from registry.views import ImageViewSet
# from scanner.views import ScanToolViewSet, PreScanViewSet
# from apps.repository.views import RepoViewSet

router = routers.DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('roles', RoleViewSet)
router.register('users', UserViewSet)
# router.register('images', ImageViewSet)
# router.register('scan-tools', ScanToolViewSet)
# router.register('pre-scans', PreScanViewSet)
# router.register('repos', RepoViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('system.urls', namespace='system')),
    path("images/", include("images.urls")),
    path("projects/", include("projects.urls")),
    path("detection/", include("detection.urls")),
    path("repo/", include("repo.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/', include(router.urls)),
]