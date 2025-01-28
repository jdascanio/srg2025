from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class Login_formulario (AuthenticationForm):   
    class Meta:
        model = User
        fields = ['username', 'password']

class Register1 (UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2', 'email']

class Register2 (forms.Form):
    distribuidor = forms.CharField(max_length=20, required=True)   
    administrador = forms.BooleanField(required=False, initial=False)   