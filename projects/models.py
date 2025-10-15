# projects/models.py
from django.db import models
from django.utils import timezone
import uuid


class BusinessDepartment(models.Model):
    name = models.CharField(max_length=100, verbose_name="业务部门")

    def __str__(self):
        return self.name


class BaseImage(models.Model):
    os = models.CharField(max_length=50, verbose_name="操作系统")
    middleware = models.CharField(max_length=100, verbose_name="中间件")
    jdk_version = models.CharField(max_length=50, verbose_name="JDK版本")

    def __str__(self):
        return f"{self.os} + {self.middleware} + {self.jdk_version}"


class Component(models.Model):
    name = models.CharField(max_length=100, verbose_name="组件名称")

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('in_progress', '进行中'),
        ('pause', '暂停'),
        ('completed', '已完成'),
        ('closed', '关闭'),
    ]

    name = models.CharField(max_length=200, verbose_name="项目名称")
    project_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="项目ID")
    business_department = models.ForeignKey(BusinessDepartment, on_delete=models.SET_NULL, null=True,
                                            verbose_name="业务部门")
    final_user = models.CharField(max_length=200, verbose_name="最终用户")
    description = models.TextField(blank=True, null=True, verbose_name="项目描述")
    expected_launch = models.DateField(default=timezone.now, verbose_name="预计上线时间")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="状态")
    base_image = models.ForeignKey(BaseImage, on_delete=models.SET_NULL, null=True, verbose_name="基础镜像版本")
    components = models.ManyToManyField(Component, blank=True, verbose_name="其他组件")

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目管理"

    def __str__(self):
        return f"{self.name} ({self.project_id})"

    # code = models.CharField(max_length=50, unique=True, verbose_name="项目编码")
    # start_date = models.DateField(null=True, blank=True, verbose_name="开始时间")
    # end_date = models.DateField(null=True, blank=True, verbose_name="结束时间")
    # create_time = models.DateTimeField(auto_now_add=True)
    # update_time = models.DateTimeField(auto_now=True)


