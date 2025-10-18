from django.db import models
from system.models import User

class BaseImage(models.Model):
    """基础镜像组件"""
    name = models.CharField(max_length=100, verbose_name="镜像名称")
    version = models.CharField(max_length=50, verbose_name="镜像版本号")
    image_id = models.CharField(max_length=100, unique=True, verbose_name="镜像ID")
    size = models.CharField(max_length=50, verbose_name="镜像大小")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户", null=True, blank=True)

    class Meta:
        verbose_name = "基础镜像组件"
        verbose_name_plural = "基础镜像组件"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}:{self.version}"


class BusinessImage(models.Model):
    """业务镜像"""
    name = models.CharField(max_length=100, verbose_name="镜像名称")
    version = models.CharField(max_length=50, verbose_name="镜像版本号")
    image_id = models.CharField(max_length=100, unique=True, verbose_name="镜像ID")
    size = models.CharField(max_length=50, verbose_name="镜像大小")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="所属用户", null=True, blank=True)

    class Meta:
        verbose_name = "业务镜像"
        verbose_name_plural = "业务镜像"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}:{self.version}"
