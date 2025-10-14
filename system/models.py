from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseModel(models.Model):
    STATUS_CHOICES = [
        (1, "启用"),
        (0, "停用"),
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True

class Department(BaseModel):
    name = models.CharField(max_length=64, verbose_name="部门名称")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级部门")

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Role(BaseModel):
    name = models.CharField(max_length=100, verbose_name="角色名称")
    code = models.CharField(max_length=50, verbose_name="权限标识", unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser, BaseModel):
    name = models.CharField(max_length=100, verbose_name="用户名称")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属部门")
    roles = models.ManyToManyField(Role, blank=True, verbose_name="角色")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户管理"

    def __str__(self):
        return self.name


class DictItem(BaseModel):
    name = models.CharField(max_length=100, verbose_name="字典名称")
    type = models.CharField(max_length=50, verbose_name="字典类型")
    value = models.CharField(max_length=200, verbose_name="字典值")

    def __str__(self):
        return f"{self.type}:{self.name}"


class UserApplication(models.Model):
    name = models.CharField(max_length=100, verbose_name="申请用户名")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    dept = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="申请部门")
    roles = models.ManyToManyField('Role', blank=True, verbose_name="申请角色")
    password = models.CharField(max_length=128, verbose_name="密码")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', '待审核'),
            ('approved', '已通过'),
            ('rejected', '已拒绝'),
        ],
        default='pending',
        verbose_name="申请状态"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"