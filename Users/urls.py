from django.urls import path
from . import views


urlpatterns = [    
    path('register', views.register, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('users', views.users, name='users')
    ]