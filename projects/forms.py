from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'name', 'business_department', 'final_user', 'description',
            'expected_launch', 'status', 'base_image', 'components'
        ]
        widgets = {
            'expected_launch': forms.DateInput(attrs={'type': 'date'}),
            'components': forms.CheckboxSelectMultiple,
            'description': forms.Textarea(attrs={'rows': 3}),
        }
