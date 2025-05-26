from django.urls import path
from . import views

app_name = 'supplies'

urlpatterns = [
    path('', views.item_list, name='list'),
    path('<int:item_id>/', views.item_detail, name='detail'),
    path('create/', views.item_create, name='create'),
    path('<int:item_id>/edit/', views.item_edit, name='edit'),
    path('<int:item_id>/delete/', views.item_delete, name='delete'),
    path('<int:item_id>/reviews/', views.review_list, name='review_list'),
    path('<int:item_id>/reviews/create/', views.review_create, name='review_create'),
    path('review/<int:review_id>/delete/', views.review_delete_confirm, name='review_delete'),
]