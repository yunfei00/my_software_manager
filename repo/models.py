from django.db import models
from system.models import User

# 平台提供的基础镜像或业务方申请入库的镜像
class Image(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 平台镜像 owner=None
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}:{self.version}"

# 仓库
class Repository(models.Model):
    REPO_TYPE_CHOICES = (
        ('system', '系统'),
        ('test', '测试'),
        ('production', '生产'),
    )
    name = models.CharField(max_length=100)
    repo_type = models.CharField(max_length=20, choices=REPO_TYPE_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Image, through='RepositoryImage')

    def image_count(self):
        return self.images.count()

    def __str__(self):
        return self.name

# 仓库-镜像关联表
class RepositoryImage(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
