from django import forms
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    department = forms.CharField(max_length=100, label="所属部署")
    username = forms.CharField(max_length=6, label="社員番号")  # usernameを社員番号として使う

    class Meta:
        model = CustomUser
        fields = ('username', 'department', 'first_name', 'last_name', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    # ログイン用フォーム。社員番号またはユーザー名でログイン可能
    username = forms.CharField(label="社員番号またはユーザー名")

# class PermissionForm(forms.ModelForm):
#     # 権限管理用フォーム
#     class Meta:
#         model = Permission
#         fields = ['user', 'permission_level']
#         widgets = {
#             'user': forms.Select(attrs={'class': 'form-control'}),
#             'permission_level': forms.TextInput(attrs={'class': 'form-control'}),
#         }