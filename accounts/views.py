from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required

# 新規ユーザー登録処理
# フォームが有効ならユーザーを作成し、そのままログインして備品一覧へリダイレクト
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)  # username=社員番号として保存
            login(request, user)
            return redirect('supplies:list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

# ログイン処理
# フォームが有効ならログインし、備品一覧へリダイレクト
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('supplies:list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

# ログアウト処理
# ログアウト後、ログアウト画面を表示
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


# 以下はpermission管理系のビュー
# @login_required
# def permission_list(request):
#     permissions = Permission.objects.all()
#     return render(request, 'accounts/permission_list.html', {'permissions': permissions})

# @login_required
# def permission_detail(request, pk):
#     permission = Permission.objects.get(pk=pk)
#     return render(request, 'accounts/permission_detail.html', {'permission': permission})

# @login_required
# def permission_create(request):
#     if request.method == 'POST':
#         # Handle form submission for creating a new permission
#         pass
#     return render(request, 'accounts/permission_form.html')

# @login_required
# def permission_update(request, pk):
#     permission = Permission.objects.get(pk=pk)
#     if request.method == 'POST':
#         # Handle form submission for updating the permission
#         pass
#     return render(request, 'accounts/permission_form.html', {'permission': permission})

# @login_required
# def permission_delete(request, pk):
#     permission = Permission.objects.get(pk=pk)
#     if request.method == 'POST':
#         permission.delete()
#         # Redirect to permission list
#     return render(request, 'accounts/permission_confirm_delete.html', {'permission': permission})