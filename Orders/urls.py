from django.urls import path
from . import views


urlpatterns = [    
    path('neworder', views.neworder, name='neworder'),    
    path('orders', views.orders, name = 'orders'),
    path('edit-order/<int:id>', views.edit_order, name='edit-order'),
    path('print_order/<int:id>', views.print_order, name='print_order'),
    path('search-order', views.search_order, name='search-order'),
    path('data_download', views.data_download, name='data_download'),
    path('sendmails', views.sendmails, name='sendmails'),
    path('dashboard', views.dashboard_stats, name='dashboard_stats')
    ]