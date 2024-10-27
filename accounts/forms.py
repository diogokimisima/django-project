from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Produto, Categoria
from django.db import models


# Formulário de registro
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'imagem', 'categoria']  # Adicione 'categoria' aqui

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), required=True)


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']