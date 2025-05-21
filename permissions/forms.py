from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Permission

class SignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=6, label="社員番号")
    department = forms.CharField(max_length=100, label="所属部署")
    first_name = forms.CharField(max_length=30, label="氏名")

    class Meta:
        model = CustomUser
        fields = ('employee_id', 'department', 'first_name', 'username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="社員番号またはユーザー名")

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['user', 'permission_level']  # Adjust fields as necessary based on your Permission model
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'permission_level': forms.Select(attrs={'class': 'form-control'}),
        }