from django.shortcuts import render
from Orders.models import *
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User
from Orders.forms import *
import datetime
import random
import string

# Create your views here.
def lector ():
    lineas = OrderContent.objects.all()
    total = str(lineas.count()).zfill(8)
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    return letras+total

def add_line_number(queryset):
    result = []
    for index, obj in enumerate(queryset):
        result.append({
            **obj.__dict__,
            'line': index + 1 
        })
    return result

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
    total = 0
    usuarios = Profile.objects.all()
    
    usuario = Profile.objects.get(user=request.user.id)    

    if request.method == "POST":
        if 'add-product' in request.POST:
            form = AddProductLine(request.POST)            
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.filter(prov_order_number=data['prov_order_number']).first()
                new_line = OrderContent(
                    user = request.user,
                    order_header = order_hd,
                    user_name = usuario.distributor,
                    prov_order_number = data['prov_order_number'],
                    family = data['family'],
                    status = data['status'],
                    missing_elem = data['missing_elem'],
                    product = data['product'],
                    in_sn = data['in_sn'],
                    client = data['client'],
                    seller = data['seller'],
                    reason = data['reason'],
                    cig = data['cig'],
                    observations = data['observations'],
                    out_sn = data['out_sn'],
                    invoice = data['invoice']
                )
                new_line.save()

                new_order_nr = data['prov_order_number']
                data = OrderContent.objects.filter(prov_order_number=data['prov_order_number'])
                products = add_line_number(data)
                total = data.count()                

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
                        "new_order_nr":new_order_nr,
                        "products": products,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total
                   })
            else:
                print('Form no valido')
    new_order_nr = nro_orden()
    new_order_hd = OrderHeader(
        user = request.user,
        prov_order_number = new_order_nr
    )
    
    new_order_hd.save()
    order_hd = OrderHeader.objects.filter(prov_order_number=new_order_hd.prov_order_number).first()
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
                        "new_order_nr":new_order_nr,
                        "usuarios":usuarios,
                        "usuario":usuario,
                        "total":total
                   })

def test (request):
    
    if request.method == "GET":
        form = request.GET
        print(form)
        
    return render (request, 'test.html')