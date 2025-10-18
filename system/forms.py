from django import forms
from .models import Department, User, Role, DictItem, Tool, LoginLog, OperationLog, Menu, Post, WorkflowConfig

class DeptForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'parent', 'status']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'code', 'status']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone', 'company', 'dept', 'roles', 'status']
        widgets = {'roles': forms.CheckboxSelectMultiple()}

class DictForm(forms.ModelForm):
    class Meta:
        model = DictItem
        fields = ['name', 'type', 'value', 'status']


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'api_url', 'description', 'status']


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'path', 'parent', 'status']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'code', 'status']


class WorkflowConfigForm(forms.ModelForm):
    class Meta:
        model = WorkflowConfig
        fields = ['name', 'steps', 'status']
        widgets = {'steps': forms.Textarea(attrs={'rows': 3})}

