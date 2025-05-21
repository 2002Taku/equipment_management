from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.archive_list, name='list'),
    path('hide/<int:item_id>/', views.archive_hide, name='hide'),
    path('restore/<int:item_id>/', views.archive_restore, name='restore'),
]