from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BaseImage, BusinessImage

def project_list(request):
    return render(request, 'images/home.html')
@login_required
def base_image_list(request):
    """基础镜像组件列表"""
    # images = BaseImage.objects.filter(owner__in=[request.user.id, None])
    images = BaseImage.objects.filter()
    print('bse images is {}'.format(images))
    return render(request, 'images/base_image_list.html', {'images': images})


@login_required
def business_image_list(request):
    """业务镜像列表"""
    print('add business image ok here')
    images = BusinessImage.objects.filter()
    return render(request, 'images/business_image_list.html', {'images': images})


@login_required
def add_base_image(request):
    """管理员添加基础镜像"""
    # if not request.user.is_superuser:
    #     messages.error(request, "只有管理员可以添加基础镜像。")
    #     return redirect('images:base_image_list')
    print('add base image ok here, ')
    if request.method == 'POST':
        name = request.POST.get('name')
        version = request.POST.get('version')
        image_id = request.POST.get('image_id')
        size = request.POST.get('size')

        print(f'data is {request.POST}')

        BaseImage.objects.create(
            name=name,
            version=version,
            image_id=image_id,
            size=size,
            owner=None  # 平台镜像无归属
        )
        messages.success(request, "基础镜像添加成功！")
        return redirect('images:base_image_list')

    return render(request, 'images/add_base_image.html')


@login_required
def add_business_image(request):
    """用户添加业务镜像"""
    if request.method == 'POST':
        name = request.POST.get('name')
        version = request.POST.get('version')
        image_id = request.POST.get('image_id')
        size = request.POST.get('size')

        BusinessImage.objects.create(
            name=name,
            version=version,
            image_id=image_id,
            size=size,
            owner=request.user
        )
        messages.success(request, "业务镜像添加成功！")
        return redirect('images:business_image_list')

    return render(request, 'images/add_business_image.html')
