from django.urls import path
from . import views


urlpatterns = [    
    path('motivo', views.motivo, name='motivo'),
    path('producto', views.producto, name='producto'),
    path('estado', views.estado, name='estado')
    
    ]