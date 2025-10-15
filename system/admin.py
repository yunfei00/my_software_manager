from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "create_time", "update_time", "status")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("额外信息", {"fields": ("phone", "dept")}),
    )
    list_display = ("name", "phone", "get_roles", "dept", "company", "status")

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = "角色"
