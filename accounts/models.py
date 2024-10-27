from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    descricao = models.TextField()

    def is_favorito(self, usuario):
        return self.favorito_set.filter(usuario=usuario).exists()

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # O preço total é calculado, então pode ser não editável
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação do pedido

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