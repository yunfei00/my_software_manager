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
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name="公司名称")  # ← 新增字段
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

class Tool(BaseModel):
    """检测工具管理"""
    name = models.CharField(max_length=100, verbose_name="工具名称")
    api_url = models.URLField(verbose_name="API接口地址")
    description = models.TextField(blank=True, null=True, verbose_name="说明")

    class Meta:
        verbose_name = "检测工具管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class LoginLog(models.Model):
    """登录日志"""
    username = models.CharField(max_length=50, verbose_name="用户名")
    ip = models.GenericIPAddressField(verbose_name="登录IP")
    status = models.CharField(max_length=10, choices=[("成功", "成功"), ("失败", "失败")], verbose_name="状态")
    time = models.DateTimeField(auto_now_add=True, verbose_name="时间")

    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name

class OperationLog(models.Model):
    """操作日志"""
    module = models.CharField(max_length=100, verbose_name="系统模块")
    operator = models.CharField(max_length=50, verbose_name="操作人员")
    ip = models.GenericIPAddressField(verbose_name="操作IP")
    action = models.CharField(max_length=100, verbose_name="操作内容")
    time = models.DateTimeField(auto_now_add=True, verbose_name="时间")

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name

class Menu(BaseModel):
    """菜单管理"""
    name = models.CharField(max_length=100, verbose_name="菜单名称")
    path = models.CharField(max_length=200, verbose_name="路径")
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级菜单")

    class Meta:
        verbose_name = "菜单管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(BaseModel):
    """岗位管理"""
    name = models.CharField(max_length=100, verbose_name="岗位名称")
    code = models.CharField(max_length=50, verbose_name="岗位编码")

    class Meta:
        verbose_name = "岗位管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class WorkflowConfig(BaseModel):
    """审批流程配置"""
    name = models.CharField(max_length=100, verbose_name="流程名称")
    steps = models.TextField(verbose_name="流程步骤（JSON）")

    class Meta:
        verbose_name = "审批流程配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
