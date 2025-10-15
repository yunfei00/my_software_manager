from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    # path("", views.project_list, name="list"),
    # path("add/", views.project_add, name="add"),
    # path("edit/<int:pk>/", views.project_edit, name="edit"),
    # path("delete/<int:pk>/", views.project_delete, name="delete"),

    path('', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('detail/<int:pk>/', views.project_detail, name='project_detail'),
]
