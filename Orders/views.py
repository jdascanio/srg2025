from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from Orders.models import *
from django.db.models import Count, Sum, Q
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from email.utils import formataddr
from django.shortcuts import redirect
from Orders.forms import *
import datetime as dt
from datetime import date, datetime
import random
import string
import pandas as pd
import csv
import codecs
import sys
import json


# Create your views here.
def lector ():
    lineas = OrderContent.objects.all()
    total = str(lineas.count()).zfill(8)
    letras = ''.join(random.choices(string.ascii_uppercase, k=2))
    return letras+total

def filename ():
    prefijo = 'garantias_'
    sufijo = dt.datetime.now().strftime('%d-%m-%Y')
    return prefijo+sufijo

def add_line_number(queryset):
    result = []
    for index, obj in enumerate(queryset):
        result.append({
            **obj.__dict__,
            'line': index + 1 
        })
    return result

def nro_orden ():
    
    dia = dt.datetime.now().strftime('%m%d')
    hora = dt.datetime.now().strftime('%H%M%S')
    letras1 = ''.join(random.choices(string.ascii_uppercase, k=2))
    letras2 = ''.join(random.choices(string.ascii_uppercase, k=3))
    listanros = random.choices(range(0,9), k=5)    
    numeros = str("".join(map(str, listanros)))
    return letras1 + hora + dia

def check_status (datos, order_hd):
    if not order_hd.reception_date:
        return "dejar"
    else:
        if datos.filter(cig='P').exists():
            return "pendiente"
        elif order_hd.finish_date:
            return "finalizado"
        elif order_hd.start_date:
            return "recepcion"
        elif order_hd.reception_date:
            return "recibido"
        else:
            return "dejar"


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
                subcat_product = Products.objects.get(name = data['product'])
                order_hd = OrderHeader.objects.filter(prov_order_number=data['prov_order_number']).first()
                order_hd.user_name = data['user_name']
                order_hd.save()
                distributor = order_hd.user_name

                new_line = OrderContent(
                    user = request.user,
                    order_header = order_hd,
                    user_name = usuario.distributor,
                    prov_order_number = data['prov_order_number'],
                    family = data['family'],
                    status = data['status'],
                    subcat = subcat_product.subcat,
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
                        "total":total,
                        "order_hd":order_hd,
                        "distributor":distributor
                   })
            
        elif 'order_save' in request.POST:
            form = SaveOrder(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                total = datos.count()
                order_hd.user_name = data['user_name']
                order_hd.total_products = total
                order_hd.visible = True
                order_hd.save()

                new_order_nr = data['prov_order_number_hd']
                products = add_line_number(datos)
                distributor = order_hd.user_name             

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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
            
        elif 'delete-row' in request.POST:
            row_id = DeleteRow(request.POST)
            if row_id.is_valid():
                dato = row_id.cleaned_data
                row = OrderContent.objects.get(id=dato['row_id'])
                orden = row.prov_order_number
                row.delete()

                order_hd = OrderHeader.objects.get(prov_order_number=row.prov_order_number)
                datos = OrderContent.objects.filter(prov_order_number=row.prov_order_number)
                total = datos.count()

                new_order_nr = row.prov_order_number
                products = add_line_number(datos)
                distributor = order_hd.user_name             

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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'edit-product' in request.POST:
            form = EditProductLine(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                product_row = OrderContent.objects.get(id=data['line_id'])
                
                product_row.user_name = data['user_name']
                product_row.status = data['status']
                product_row.missing_elem = data['missing_elem']
                product_row.product = data['product']
                product_row.in_sn = data['in_sn']
                product_row.client = data['client']
                product_row.seller = data['seller']
                product_row.reason = data['reason']
                product_row.cig = data['cig']
                product_row.observations = data['observations']
                product_row.out_sn = data['out_sn']
                product_row.invoice = data['invoice']  

                product_row.save()              
                
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number'])
                total = datos.count()

                new_order_nr = data['prov_order_number']
                products = add_line_number(datos)
                distributor = order_hd.user_name             

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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'order_send' in request.POST:
            form = request.POST
            order_hd = OrderHeader.objects.get(prov_order_number=form['prov_order_number_hd'])
            order = Order.objects.get(id=1)
            order_nr = order.order_nr + 1
            order.order_nr = order_nr
            order.save()
            neworder_nr = str(order_nr).zfill(8)

            order_hd.order_stage = "envio"
            order_hd.order_status = True
            order_hd.order_number = neworder_nr
            order_hd.send_date = dt.datetime.now().strftime("%Y-%m-%d")
            order_hd.save()

            subject = f'Orden de reparación #{order_hd.order_number} - Cargada'
            message = f'NO RESPONDA ESTE MAIL\n\n\nLa orden {order_hd.order_number} ha sido cargada. Aguardamos la recepción de la misma en nuestras oficinas.\nRecuerde identificar el envoltorio/paquete con el nro de orden de reparación.'
            # from_email = '"Garantias Positron" <pstargentina@gmail.com>'
            to_emails = [usuario.email]
            # to_emails = ['julian.dascanio@gmail.com']
        
            bcc_emails = ['sat@pstarg.com.ar'] 
            email = EmailMessage(
                subject,
                message,
                '"Garantias Positron" <pstargentina@gmail.com>',
                to_emails,
                bcc=bcc_emails
            )
        
            email.send()       


            return redirect ('/Orders/orders')
        

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
                        "total":total,
                        "order_hd":order_hd
                   })

def orders (request):
    usuario = Profile.objects.get(user=request.user.id)
    if usuario.is_admin == True:
        orders = OrderHeader.objects.filter(visible=True, order_status=True).order_by('-order_number')
    else:
        orders = OrderHeader.objects.filter(visible=True, user_name=usuario.distributor).order_by('-id')
    return render(request, 'orders.html',
                  {
                      "orders": orders,
                      "usuario":usuario
                  })
def search_order(request):

    if request.GET['user_name']:
        usuario = Profile.objects.get(user=request.user.id)
        distri = request.GET['user_name']
        alerta = f'No se han encontrado órdenes para de distribuidor "{distri}".'
        orders = OrderHeader.objects.filter(visible=True,order_status=True, user_name__icontains=distri).order_by('-id')
        if orders: 
            return render(request, 'orders.html',
                        {
                            "orders": orders,
                            "usuario":usuario,
                            
                        })
        else:
            if usuario.is_admin == True:
                orders = OrderHeader.objects.filter(visible=True, order_status=True).order_by('-order_number')
            else:
                orders = OrderHeader.objects.filter(visible=True, user_name=usuario.distributor).order_by('-id')
            return render(request, 'orders.html',
                  {
                      "orders": orders,
                      "usuario":usuario,
                      "alerta":alerta
                  })
    else:
        alerta2 = f'Debe ingresar un distribuidor para poder filtar'
        usuario = Profile.objects.get(user=request.user.id)
        if usuario.is_admin == True:
            orders = OrderHeader.objects.filter(visible=True, order_status=True).order_by('-order_number')
        else:
            orders = OrderHeader.objects.filter(visible=True, user_name=usuario.distributor).order_by('-id')
        return render(request, 'orders.html',
                  {
                      "orders": orders,
                      "usuario":usuario,
                      "alerta2":alerta2
                  })


def edit_order (request, id):
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
    usuarios = Profile.objects.all()
    usuario = Profile.objects.get(user=request.user.id)
    order_hd = OrderHeader.objects.get(id=id)
    datos = OrderContent.objects.filter(prov_order_number=order_hd.prov_order_number)
    total = datos.count()
    new_order_nr = order_hd.prov_order_number
    products = add_line_number(datos)
    distributor = order_hd.user_name

    if request.method == "POST":
        if 'add-product' in request.POST:
            form = AddProductLine(request.POST)            
            if form.is_valid():
                data = form.cleaned_data

                order_hd = OrderHeader.objects.filter(prov_order_number=data['prov_order_number']).first()
                order_hd.user_name = data['user_name']
                order_hd.save()
                distributor = order_hd.user_name

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

                return render (request, 'edit-order.html',
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
                        "total":total,
                        "order_hd":order_hd,
                        "distributor":distributor
                   })
        elif 'order_save' in request.POST:
            form = SaveOrder(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                total = datos.count()
                order_hd.user_name = data['user_name']
                order_hd.total_products = total
                order_hd.visible = True
                if data['start_date']:
                    order_hd.start_date = data['start_date']
                stage = check_status(datos, order_hd)
                if stage != "dejar":    
                    order_hd.order_stage = stage
                order_hd.save()

                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                new_order_nr = data['prov_order_number_hd']
                products = add_line_number(datos)
                distributor = order_hd.user_name

                return render (request, 'edit-order.html',
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'order_recieved' in request.POST:
            form = SaveOrder(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                total = datos.count()
                order_hd.user_name = data['user_name']
                order_hd.reception_date = dt.datetime.now().strftime("%Y-%m-%d")
                order_hd.order_stage = "recepcion"
                order_hd.total_products = total
                order_hd.visible = True
                order_hd.save()

                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                new_order_nr = data['prov_order_number_hd']
                products = add_line_number(datos)
                distributor = order_hd.user_name             

                return render (request, 'edit-order.html',
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'order_close' in request.POST:
            form = SaveOrder(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                total = datos.count()
                order_hd.user_name = data['user_name']
                order_hd.finish_date = dt.datetime.now().strftime("%Y-%m-%d")
                order_hd.total_products = total
                if datos.filter(cig='P').exists():
                    order_hd.order_stage = "pendiente"
                    print('encontrado P')
                else:
                    order_hd.order_stage = "finalizado"
                    print('no encontrado P')
                order_hd.save()
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])                

                new_order_nr = data['prov_order_number_hd']
                products = add_line_number(datos)
                distributor = order_hd.user_name

                subject = f'Orden de reparación #{order_hd.order_number} - Finalizada'
                message = f'NO RESPONDA ESTE MAIL\n\n\nLa orden {order_hd.order_number} ha sido finalizada y se encuentra disponible para ser retirada en nuestras oficinas'
                # SENDER_EMAIL = 'Positron Argentina <pstargentina@gmail.com>'
                # from_email = 'pstargentina@gmail.com'
                to_emails = [usuario.email]
                # to_emails = ['jdascanio@stoneridge.com']
            
                bcc_emails = ['sat@pstarg.com.ar'] 

                email = EmailMessage(
                    subject,
                    message,
                    '"Garantias Positron" <pstargentina@gmail.com>',
                    to_emails,
                    bcc=bcc_emails # This is where you add the BCC recipients
                )
            
                email.send()             

                return render (request, 'edit-order.html',
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'order_end' in request.POST:
            form = SaveOrder(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                total = datos.count()
                order_hd.user_name = data['user_name']
                order_hd.return_date = dt.datetime.now().strftime("%Y-%m-%d")
                order_hd.total_products = total
                order_hd.tracking = data['tracking']
                order_hd.blocked = True
                if datos.filter(cig='P').exists():
                    order_hd.order_stage = "pendiente"
                else:
                    order_hd.order_stage = "devuelto"
                order_hd.save()

                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number_hd'])
                for line in datos:
                    new_complete_order = CompleteOrder(
                        order_header = order_hd,
                        order_number = order_hd.order_number,
                        prov_order_number = order_hd.prov_order_number,
                        user_name = order_hd.user_name,
                        total_products = 1,
                        tracking = order_hd.tracking,
                        send_date = order_hd.send_date,
                        reception_date = order_hd.reception_date,
                        start_date = order_hd.start_date,
                        finish_date = order_hd.finish_date,
                        return_date = order_hd.return_date,
                        order_stage = order_hd.order_stage,
                        order_status = order_hd.order_status,
                        blocked = order_hd.blocked,
                        family = line.family,
                        subcat = line.subcat,
                        status = line.status,
                        missing_elem = line.missing_elem,
                        product = line.product,
                        in_sn = line.in_sn,
                        client = line.client,
                        seller = line.seller,
                        reason = line.reason,
                        cig = line.cig,
                        observations = line.observations,
                        out_sn = line.out_sn,
                        invoice = line.invoice
                    )
                    new_complete_order.save()



                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number_hd'])
                new_order_nr = data['prov_order_number_hd']
                products = add_line_number(datos)
                distributor = order_hd.user_name
                          

                return redirect ('/Orders/orders')

        elif 'delete-row' in request.POST:
            row_id = DeleteRow(request.POST)
            if row_id.is_valid():
                dato = row_id.cleaned_data
                row = OrderContent.objects.get(id=dato['row_id'])
                orden = row.prov_order_number
                row.delete()

                order_hd = OrderHeader.objects.get(prov_order_number=row.prov_order_number)
                datos = OrderContent.objects.filter(prov_order_number=row.prov_order_number)
                total = datos.count()

                new_order_nr = row.prov_order_number
                products = add_line_number(datos)
                distributor = order_hd.user_name             

                return render (request, 'edit-order.html',
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'edit-product' in request.POST:
            form = EditProductLine(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                product_row = OrderContent.objects.get(id=data['line_id'])
                
                product_row.user_name = data['user_name']
                product_row.status = data['status']
                product_row.missing_elem = data['missing_elem']
                product_row.product = data['product']
                product_row.in_sn = data['in_sn']
                product_row.client = data['client']
                product_row.seller = data['seller']
                product_row.reason = data['reason']
                product_row.cig = data['cig']
                product_row.observations = data['observations']
                product_row.out_sn = data['out_sn']
                product_row.invoice = data['invoice']  

                product_row.save()              
                
                order_hd = OrderHeader.objects.get(prov_order_number=data['prov_order_number'])
                datos = OrderContent.objects.filter(prov_order_number=data['prov_order_number'])
                total = datos.count()
                stage = check_status(datos, order_hd)
                if stage != "dejar":    
                    order_hd.order_stage = stage
                order_hd.save()

                new_order_nr = data['prov_order_number']
                products = add_line_number(datos)
                distributor = order_hd.user_name             

                return render (request, 'edit-order.html',
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
                   })
        elif 'order_send' in request.POST:
            form = request.POST
            order_hd = OrderHeader.objects.get(prov_order_number=form['prov_order_number_hd'])
            order = Order.objects.get(id=1)
            order_nr = order.order_nr + 1
            order.order_nr = order_nr
            order.save()
            neworder_nr = str(order_nr).zfill(8)

            
            order_hd.order_status = True
            order_hd.order_number = neworder_nr
            order_hd.order_stage = "envio"
            order_hd.send_date = dt.datetime.now().strftime("%Y-%m-%d")
            order_hd.save()                       
            return redirect ('/Orders/orders')
        elif 'cancel' in request.POST:
            form = request.POST
            order_hd = OrderHeader.objects.get(prov_order_number=form['prov_order_number_hd'])
            order_hd.blocked = True
            order_hd.order_stage = "cancelada"
            order_hd.save()   
            return redirect ('/Orders/orders')

    return render (request,'edit-order.html',{
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
                        "distributor":distributor,
                        "usuario":usuario,
                        "usuarios":usuarios,
                        "total":total,
                        "order_hd":order_hd
    })
  
def print_order (request, id):
    usuario = Profile.objects.get(user=request.user.id)
    order_hd = OrderHeader.objects.get(id=id)
    datos = OrderContent.objects.filter(prov_order_number=order_hd.prov_order_number)
    products = add_line_number(datos)
    return render (request, 'print.html', {"order_hd":order_hd, "products":products,"usuario":usuario})






def data_download (request):
    
    form = CompleteOrder.objects.all().values()
    # form = OrderContent.objects.filter(Q(order_number__isnull=True), Q(order_number='')).values()
    list_of_dicts = list(form)
    DB = pd.DataFrame(list_of_dicts)

    columns_to_drop = ['id','order_header_id', 'prov_order_number','total_products','tracking','send_date','start_date','order_stage','order_status','blocked',]  # List of columns to remove
    DB = DB.drop(columns=columns_to_drop, errors='ignore') 

    new_columns = {
        'user_name': 'Distribuidor',
        'order_number': 'Nro_Orden',
        'reception_date': 'F. Recepcion',
        'finish_date':'F. Finalizacion',
        'return_date':'F. Devolucion',
        'family': 'Familia',
        'subcat': 'Subcategoria',
        'status': 'Estado',
        'missing_elem': 'Faltantes',
        'product': 'Producto',
        'in_sn': 'Nro Serie',
        'client': 'Cliente',
        'seller': 'Vendedor',
        'reason': 'Motivo',
        'observations': 'Obs',
        'out_sn': 'Egresa SN',
        'invoice': 'Factura'
    }
    DB = DB.rename(columns=new_columns)
    name = filename()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{name}.xlsx"'
    DB.to_excel(response, index=False)
    # DB.to_excel(response, index=False)
    # DB.to_excel('data.xlsx', index=False)
    return response
    # return render (request, 'test.html')
    

# def loader (request):
#     with codecs.open("C:\\Users\\jdascanio\\OneDrive - Stoneridge Inc\\Documentos\\Python\\Garantias2025\\padrones\\Producto.csv","r",encoding="ANSI") as padron:
#         csv_lector = csv.reader(padron, delimiter=';')
#         for n in csv_lector:
#             new_status = Products(
#                     name = n[0],
#                     family = n[1],
#                     subcat = n[2]
#                 )
#             # new_status.save()

#     return render(request,'test.html')

def sortList(e):
    return e['quantity']
def subcat (start_date, end_date):
    subcat_stats = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date) #Filter by date in the OrderHeader
    ).values('subcat').annotate(
        product_count=Count('product')
    ).order_by('subcat')
    valores = []
    subcat = []

    for item in subcat_stats:
        valores.append({"subcategory":item['subcat'], "quantity":item['product_count']})

    sorted_valores = sorted(valores, key=sortList, reverse=True)
    line = 0
    otros = 0
    for item in sorted_valores:
        if line < 4:
            subcat.append(item)
            line += 1
        else:
            otros += item['quantity']
    subcat.append({"subcategory":'otros',"quantity":otros})
    return subcat

def cig_stats (start_date, end_date):
    cig = []
    cig_stats = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date), order_header__finish_date__isnull=False #Filter by date in the OrderHeader
    ).values('cig').annotate(
        product_count=Count('product')

    ).order_by('cig')

    for item in cig_stats:
        cig.append({"cig":item['cig'], "quantity":item['product_count']})

    scrap_family_list = []
    repair_family_list =[]
    cig_family = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date), order_header__finish_date__isnull=False #Filter by date in the OrderHeader
    ).values('cig','subcat').annotate(
        product_count=Count('subcat')
    )
    fam = []
    for item in cig_family:
        fam.append(item['subcat'])
    familias = set(fam)
    fam = list(familias)

    for item in cig_family:
        for cat in fam:
            if item['cig'] == '2-B' or item['cig'] == '1-E':
                if item['subcat'] == cat:
                    scrap_family_list.append({'family':item['subcat'], "quantity":item['product_count']})
    for item in cig_family:
        for cat in fam:
            if item['cig'] == '2-A':
                if item['subcat'] == cat:
                    repair_family_list.append({'family':item['subcat'], "quantity":item['product_count']})
    
    return (cig, cig_stats,scrap_family_list,repair_family_list)


def prod_stats (start_date, end_date):
    product_count = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date), order_header__finish_date__isnull=False #Filter by date in the OrderHeader
    ).count()

    prod_stats = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date), order_header__finish_date__isnull=False #Filter by date in the OrderHeader
    ).values('product').annotate(
        product_count=Count('product')
    )

    unsorted_products = []
    productsA = []
    

    for item in prod_stats:
        unsorted_products.append({"product":item['product'], "quantity":item['product_count']})

    sorted_products = sorted(unsorted_products, key=sortList, reverse=True)
    line = 0
    otros = 0
    for item in sorted_products:
        if line < 10:
            productsA.append(item)
            line += 1
        else:
            otros += item['quantity']
    # products.append({"product":'otros',"quantity":otros})
    products = sorted(productsA, key=sortList, reverse=False)

    return (products, product_count)

def reason_stats (start_date, end_date):
    reason_stats = OrderContent.objects.filter(
        order_header__send_date__range = (start_date, end_date), order_header__finish_date__isnull=False #Filter by date in the OrderHeader
    ).values('reason').annotate(
        product_count=Count('product')
    )
    unsorted_reason = []
    reason = []
    for item in reason_stats:
        unsorted_reason.append({"reason":item['reason'], "quantity":item['product_count']})

    sorted_reason = sorted(unsorted_reason, key=sortList, reverse=True)
    line = 0
    for item in sorted_reason:
        if line < 5:
            reason.append(item)
            line += 1
    return reason

def dashboard_stats (request):
    usuario = Profile.objects.get(user=request.user.id)
    today = date.today()
    start_date = date(today.year,today.month,1)
    end_date = today

    
    info = []
    datos_cig = cig_stats(start_date,end_date)
    datos_products = prod_stats(start_date,end_date)

    info.append({"subcat": subcat(start_date,end_date)})
    info.append({"cig_stats": datos_cig[0]})
    info.append({"prod_stats": datos_products[0]})
    info.append({"reason_stats": reason_stats(start_date,end_date)})
    info.append({"family_scrap": datos_cig[2]})
    info.append({"family_repair": datos_cig[3]})


    order_stats = OrderHeader.objects.filter(
        send_date__range = (start_date, end_date), finish_date__isnull=False 
    ).count()

    
    
    graph1 = {}
    graph1['orders'] = order_stats
    graph1['products'] = datos_products[1]
    for item in datos_cig[1]:
        if item['cig'] == '1-A':
            graph1['sin_falla'] = item['product_count']
        elif item['cig'] == '2-B' or item['cig'] == '1-E':
            graph1['scrap'] = item['product_count']

    if request.method == "GET":
        if 'dateRange' in request.GET:
            sdate = request.GET['startDate']
            edate = request.GET['endDate']
            start_date = datetime.strptime(sdate, '%Y-%m-%d').date()
            end_date = datetime.strptime(edate, '%Y-%m-%d').date()

            info = []
            datos_cig = cig_stats(start_date,end_date)
            datos_products = prod_stats(start_date,end_date)

            info.append({"subcat": subcat(start_date,end_date)})
            info.append({"cig_stats": datos_cig[0]})
            info.append({"prod_stats": datos_products[0]})
            info.append({"reason_stats": reason_stats(start_date,end_date)})
            info.append({"family_scrap": datos_cig[2]})
            info.append({"family_repair": datos_cig[3]})


            order_stats = OrderHeader.objects.filter(
                send_date__range = (start_date, end_date), finish_date__isnull=False 
            ).count()



            graph1 = {}
            graph1['orders'] = order_stats
            graph1['products'] = datos_products[1]
            for item in datos_cig[1]:
                if item['cig'] == '1-A':
                    graph1['sin_falla'] = item['product_count']
                elif item['cig'] == '2-B' or item['cig'] == '1-E':
                    graph1['scrap'] = item['product_count']
    


    with open('Orders\static\orders\json\categorias.json', 'w') as f: 
        json.dump(info, f)  
        
    
    return render(request, 'dashboard.html', {"usuario":usuario, "graph1":graph1, "fecha":{"start":start_date, "finish":end_date}})

def sendmails (request):
    usuario = Profile.objects.get(id=5)

    subject = f'Orden de reparación'
    message = f'No responda este mail\n\nLa orden 000001 ha sido enviada usuario {usuario.user_name}'
    sender_name = "Garantías Positron"
    sender_email = settings.EMAIL_HOST_USER
    from_email = formataddr((sender_name, sender_email))
    to_list = ['julian.dascanio@gmail.com']
    bcc_list= ['jdascanio@stoneridge.com']
    email = EmailMessage(subject, message, from_email, to_list, bcc=bcc_list)
    email.send()
    return HttpResponse('Email sent successfully!')
    
    # return redirect ('/Orders/orders')