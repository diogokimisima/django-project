from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
import re

def validate_nome_categoria(value):
    if re.search(r'[^a-zA-Z0-9\s\-àáâãéêíóôõúçÀÁÂÃÉÊÍÓÔÕÚÇ]', value):
        raise ValidationError('O nome da categoria não pode conter caracteres especiais')
    
    if len(value) < 3:
        raise ValidationError('O nome da categoria deve ter pelo menos 3 caracteres')

class Categoria(models.Model):
    nome = models.CharField(
        max_length=255, 
        validators=[validate_nome_categoria],
        unique=True
    )
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    def clean(self):
        # Convertendo o nome para title case (primeira letra de cada palavra em maiúsculo)
        self.nome = self.nome.title()
        super().clean()

def validate_produto_nome(value):
    if len(value) < 3:
        raise ValidationError('O nome do produto deve ter pelo menos 3 caracteres')

class Produto(models.Model):
    nome = models.CharField(max_length=255, validators=[validate_produto_nome])
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message='O preço deve ser maior que zero'),
            MaxValueValidator(10000, message='O preço não pode ser maior que R$10.000')
        ]
    )
    imagem = models.ImageField(upload_to='produtos/', default='produtos/default.jpg')
    descricao = models.TextField(validators=[MinLengthValidator(10, 'A descrição deve ter pelo menos 10 caracteres')])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True, related_name='produtos')

    def is_favorito(self, usuario):
        return self.favorito_set.filter(usuario=usuario).exists()

    def clean(self):
        if not self.categoria:
            raise ValidationError('Um produto deve pertencer a uma categoria')
        super().clean()

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message='A quantidade mínima é 1'),
            MaxValueValidator(100, message='A quantidade máxima é 100')
        ]
    )
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.preco_total = self.produto.preco * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido de {self.usuario.username} - {self.produto.nome} (Quantidade: {self.quantidade})"
    
class Favorito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'produto')