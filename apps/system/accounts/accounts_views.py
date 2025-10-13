from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm
from ..models import UserApplication, User

def register_view(request):
    """注册用户（生成申请）"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册申请已提交，请等待管理员审核。')
            return redirect('system:login')
    else:
        form = UserRegisterForm()
    return render(request, 'system/accounts/register.html', {'form': form})


def is_admin(user):
    return hasattr(user, 'roles') and user.roles.filter(name='管理员').exists()


@login_required
@user_passes_test(is_admin)
def application_list(request):
    """管理员审批页面"""
    apps = UserApplication.objects.all().order_by('-create_time')
    return render(request, 'system/accounts/application_list.html', {'apps': apps})


@login_required
@user_passes_test(is_admin)
def approve_application(request, app_id):
    app = get_object_or_404(UserApplication, id=app_id)
    if app.status == 'pending':
        user = User.objects.create(
            name=app.name,
            phone=app.phone,
            dept=app.dept,
            status=1  # 启用
        )
        user.roles.set(app.roles.all())
        user.save()
        app.status = 'approved'
        app.save()
        messages.success(request, f'用户 {user.name} 审核通过并已创建。')
    return redirect('application_list')


@login_required
@user_passes_test(is_admin)
def reject_application(request, app_id):
    app = get_object_or_404(UserApplication, id=app_id)
    if app.status == 'pending':
        app.status = 'rejected'
        app.save()
        app.delete()
        messages.warning(request, f'用户 {app.name} 申请已拒绝并删除。')
    return redirect('application_list')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.error(request, '您的账号尚未通过管理员审核。')
                return redirect('login')
            login(request, user)
            return redirect('system:dept_list')
    else:
        form = AuthenticationForm()
    return render(request, 'system/accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')
