from django.db import models
from system.models import User
# 系统已有检测工具
class DetectionTool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 业务方选择的检测工具
class BusinessDetectionTool(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(DetectionTool, on_delete=models.CASCADE)
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tool.name}"

# 预检测管理
class PreDetectionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', '待检测'),
        ('success', '成功'),
        ('failed', '失败'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tools = models.ManyToManyField(DetectionTool)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    vulnerabilities_count = models.IntegerField(default=0)
    report_file = models.FileField(upload_to='detection_reports/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status} - {self.requested_at.strftime('%Y-%m-%d %H:%M')}"
