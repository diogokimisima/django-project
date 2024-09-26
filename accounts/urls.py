from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-produto/', views.add_produto_view, name='add_produto'),
]

