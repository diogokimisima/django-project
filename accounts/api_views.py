from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Categoria, Produto, Pedido, Favorito
from .serializers import (
    CategoriaSerializer, 
    ProdutoSerializer, 
    PedidoSerializer, 
    FavoritoSerializer,
    UserSerializer
)
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de Categorias de produtos.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Lista todas as categorias disponíveis",
        responses={200: CategoriaSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria uma nova categoria",
        request_body=CategoriaSerializer,
        responses={201: CategoriaSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de Produtos.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @swagger_auto_schema(
        operation_description="Lista todos os produtos disponíveis",
        manual_parameters=[
            openapi.Parameter('categoria', openapi.IN_QUERY, 
                             description="Filtrar por categoria", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, 
                             description="Buscar por nome ou descrição", type=openapi.TYPE_STRING),
        ],
        responses={200: ProdutoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Filtra por categoria se especificado
        categoria_id = request.query_params.get('categoria')
        if categoria_id:
            queryset = queryset.filter(categoria_id=categoria_id)
            
        # Busca por nome ou descrição
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(nome__icontains=search) | queryset.filter(descricao__icontains=search)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Retorna detalhes de um produto específico",
        responses={200: ProdutoSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PedidoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de Pedidos.
    """
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra pedidos para mostrar apenas os do usuário atual.
        """
        return Pedido.objects.filter(usuario=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Lista todos os pedidos do usuário logado",
        responses={200: PedidoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Cria um novo pedido",
        request_body=PedidoSerializer,
        responses={201: PedidoSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class FavoritoViewSet(viewsets.ModelViewSet):
    """
    API para gerenciamento de Favoritos.
    """
    serializer_class = FavoritoSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra favoritos para mostrar apenas os do usuário atual.
        """
        return Favorito.objects.filter(usuario=self.request.user)
    
    @swagger_auto_schema(
        operation_description="Lista todos os favoritos do usuário logado",
        responses={200: FavoritoSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    @swagger_auto_schema(
        operation_description="Alternar um produto como favorito (adicionar/remover)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['produto_id'],
            properties={
                'produto_id': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: "{'success': True, 'message': 'Produto adicionado/removido dos favoritos'}"}
    )
    def toggle(self, request):
        produto_id = request.data.get('produto_id')
        if not produto_id:
            return Response({"error": "Produto ID é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)
            
        produto = get_object_or_404(Produto, id=produto_id)
        favorito = Favorito.objects.filter(usuario=request.user, produto=produto).first()
        
        if favorito:
            favorito.delete()
            return Response({"success": True, "message": "Produto removido dos favoritos"})
        else:
            Favorito.objects.create(usuario=request.user, produto=produto)
            return Response({"success": True, "message": "Produto adicionado aos favoritos"})


class UserAPIView(APIView):
    """
    API para gerenciamento do usuário atual.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retorna os detalhes do usuário logado",
        responses={200: UserSerializer()}
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Atualiza os dados do usuário logado",
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)