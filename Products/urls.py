from django.urls import path
from . import views


urlpatterns = [    
    path('motivo', views.motivo, name='motivo'),
    path('producto', views.producto, name='producto'),
    path('estado', views.estado, name='estado'),
    path('search-family',views.search_family, name='search-family')
    
    ]