from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-produto/', views.add_produto_view, name='add_produto'),
    path('incluir-pedido/<int:produto_id>/', views.incluir_pedido, name='incluir_pedido'),
    path('pedidos/', views.pedidos_view, name='pedidos'),
    path('update_produto/<int:id>/', views.update_produto, name='update_produto'),
    path('produto/<int:produto_id>/delete/', views.delete_produto, name='delete_produto')
]

