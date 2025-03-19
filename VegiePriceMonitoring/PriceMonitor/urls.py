from django.urls import path
from . import views

urlpatterns = [
    path('', views.price_list, name='price_list'),
    path('vegetable/add/', views.add_vegetable, name='add_vegetable'),
    path('vegetable/update/<int:pk>/', views.update_vegetable, name='update_vegetable'),
    path('vegetable/delete/<int:pk>/', views.delete_vegetable, name='delete_vegetable'),
    path('transactions/', views.transaction_log, name='transaction_log')
]

