from django.shortcuts import render
from Orders.models import *
from Products.models import *
from Users.models import *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from Orders.forms import *
import datetime
import random
import string
import pandas as pd
import csv
import codecs
import sys

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
            else:        
                print('Form no valido')
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
            else:
                print(form)
        elif 'delete-row' in request.POST:
            row_id = DeleteRow(request.POST)
            if row_id.is_valid():
                dato = row_id.cleaned_data
                print(dato)
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
            order_hd.send_date = datetime.datetime.now().strftime("%Y-%m-%d")
            order_hd.save()                       
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
                order_hd.reception_date = datetime.datetime.now().strftime("%Y-%m-%d")
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
                order_hd.finish_date = datetime.datetime.now().strftime("%Y-%m-%d")
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
            
        elif 'delete-row' in request.POST:
            row_id = DeleteRow(request.POST)
            if row_id.is_valid():
                dato = row_id.cleaned_data
                print(dato)
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
            order_hd.send_date = datetime.datetime.now().strftime("%Y-%m-%d")
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
    order_hd = OrderHeader.objects.get(id=id)
    datos = OrderContent.objects.filter(prov_order_number=order_hd.prov_order_number)
    products = add_line_number(datos)
    return render (request, 'print.html', {"order_hd":order_hd, "products":products})






def test (request):
    
    form = OrderContent.objects.all().values()
    list_of_dicts = list(form)
    DB = pd.DataFrame(list_of_dicts)

    new_columns = {
        'user': 'id_usuario',
        'order_header': 'id_orden',
        'user_name': 'Distribuidor',
        'order_number': 'Nro_Orden',
        'prov_order_number': 'Nro_Orden_Provisorio',
        'family': 'Familia',
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

    DB.to_excel('data.xlsx', index=False)
    return render(request, 'test.html')

def loader (request):
    with codecs.open("C:\\Users\\jdascanio\\OneDrive - Stoneridge Inc\\Documentos\\Python\\Garantias2025\\padrones\\Producto.csv","r",encoding="ANSI") as padron:
        csv_lector = csv.reader(padron, delimiter=';')
        for n in csv_lector:
            new_status = Products(
                    name = n[0],
                    family = n[1],
                    subcat = n[2]
                )
            # new_status.save()

    return render(request,'test.html')