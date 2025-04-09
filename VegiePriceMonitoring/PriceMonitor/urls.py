from django.urls import path
from . import views

urlpatterns = [
    path('', views.price_list, name='price_list'),
    path('vegetable/add/', views.add_vegetable, name='add_vegetable'),
    path('vegetable/update/<int:pk>/', views.update_vegetable, name='update_vegetable'),
    path('vegetable/delete/<int:pk>/', views.delete_vegetable, name='delete_vegetable'),
    path('vegetable/actions-log/', views.vegetable_actions_log, name='vegetable_actions'),
    path('vegetable/price-chart/', views.veg_price_chart, name='veg_price_chart')
]

