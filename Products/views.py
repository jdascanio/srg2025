from django.shortcuts import render
from Products.models import *

# Create your views here.

def motivo (request):
    motivos = Reason.objects.all().order_by('family','reason')
    return render (request, 'motivo.html', {"motivos":motivos})