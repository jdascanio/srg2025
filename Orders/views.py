from django.shortcuts import render
from Orders.models import *
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User

# Create your views here.

def neworder (request):
    return render (request, 'neworder.html')