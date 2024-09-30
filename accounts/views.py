from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Produto
from .forms import RegisterForm, ProdutoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# View de registro
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# View de login
def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'accounts/login.html')

# View de Home (apenas usuários logados podem acessar)
@login_required(login_url='login') 
def home_view(request):
    produtos = Produto.objects.all()
    return render(request, 'accounts/home.html', {'produtos': produtos})

# Verifica se o usuário é admin
def is_admin(user):
    return user.is_superuser

# View para adicionar produto (restrito a admins)
@login_required
@user_passes_test(is_admin)
def add_produto_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto adicionado com sucesso!')
            return redirect('home')
    else:
        form = ProdutoForm()
    return render(request, 'accounts/add_produto.html', {'form': form})    

# View para editar produto (restrito a admins)
@login_required
@user_passes_test(is_admin)
def update_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'accounts/update_produto.html', {'produto': produto})