from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('detection-tools/', views.detection_tools_list, name='detection_tools_list'),
    path('detection-tools/add/', views.detection_tools_add, name='detection_tools_add'),
    path('pre-detection/', views.pre_detection_list, name='pre_detection_list'),
    path('pre-detection/add/', views.pre_detection_add, name='pre_detection_add'),
    path('pre-detection/download/<int:pk>/', views.pre_detection_download, name='pre_detection_download'),
]





