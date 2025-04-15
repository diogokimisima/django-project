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

# Limitar os métodos/operações dos ViewSets
class LimitedCategoriaViewSet(CategoriaViewSet):
    http_method_names = ['get']  # Apenas listagem e detalhes

class LimitedProdutoViewSet(ProdutoViewSet):
    http_method_names = ['get']  # Apenas listagem e detalhes

class LimitedPedidoViewSet(PedidoViewSet):
    http_method_names = ['get', 'post']  # Listagem, detalhes e criação

class LimitedFavoritoViewSet(FavoritoViewSet):
    http_method_names = ['get', 'post']  # Listagem, detalhes e toggle (via action)

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Restaurant API - Accounts",
        default_version='v1',
        description="API para endpoints relacionados às funcionalidades de contas e pedidos do restaurante",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[path('api/', include('accounts.api_urls'))],  # Limita ao escopo da API
)

# Configurar o router
router = DefaultRouter()
# Usar as versões limitadas dos ViewSets
router.register(r'categorias', LimitedCategoriaViewSet)
router.register(r'produtos', LimitedProdutoViewSet)
router.register(r'pedidos', LimitedPedidoViewSet, basename='pedido')
router.register(r'favoritos', LimitedFavoritoViewSet, basename='favorito')

urlpatterns = [
    # URLs do router
    path('', include(router.urls)),
    
    # URL para o usuário atual
    path('me/', UserAPIView.as_view(), name='user-me'),
    
    # URLs do Swagger (específicos para accounts)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-accounts'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-accounts'),
]