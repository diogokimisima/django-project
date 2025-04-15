from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Produto, Categoria, Pedido, Favorito
import re


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']

    def validate_nome(self, value):
        # Verifica se o nome tem pelo menos 3 caracteres
        if len(value) < 3:
            raise serializers.ValidationError("O nome da categoria deve ter pelo menos 3 caracteres.")
        
        # Verifica se já existe uma categoria com este nome (case insensitive)
        if Categoria.objects.filter(nome__iexact=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Já existe uma categoria com este nome.")
        
        return value


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True
    )

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'imagem', 'descricao', 'categoria', 'categoria_id']

    def validate_nome(self, value):
        # Verifica se o nome tem pelo menos 3 caracteres
        if len(value) < 3:
            raise serializers.ValidationError("O nome do produto deve ter pelo menos 3 caracteres.")
        return value

    def validate_preco(self, value):
        # Verifica se o preço é positivo e não excede um valor máximo razoável
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        if value > 10000:
            raise serializers.ValidationError("O preço está muito alto (máximo R$10.000).")
        return value

    def validate_descricao(self, value):
        # Verifica se a descrição tem pelo menos 10 caracteres
        if len(value) < 10:
            raise serializers.ValidationError("A descrição deve ter pelo menos 10 caracteres.")
        return value


class PedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    
    class Meta:
        model = Pedido
        fields = ['id', 'usuario', 'produto', 'produto_nome', 'quantidade', 'preco_total', 'data_criacao']
        read_only_fields = ['preco_total', 'usuario']

    def validate_quantidade(self, value):
        # Verifica se a quantidade é positiva e não excede um valor máximo razoável
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        if value > 100:
            raise serializers.ValidationError("A quantidade máxima permitida é 100.")
        return value

    def create(self, validated_data):
        # Associa o usuário atual ao pedido
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class FavoritoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    produto_preco = serializers.ReadOnlyField(source='produto.preco')
    
    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'produto', 'produto_nome', 'produto_preco']
        read_only_fields = ['usuario']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorito.objects.all(),
                fields=['usuario', 'produto'],
                message="Este produto já está nos favoritos."
            )
        ]

    def create(self, validated_data):
        # Associa o usuário atual ao favorito
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        # Verifica se o username tem apenas caracteres alfanuméricos
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "O nome de usuário deve conter apenas letras, números e underscores."
            )
        return value

    def validate_email(self, value):
        # Verifica se o email já está cadastrado
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value