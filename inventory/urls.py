from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.item_list, name='list'),
    path('create/', views.item_create, name='create'),
    path('search/', views.item_search, name='search'),
    path('item/<int:item_id>/', views.item_detail, name='detail'),
    path('item/<int:item_id>/edit/', views.item_edit, name='edit'),
    path('item/<int:item_id>/delete/', views.item_delete, name='delete'),
]