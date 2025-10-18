from django.urls import path
from . import views

app_name = 'images'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('base/', views.base_image_list, name='base_image_list'),
    path('business/', views.business_image_list, name='business_image_list'),
    path('base/add/', views.add_base_image, name='add_base_image'),
    path('business/add/', views.add_business_image, name='add_business_image'),
]
