from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from Users.models import *
from Orders.models import *
from Users.forms import *
from . import views

# Create your views here.

def login_request(request):
    
    if request.user.is_authenticated:
            return render(request, 'index.html')
    else:
        if request.method == "POST":

            formulario = Login_formulario(request, data=request.POST)

            if formulario.is_valid():
                usuario = formulario.cleaned_data.get("username")
                contrasenia = formulario.cleaned_data.get("password")

                user = authenticate(username=usuario, password=contrasenia)

                if user is not None:
                    login(request, user)
                    if request.user.is_staff:
                        #accion si el usuario es admin (cargar perfil)
                        print('es administrador')
                    else:
                        #accion si el usuario NO es admin (cargar perfil)
                        print('no es staff')
                    print('etapa4')
                    return render(request, 'index.html')
                else:
                    print('etapa3')
                    return render(
                        request, "login.html", {"mensaje": "Error. Formulario erroneo."}
                    )

            else:
                formulario = Login_formulario()
                return render(
                    request,
                    "login.html",
                    {
                        "formulario": formulario,
                        "mensaje": "Error. Datos de ingreso incorrectos",
                    },
                )
        else:            
            formulario = Login_formulario()
            return render(request, "login.html", {"formulario": formulario})

    # return redirect('/Orders/orders')
    return render(request, 'loged.html')


def logout_user (request):
    logout(request)

    return redirect("login_request")

def register (request):
    form1 = Register1()
    form2 = Register2()
    if request.method == 'POST':
        form1 = Register1(request.POST)
        form2 = Register2(request.POST)

        if form1.is_valid() and form2.is_valid():
            new_user = form1.save()
            user_data = form1.cleaned_data
            user_extra = form2.cleaned_data
            user_passwrd = user_data['password1']
            
            # print (new_user.id, new_user.username)
            # print(request.user)
            user_profile = Profile(
                user = new_user,
                user_name = new_user.username,
                passwrd = user_passwrd,
                email = new_user.email,
                distributor = user_extra['distribuidor'],
                is_admin = user_extra['administrador']
            )
            user_profile.save()
        else:
            return render(request, 'register.html', {"form1":form1,"form2":form2})    

    return render(request, 'register.html', {"form1":form1,"form2":form2})