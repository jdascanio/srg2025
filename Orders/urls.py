from django.urls import path
from . import views


urlpatterns = [    
    path('neworder', views.neworder, name='neworder'),
    path('orders', views.orders, name = 'orders'),
    path('test', views.test, name='test')  
    ]