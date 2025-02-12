from django.urls import path
from . import views


urlpatterns = [    
    path('neworder', views.neworder, name='neworder'),    
    path('orders', views.orders, name = 'orders'),
    path('edit-order/<int:id>', views.edit_order, name='edit-order'),
    path('print/<int:id>', views.print, name='print'),
    path('test', views.test, name='test'),
    path('loader', views.loader, name='loader')  
    ]