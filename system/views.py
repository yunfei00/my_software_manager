from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets

from .models import Department, User, Role, DictItem
from .forms import DeptForm, UserForm, RoleForm, DictForm, Tool, LoginLog, OperationLog, Menu, Post, WorkflowConfig
from .filters import DepartmentFilter, UserFilter, RoleFilter, DictFilter
from .utils import export_queryset_to_excel
from .forms import ToolForm, MenuForm, PostForm, WorkflowConfigForm

from .serializers import DepartmentSerializer, RoleSerializer, UserSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('-create_time')
    serializer_class = DepartmentSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ---------- Generic helpers to handle modal form (AJAX) ----------
def render_modal_form(request, form, template='system/includes/modal_form.html', context_extra=None):
    context = {'form': form}
    if context_extra:
        context.update(context_extra)
    html = render_to_string(template, context, request=request)
    return JsonResponse({'html': html})

# ---------- Department ----------
class DeptListView(View):
    def get(self, request):
        f = DepartmentFilter(request.GET, queryset=Department.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        page = request.GET.get('page')
        objs = paginator.get_page(page)
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','部门名称'), ('parent','上级部门'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'departments')
        return render(request, 'system/dept_list.html', {'filter': f, 'page_obj': objs})

class DeptCreateView(View):
    def get(self, request):
        form = DeptForm()
        return render_modal_form(request, form)

    def post(self, request):
        form = DeptForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class DeptUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Department, pk=pk)
        form = DeptForm(instance=obj)
        return render_modal_form(request, form, context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Department, pk=pk)
        form = DeptForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class DeptDeleteView(DeleteView):
    model = Department
    success_url = reverse_lazy('system:dept_list')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

# ---------- Role ----------
class RoleListView(View):
    def get(self, request):
        f = RoleFilter(request.GET, queryset=Role.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','角色名称'), ('code','权限标识'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'roles')
        return render(request, 'system/role_list.html', {'filter': f, 'page_obj': objs})

class RoleCreateView(View):
    def get(self, request):
        return render_modal_form(request, RoleForm())

    def post(self, request):
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class RoleUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Role, pk=pk)
        return render_modal_form(request, RoleForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Role, pk=pk)
        form = RoleForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class RoleDeleteView(DeleteView):
    model = Role
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

# ---------- User ----------
class UserListView(View):
    def get(self, request):
        # if request.user.roles.name != "超级管理员":
        #     print('无权访问用户列表')
        #     return HttpResponseForbidden("你没有权限访问此页面")
        f = UserFilter(request.GET, queryset=User.objects.select_related('dept').prefetch_related('roles').all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        # ✅ 打印所有用户信息（分页后的）
        print("=== 用户列表调试输出 ===")
        for u in objs:
            role_names = ", ".join([r.name for r in u.roles.all()]) or "无角色"
            dept_name = u.dept.name if u.dept else "无部门"
            status_display = u.get_status_display() if hasattr(u, 'get_status_display') else u.status
            print(f"ID: {u.id} | 用户名: {u.username} | 姓名: {u.name} | 公司: {u.company or '无'} | "
                  f"部门: {dept_name} | 角色: {role_names} | 状态: {status_display}")
        print("=======================")

        if 'export' in request.GET:
            cols = [('id','ID'), ('name','用户名称'), ('phone','手机号'), ('company','公司'),('dept','部门'), ('roles','角色'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'users')

        return render(request, 'system/user_list.html', {'filter': f, 'page_obj': objs})

class UserCreateView(View):
    def get(self, request):
        return render_modal_form(request, UserForm())

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # form.save_m2m()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class UserUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        return render_modal_form(request, UserForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            # form.save_m2m()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class UserDeleteView(DeleteView):
    model = User
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

# ---------- Dict (支持批量删除) ----------
class DictListView(View):
    def get(self, request):
        f = DictFilter(request.GET, queryset=DictItem.objects.all())
        qs = f.qs.order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id','ID'), ('type','字典类型'), ('name','字典名称'), ('value','字典值'), ('status','状态')]
            return export_queryset_to_excel(f.qs, cols, 'dicts')
        return render(request, 'system/dict_list.html', {'filter': f, 'page_obj': objs})

class DictCreateView(View):
    def get(self, request):
        return render_modal_form(request, DictForm())

    def post(self, request):
        form = DictForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class DictUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(DictItem, pk=pk)
        return render_modal_form(request, DictForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(DictItem, pk=pk)
        form = DictForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class DictDeleteView(DeleteView):
    model = DictItem
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})

@method_decorator(csrf_exempt, name='dispatch')
class DictBulkDeleteView(View):
    def post(self, request):
        ids = request.POST.get('ids')
        if not ids:
            return HttpResponseBadRequest("没有选择任何项")
        id_list = ids.split(',')
        DictItem.objects.filter(id__in=id_list).delete()
        return JsonResponse({'success': True})

@login_required
def dashboard(request):
    # 后续注入统计数据、快捷入口等

    # 查询角色
    user = request.user
    user_role = None
    if request.user.is_authenticated:
        user = User.objects.get(username=user)
        user_role = user.roles.first()  # 返回 Role 对象 或 None
        user_role = str(user_role)

    is_admin = user_role == '超级管理员'
    return render(request, "system/accounts/dashboard.html",
                  {"user_role": user_role, 'is_admin': is_admin})


# ---------- 检测工具管理 ----------
class ToolListView(View):
    def get(self, request):
        qs = Tool.objects.all().order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id', 'ID'), ('name', '工具名称'), ('api_url', '接口地址'), ('description', '说明'), ('status', '状态')]
            return export_queryset_to_excel(qs, cols, 'tools')
        return render(request, 'system/tool_list.html', {'page_obj': objs})

class ToolCreateView(View):
    def get(self, request):
        return render_modal_form(request, ToolForm())

    def post(self, request):
        form = ToolForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class ToolUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Tool, pk=pk)
        return render_modal_form(request, ToolForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Tool, pk=pk)
        form = ToolForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class ToolDeleteView(DeleteView):
    model = Tool
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


# ---------- 登录日志 ----------
class LoginLogListView(View):
    def get(self, request):
        qs = LoginLog.objects.all().order_by('-time')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('username', '用户名'), ('ip', 'IP'), ('status', '状态'), ('time', '时间')]
            return export_queryset_to_excel(qs, cols, 'login_logs')
        return render(request, 'system/loginlog_list.html', {'page_obj': objs})


# ---------- 操作日志 ----------
class OperationLogListView(View):
    def get(self, request):
        qs = OperationLog.objects.all().order_by('-time')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('module', '系统模块'), ('operator', '操作人员'), ('ip', 'IP'), ('action', '操作内容'), ('time', '时间')]
            return export_queryset_to_excel(qs, cols, 'operation_logs')
        return render(request, 'system/operationlog_list.html', {'page_obj': objs})


# ---------- 菜单管理 ----------
class MenuListView(View):
    def get(self, request):
        qs = Menu.objects.all().order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id', 'ID'), ('name', '菜单名称'), ('path', '路径'), ('parent', '上级菜单'), ('status', '状态')]
            return export_queryset_to_excel(qs, cols, 'menus')
        return render(request, 'system/menu_list.html', {'page_obj': objs})

class MenuCreateView(View):
    def get(self, request):
        return render_modal_form(request, MenuForm())

    def post(self, request):
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class MenuUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        return render_modal_form(request, MenuForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Menu, pk=pk)
        form = MenuForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class MenuDeleteView(DeleteView):
    model = Menu
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


# ---------- 岗位管理 ----------
class PostListView(View):
    def get(self, request):
        qs = Post.objects.all().order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id', 'ID'), ('name', '岗位名称'), ('code', '岗位编码'), ('status', '状态')]
            return export_queryset_to_excel(qs, cols, 'posts')
        return render(request, 'system/post_list.html', {'page_obj': objs})

class PostCreateView(View):
    def get(self, request):
        return render_modal_form(request, PostForm())

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class PostUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(Post, pk=pk)
        return render_modal_form(request, PostForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class PostDeleteView(DeleteView):
    model = Post
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})


# ---------- 审批流程配置 ----------
class WorkflowListView(View):
    def get(self, request):
        qs = WorkflowConfig.objects.all().order_by('-id')
        paginator = Paginator(qs, 10)
        objs = paginator.get_page(request.GET.get('page'))
        if 'export' in request.GET:
            cols = [('id', 'ID'), ('name', '流程名称'), ('steps', '流程步骤'), ('status', '状态')]
            return export_queryset_to_excel(qs, cols, 'workflows')
        return render(request, 'system/workflow_list.html', {'page_obj': objs})

class WorkflowCreateView(View):
    def get(self, request):
        return render_modal_form(request, WorkflowConfigForm())

    def post(self, request):
        form = WorkflowConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form)

class WorkflowUpdateView(View):
    def get(self, request, pk):
        obj = get_object_or_404(WorkflowConfig, pk=pk)
        return render_modal_form(request, WorkflowConfigForm(instance=obj), context_extra={'obj': obj})

    def post(self, request, pk):
        obj = get_object_or_404(WorkflowConfig, pk=pk)
        form = WorkflowConfigForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return render_modal_form(request, form, context_extra={'obj': obj})

class WorkflowDeleteView(DeleteView):
    model = WorkflowConfig
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
