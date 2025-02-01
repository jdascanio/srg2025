from django.shortcuts import render
from Orders.models import *
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User
import datetime
import random
import string

# Create your views here.
def nro_orden ():
    
    dia = datetime.datetime.now().strftime('%m%d')
    hora = datetime.datetime.now().strftime('%H%M%S')
    letras1 = ''.join(random.choices(string.ascii_uppercase, k=2))
    letras2 = ''.join(random.choices(string.ascii_uppercase, k=3))
    listanros = random.choices(range(0,9), k=5)    
    numeros = str("".join(map(str, listanros)))
    return letras1 + hora + dia


def neworder (request):
    #LOADS CONTENT AND CREATES PROV_ORDER_NR
    new_order_nr = nro_orden()
    new_order_hd = OrderHeader(
        user = request.user,
        prov_order_number = new_order_nr
    )
    
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

    print({"new_order_hd":new_order_hd})

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
                        "cig":cig,
                        "new_order_nr":new_order_nr
                   })