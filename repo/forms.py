from django import forms
from .models import Repository, Image

class RepositoryForm(forms.ModelForm):
    images = forms.ModelMultipleChoiceField(
        queryset=Image.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Repository
        fields = ['name', 'repo_type', 'images']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # 用户只能看到自己有权限的镜像
        self.fields['images'].queryset = Image.objects.filter(models.Q(owner=user) | models.Q(owner__isnull=True))
