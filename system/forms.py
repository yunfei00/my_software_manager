from django import forms
from .models import Department, User, Role, DictItem

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
