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

from .models import Department, User, Role, DictItem
from .forms import DeptForm, UserForm, RoleForm, DictForm
from .filters import DepartmentFilter, UserFilter, RoleFilter, DictFilter
from .utils import export_queryset_to_excel

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
        if 'export' in request.GET:
            cols = [('id','ID'), ('name','用户名称'), ('phone','手机号'), ('dept','部门'), ('roles','角色'), ('status','状态')]
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
    print(f'request.user is {request.user}')

    # 查询角色
    user = request.user
    user_role = None
    if request.user.is_authenticated:
        user = User.objects.get(username=user)
        user_role = user.roles.first()  # 返回 Role 对象 或 None

    print(f'user_role is {user_role}')
    return render(request, "system/accounts/dashboard.html", {"user_role": user_role})
