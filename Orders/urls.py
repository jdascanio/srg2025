from django.urls import path
from . import views


urlpatterns = [    
    path('neworder', views.neworder, name='neworder')    
    ]