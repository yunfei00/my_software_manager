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
    name = models.CharField(max_length=100, verbose_name="部门名称")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级部门")

    def __str__(self):
        return self.name

class Role(BaseModel):
    name = models.CharField(max_length=100, verbose_name="角色名称")
    code = models.CharField(max_length=50, verbose_name="权限标识", unique=True)

    def __str__(self):
        return self.name

class User(BaseModel):
    name = models.CharField(max_length=100, verbose_name="用户名称")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="手机号")
    dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="所属部门")
    roles = models.ManyToManyField(Role, blank=True, verbose_name="角色")

    def __str__(self):
        return self.name

class DictItem(BaseModel):
    name = models.CharField(max_length=100, verbose_name="字典名称")
    type = models.CharField(max_length=50, verbose_name="字典类型")
    value = models.CharField(max_length=200, verbose_name="字典值")

    def __str__(self):
        return f"{self.type}:{self.name}"
