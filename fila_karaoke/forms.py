from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Promocao

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('cpf', 'email', 'first_name', 'last_name', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='CPF')

class PromocaoForm(forms.ModelForm):
    class Meta:
        model = Promocao
        fields = ['titulo', 'descricao', 'valor', 'imagem']