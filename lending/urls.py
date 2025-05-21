from django.urls import path
from . import views

app_name = 'lending'

urlpatterns = [
    path('status/<int:item_id>/', views.lending_status, name='status'),
    path('borrow/<int:item_id>/', views.lending_borrow, name='borrow'),
    path('return/<int:item_id>/', views.lending_return, name='return'),
]