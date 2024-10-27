from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('add-produto/', views.add_produto_view, name='add_produto'),
    path('favoritos/', views.favoritos_view, name='favoritos_view'),
    path('add-categoria/', views.add_categoria_view, name='add_categoria'),

    path('incluir-pedido/<int:produto_id>/', views.incluir_pedido, name='incluir_pedido'),
    path('pedidos/delete/<int:id>/', views.delete_pedido, name='delete_pedido'),
    path('update_produto/<int:id>/', views.update_produto, name='update_produto'),
    path('produto/<int:produto_id>/delete/', views.delete_produto, name='delete_produto'),
    path('toggle-favorito/<int:produto_id>/', views.toggle_favorito, name='toggle_favorito'),
]

