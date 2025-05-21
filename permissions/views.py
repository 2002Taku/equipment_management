from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.employee_id  # ログインIDとして社員番号を使用
            user.save()
            login(request, user)
            return redirect('inventory:list')
    else:
        form = SignUpForm()
    return render(request, 'permissions/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inventory:list')
    else:
        form = LoginForm()
    return render(request, 'permissions/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'permissions/logout.html')

@login_required
def permission_list(request):
    permissions = UserPermission.objects.all()
    return render(request, 'permissions/permission_list.html', {'permissions': permissions})

@login_required
def permission_detail(request, pk):
    permission = UserPermission.objects.get(pk=pk)
    return render(request, 'permissions/permission_detail.html', {'permission': permission})

@login_required
def permission_create(request):
    if request.method == 'POST':
        # Handle form submission for creating a new permission
        pass
    return render(request, 'permissions/permission_form.html')

@login_required
def permission_update(request, pk):
    permission = UserPermission.objects.get(pk=pk)
    if request.method == 'POST':
        # Handle form submission for updating the permission
        pass
    return render(request, 'permissions/permission_form.html', {'permission': permission})

@login_required
def permission_delete(request, pk):
    permission = UserPermission.objects.get(pk=pk)
    if request.method == 'POST':
        permission.delete()
        # Redirect to permission list
    return render(request, 'permissions/permission_confirm_delete.html', {'permission': permission})