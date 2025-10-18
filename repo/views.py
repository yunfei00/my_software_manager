from django.shortcuts import render, redirect, get_object_or_404
from .models import Repository, RepositoryImage, Image
from .forms import RepositoryForm
from django.http import FileResponse
import os
# Create your views here.

def project_list(request):
    return render(request, 'images/home.html')

# 仓库列表
def repository_list(request):
    repos = Repository.objects.filter(owner=request.user)
    return render(request, 'repository_list.html', {'repos': repos})

# 新建仓库
def repository_add(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST, user=request.user)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.owner = request.user
            repo.save()
            form.save_m2m()
            return redirect('repository_list')
    else:
        form = RepositoryForm(user=request.user)
    return render(request, 'repository_add.html', {'form': form})

# 打包镜像
def repository_package(request, pk):
    repo = get_object_or_404(Repository, pk=pk, owner=request.user)
    # TODO: 实现打包逻辑，这里假设生成 tar 文件
    package_path = f"/tmp/{repo.name}.tar"
    with open(package_path, 'wb') as f:
        f.write(b'fake docker image package content')  # 占位
    repo.package_file_path = package_path  # 可在 Repository 模型中加 filefield 保存
    repo.save()
    return redirect('repository_list')

# 下载镜像包
def repository_download(request, pk):
    repo = get_object_or_404(Repository, pk=pk, owner=request.user)
    package_path = getattr(repo, 'package_file_path', None)
    if package_path and os.path.exists(package_path):
        return FileResponse(open(package_path, 'rb'), as_attachment=True, filename=os.path.basename(package_path))
    return redirect('repository_list')


