from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # サインアップ
    path('login/', views.login_view, name='login'),  # ログイン
    path('logout/', views.logout_view, name='logout'),  # ログアウト
]