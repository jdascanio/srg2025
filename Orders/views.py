from django.shortcuts import render
from Orders.models import *
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User

# Create your views here.

def neworder (request):
    alm_products = Products.objects.filter(family='alarma').order_by('name')
    audio_products = Products.objects.filter(family='audio').order_by('name')
    taco_products = Products.objects.filter(family='tacografo').order_by('name')
    alm_reason = Reason.objects.filter(family='alarma').order_by('reason')
    audio_reason = Reason.objects.filter(family='audio').order_by('reason')
    taco_reason = Reason.objects.filter(family='tacografo').order_by('reason')
    alm_status = Status.objects.filter(family='alarma').order_by('status')
    audio_status = Status.objects.filter(family='audio').order_by('status')
    taco_status = Status.objects.filter(family='tacografo').order_by('status')
    cig = Cig.objects.all().order_by('cig')
    return render (request, 'neworder.html',
                   {
                       "alm_products":alm_products,
                        "audio_products":audio_products,
                        "taco_products":taco_products,
                        "alm_reason":alm_reason,
                        "audio_reason":audio_reason,
                        "taco_reason":taco_reason,
                        "alm_status":alm_status,
                        "audio_status":audio_status,
                        "taco_status":taco_status,
                        "cig":cig
                   })