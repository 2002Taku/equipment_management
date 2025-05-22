from django.urls import path
from . import views

app_name = 'lending'

urlpatterns = [
    path('status/<int:item_id>/', views.lending_status, name='status'),
    path('<int:item_id>/borrow/', views.lending_borrow, name='borrow'),  # ← 正しい関数名に修正
    path('return/<int:item_id>/', views.lending_return, name='return'),
]