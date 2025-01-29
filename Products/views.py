from django.shortcuts import render
from Products.models import *

# Create your views here.

def motivo (request):
    motivos = Reason.objects.all().order_by('family','reason')
    return render (request, 'motivo.html', {"motivos":motivos})

def producto (request):
    productos = Products.objects.all().order_by('family','subcat','name')
    return render(request, 'producto.html', {"productos":productos})

def estado (request):
    estados = Status.objects.all().order_by('family','status')
    return render (request, 'estado.html', {"estados":estados})