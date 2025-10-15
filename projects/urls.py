from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path("", views.project_list, name="list"),
    path("add/", views.project_add, name="add"),
    path("edit/<int:pk>/", views.project_edit, name="edit"),
    path("delete/<int:pk>/", views.project_delete, name="delete"),
]
