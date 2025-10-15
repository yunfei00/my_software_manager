# projects/views.py
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
#
# @login_required
# def project_list(request):
#     keyword = request.GET.get("keyword", "")
#     projects = Project.objects.all()
#     if keyword:
#         projects = projects.filter(name__icontains=keyword)
#     return render(request, "projects/list.html", {"projects": projects, "keyword": keyword})
#
# @login_required
# def project_add(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         code = request.POST.get("code")
#         description = request.POST.get("description")
#         Project.objects.create(name=name, code=code, description=description, owner=request.user)
#         return redirect("projects:list")
#     return render(request, "projects/add.html")
#
#
# def create_project(request):
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('project_list')
#     else:
#         form = ProjectForm()
#     return render(request, 'projects/project_form.html', {'form': form})
#
# @login_required
# def project_edit(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#
#     if request.method == "POST":
#         # 获取用户修改后的表单值
#         project.name = request.POST.get("name")
#         project.description = request.POST.get("description")
#         project.status = request.POST.get("status")
#         project.save()
#
#         messages.success(request, "项目信息已更新！")
#         return redirect("project:list")
#
#     # ⚠️ GET 请求 — 返回模板并传入原始项目对象
#     return render(request, "projects/edit.html", {"project": project})
# @login_required
# def project_delete(request, pk):
#     project = get_object_or_404(Project, pk=pk)
#     if request.method == "POST":
#         project.delete()
#         return redirect("projects:list")
#     return render(request, "projects/delete.html", {"projects": project})


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form, 'title': '创建项目'})

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form, 'title': '编辑项目'})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


