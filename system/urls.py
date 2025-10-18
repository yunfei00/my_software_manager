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

    # 检测工具管理
    path('tool/', views.ToolListView.as_view(), name='tool_list'),
    path('tool/create/', views.ToolCreateView.as_view(), name='tool_create'),
    path('tool/<int:pk>/edit/', views.ToolUpdateView.as_view(), name='tool_edit'),
    path('tool/<int:pk>/delete/', views.ToolDeleteView.as_view(), name='tool_delete'),

    # 日志管理
    path('loginlog/', views.LoginLogListView.as_view(), name='loginlog_list'),
    path('operationlog/', views.OperationLogListView.as_view(), name='operationlog_list'),

    # 菜单管理
    path('menu/', views.MenuListView.as_view(), name='menu_list'),
    path('menu/create/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menu/<int:pk>/edit/', views.MenuUpdateView.as_view(), name='menu_edit'),
    path('menu/<int:pk>/delete/', views.MenuDeleteView.as_view(), name='menu_delete'),

    # 岗位管理
    path('post/', views.PostListView.as_view(), name='post_list'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # 审批流程配置
    path('workflow/', views.WorkflowListView.as_view(), name='workflow_list'),
    path('workflow/create/', views.WorkflowCreateView.as_view(), name='workflow_create'),
    path('workflow/<int:pk>/edit/', views.WorkflowUpdateView.as_view(), name='workflow_edit'),
    path('workflow/<int:pk>/delete/', views.WorkflowDeleteView.as_view(), name='workflow_delete'),

]
