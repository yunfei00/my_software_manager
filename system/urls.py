from django.urls import path
from . import views
from .accounts import accounts_views

app_name = 'system'

urlpatterns = [
    # dept
    path('dept/', views.DeptListView.as_view(), name='dept_list'),
    path('dept/create/', views.DeptCreateView.as_view(), name='dept_create'),
    path('dept/<int:pk>/edit/', views.DeptUpdateView.as_view(), name='dept_edit'),
    path('dept/<int:pk>/delete/', views.DeptDeleteView.as_view(), name='dept_delete'),

    # role
    path('role/', views.RoleListView.as_view(), name='role_list'),
    path('role/create/', views.RoleCreateView.as_view(), name='role_create'),
    path('role/<int:pk>/edit/', views.RoleUpdateView.as_view(), name='role_edit'),
    path('role/<int:pk>/delete/', views.RoleDeleteView.as_view(), name='role_delete'),

    # user
    path('user/', views.UserListView.as_view(), name='user_list'),
    path('user/create/', views.UserCreateView.as_view(), name='user_create'),
    path('user/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('user/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # dict
    path('dict/', views.DictListView.as_view(), name='dict_list'),
    path('dict/create/', views.DictCreateView.as_view(), name='dict_create'),
    path('dict/<int:pk>/edit/', views.DictUpdateView.as_view(), name='dict_edit'),

    path('dict/<int:pk>/delete/', views.DictDeleteView.as_view(), name='dict_delete'),
    # path('dict/bulk-delete/', views.DictBulkDeleteView.as_view(), name='dict_bulk_delete'),

    path('register/', accounts_views.register_view, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('applications/', accounts_views.application_list, name='application_list'),
    path('applications/approve/<int:app_id>/', accounts_views.approve_application, name='approve_application'),
    path('applications/reject/<int:app_id>/', accounts_views.reject_application, name='reject_application'),
    path("", views.dashboard, name="dashboard"),
]
