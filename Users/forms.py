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

class DeleteUser(forms.Form):
    user_id = forms.CharField(max_length=30)

class EditUser(forms.Form):
    user_id = forms.CharField(max_length=30)
    user_name = forms.CharField(max_length=30)
    user_mail = forms.EmailField()
    user_psw = forms.CharField()
    user_distributor = forms.CharField(max_length=20)
    user_is_admin = forms.BooleanField(required=False)