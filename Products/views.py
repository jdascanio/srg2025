from django.shortcuts import render
from Products.models import *
from Products.forms import *

# Create your views here.

def motivo (request):
    family = Family.objects.all().order_by('family')
    motivos = Reason.objects.all().order_by('family','reason')

    if request.method == "POST":
        if 'create-reason' in request.POST:
            form = AddReason(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_reason = Reason(
                    reason = data['reason'],
                    family = data['family']
                )
                new_reason.save()
                motivos = Reason.objects.all().order_by('family','reason')
                return render(request, 'motivo.html', {"motivos":motivos, "family":family})
        elif 'edit-reason' in request.POST:
            form = EditReason(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                motivo = Reason.objects.get(id=int(data['reason_id']))
                motivo.reason = data['reason']
                motivo.family = data['family']
                motivo.save()

                motivos = Reason.objects.all().order_by('family','reason')
                return render(request, 'motivo.html', {"motivos":motivos, "family":family})
        elif 'delete-reason' in request.POST:
            form = DeleteReason(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                motivo = Reason.objects.get(id=int(data['reason_id']))
                motivo.delete()

                motivos = Reason.objects.all().order_by('family','reason')
                return render(request, 'motivo.html', {"motivos":motivos, "family":family})

    return render (request, 'motivo.html', {"motivos":motivos, "family":family})

def producto (request):
    family = Family.objects.all().order_by('family')
    subcat = Subcat.objects.all().order_by('subcat')
    productos = Products.objects.all().order_by('family','subcat','name')

    if request.method == "POST":
        if 'create-product' in request.POST:
            form = AddProduct(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_product = Products(
                    name = data['name'],
                    family = data['family'],
                    subcat = data['subcat']
                )
                new_product.save()
                productos = Products.objects.all().order_by('family','subcat','name')
                return render(request, 'producto.html', {"productos":productos,"family":family,"subcat":subcat})
        elif 'edit-product' in request.POST:
            form = EditProduct(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                producto = Products.objects.get(id=int(data['product_id']))
                producto.name = data['name']
                producto.family = data['family']
                producto.subcat = data['subcat']
                producto.save()

                productos = Products.objects.all().order_by('family','subcat','name')
                return render(request, 'producto.html', {"productos":productos,"family":family,"subcat":subcat})
        elif 'delete-product' in request.POST:
            form = DeleteProduct(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                producto = Products.objects.get(id=int(data['product_id']))
                producto.delete()

                productos = Products.objects.all().order_by('family','subcat','name')
                return render(request, 'producto.html', {"productos":productos,"family":family,"subcat":subcat})

    return render(request, 'producto.html', {"productos":productos,"family":family,"subcat":subcat})

def estado (request):
    family = Family.objects.all().order_by('family')
    estados = Status.objects.all().order_by('family','status')

    if request.method == "POST":
        if 'create-status' in request.POST:
            form = AddStatus(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_status = Status(
                    status = data['status'],
                    family = data['family']
                )
                new_status.save()
                estados = Status.objects.all().order_by('family','status')
                return render(request, 'estado.html', {"estados":estados,"family":family})
        
        elif 'edit-status' in request.POST:
            form = EditStatus(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                estado = Status.objects.get(id=int(data['status_id']))
                estado.status = data['status']
                estado.family = data['family']
                
                estado.save()

                estados = Status.objects.all().order_by('family','status')
                return render(request, 'estado.html', {"estados":estados,"family":family})
        
        elif 'delete-status' in request.POST:
            form = DeleteStatus(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                estado = Status.objects.get(id=int(data['status_id']))
                estado.delete()

                estados = Status.objects.all().order_by('family','status')
                return render(request, 'estado.html', {"estados":estados,"family":family})

    return render (request, 'estado.html', {"estados":estados,"family":family})