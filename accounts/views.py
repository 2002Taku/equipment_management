from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def signup(request):
    """
    新規ユーザー登録（サインアップ）処理
    POST: 入力内容でユーザー作成、ログイン後に備品一覧へリダイレクト
    GET: 空フォームを表示
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.employee_id  # ログインIDとして社員番号を使用
            user.save()
            login(request, user)
            return redirect('supplies:list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """
    ログイン処理
    POST: 認証成功で備品一覧へリダイレクト
    GET: 空フォームを表示
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('supplies:list')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    ログアウト処理
    ログアウト後にログアウト完了画面を表示
    """
    logout(request)
    return render(request, 'accounts/logout.html')

# permission管理系のテンプレートパスも 'accounts/' に修正
@login_required
def permission_list(request):
    """
    権限一覧表示
    """
    permissions = Permission.objects.all()
    return render(request, 'accounts/permission_list.html', {'permissions': permissions})

@login_required
def permission_detail(request, pk):
    """
    権限詳細表示
    """
    permission = Permission.objects.get(pk=pk)
    return render(request, 'accounts/permission_detail.html', {'permission': permission})

@login_required
def permission_create(request):
    """
    権限新規作成（未実装）
    """
    if request.method == 'POST':
        # Handle form submission for creating a new permission
        pass
    return render(request, 'accounts/permission_form.html')

@login_required
def permission_update(request, pk):
    """
    権限編集（未実装）
    """
    permission = Permission.objects.get(pk=pk)
    if request.method == 'POST':
        # Handle form submission for updating the permission
        pass
    return render(request, 'accounts/permission_form.html', {'permission': permission})

@login_required
def permission_delete(request, pk):
    """
    権限削除
    POST: 削除実行
    GET: 確認画面表示
    """
    permission = Permission.objects.get(pk=pk)
    if request.method == 'POST':
        permission.delete()
        # Redirect to permission list
    return render(request, 'accounts/permission_confirm_delete.html', {'permission': permission})