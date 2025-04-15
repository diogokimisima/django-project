from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CategoriaViewSet, 
    ProdutoViewSet, 
    PedidoViewSet, 
    FavoritoViewSet,
    UserAPIView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API",
        default_version='v1',
        description="API para gerenciamento de restaurante",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Configurar o router
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'produtos', ProdutoViewSet)
router.register(r'pedidos', PedidoViewSet, basename='pedido')
router.register(r'favoritos', FavoritoViewSet, basename='favorito')

urlpatterns = [
    # URLs do router
    path('', include(router.urls)),
    
    # URL para o usuário atual
    path('me/', UserAPIView.as_view(), name='user-me'),
    
    # URLs do Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]