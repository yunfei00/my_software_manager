from django.urls import path
from . import views

app_name = 'repo'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('repositories/', views.repository_list, name='repository_list'),
    path('repositories/add/', views.repository_add, name='repository_add'),
    path('repositories/package/<int:pk>/', views.repository_package, name='repository_package'),
    path('repositories/download/<int:pk>/', views.repository_download, name='repository_download'),
]

