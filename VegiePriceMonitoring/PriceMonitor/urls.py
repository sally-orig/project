from django.urls import path
from . import views

urlpatterns = [
    path('', views.price_list, name='price_list'),
    path('add_vegetable/', views.add_vegetable, name='add_vegetable'),
]

