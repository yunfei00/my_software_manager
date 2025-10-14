from django import forms
from ..models  import UserApplication

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserApplication
        fields = ['name', 'phone', 'dept', 'roles']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # 检查重复申请
        if UserApplication.objects.filter(name=name, status='pending').exists():
            raise forms.ValidationError('该用户名已有申请正在审核中，请勿重复提交。')

        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致。')

        cleaned_data['password'] = password1
        return cleaned_data

    def save(self, commit=True):
        app = super().save(commit=False)
        app.password = self.cleaned_data['password']
        if commit:
            app.save()
            self.save_m2m()
        return app
