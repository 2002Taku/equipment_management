from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('<int:item_id>/', views.review_list, name='list'),
    path('<int:item_id>/create/', views.review_create, name='create'),
]