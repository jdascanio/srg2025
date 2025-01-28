from django.urls import path
from . import views


urlpatterns = [    
    path('motivo', views.motivo, name='motivo'),
    
    ]