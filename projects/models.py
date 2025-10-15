# projects/models.py
from django.db import models
from system.models import User  # 复用用户模型

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name="项目名称")
    code = models.CharField(max_length=50, unique=True, verbose_name="项目编码")
    description = models.TextField(blank=True, null=True, verbose_name="项目描述")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="负责人")
    status = models.IntegerField(default=1, choices=[(1, "进行中"), (2, "已完成"), (3, "暂停")], verbose_name="状态")
    start_date = models.DateField(null=True, blank=True, verbose_name="开始时间")
    end_date = models.DateField(null=True, blank=True, verbose_name="结束时间")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = "项目管理"

    def __str__(self):
        return self.name
