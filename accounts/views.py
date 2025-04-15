from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Produto, Pedido, Favorito, Categoria
from .forms import RegisterForm, ProdutoForm, CategoriaForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.http import JsonResponse
from urllib.parse import urlencode
from django.utils.timezone import now

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
    categorias = Categoria.objects.all()

    search = request.GET.get('search', '')
    if search:
        produtos = produtos.filter(nome__icontains=search) | produtos.filter(descricao__icontains=search)

    categoria_id = request.GET.get('categoria')
    if categoria_id:
        produtos = produtos.filter(categoria__id=categoria_id)

    favoritos = Favorito.objects.filter(usuario=request.user).values_list('produto_id', flat=True)

    for produto in produtos:
        produto.is_favorito = produto.id in favoritos

    produtos_por_categoria = {}
    for categoria in categorias:
        produtos_por_categoria[categoria] = produtos.filter(categoria=categoria)

    return render(request, 'accounts/home.html', {
        'produtos_por_categoria': produtos_por_categoria,
        'categorias': categorias,
        'selected_categoria': categoria_id
    })



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

    categorias = Categoria.objects.all()

    return render(request, 'accounts/add_produto.html', {'form': form, 'categorias': categorias})    

# View para editar produto (restrito a admins)
@login_required
@user_passes_test(is_admin)
def update_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        preco = request.POST.get('preco', '').replace(',', '.')
        data = request.POST.copy()
        data['preco'] = preco

        form = ProdutoForm(data, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = ProdutoForm(instance=produto)

    categorias = Categoria.objects.all()

    return render(request, 'accounts/update_produto.html', {'form': form, 'produto': produto, 'categorias': categorias})

@login_required
@user_passes_test(is_admin)
def delete_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto deletado com sucesso!')
        return redirect('home')
    return redirect('update_produto', id=produto_id)

@login_required
def incluir_pedido(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1)) 
        pedido = Pedido(usuario=request.user, produto=produto, quantidade=quantidade)
        pedido.save()

        return JsonResponse({'success': True, 'message': 'Produto incluído no pedido com sucesso!'})

    return JsonResponse({'success': False, 'message': 'Erro ao incluir o produto.'})

@login_required
def pedidos_view(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    total = sum(pedido.preco_total for pedido in pedidos)
    return render(request, 'accounts/pedidos.html', {'pedidos': pedidos, 'total': total})

@login_required
def delete_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id, usuario=request.user)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido excluído com sucesso!')
        return redirect('pedidos')
    return redirect('pedidos')

@login_required
def toggle_favorito(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    favorito, created = Favorito.objects.get_or_create(usuario=request.user, produto=produto)

    if not created:
        favorito.delete()  
    message = "Produto adicionado aos favoritos!" if created else "Produto removido dos favoritos!"
    return JsonResponse({'success': True, 'message': message})

@login_required
def favoritos_view(request):
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('produto')
    return render(request, 'accounts/favoritos.html', {'favoritos': favoritos})

@login_required
@user_passes_test(is_admin)
def add_categoria_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('home')
    else:
        form = CategoriaForm()
    return render(request, 'accounts/add_categoria.html', {'form': form})

@login_required
def enviar_whatsapp(request):
    pedidos = Pedido.objects.filter(usuario=request.user)

    if not pedidos.exists():
        messages.error(request, "Você não tem pedidos para enviar.")
        return redirect('pedidos')

    detalhes_pedidos = "\n".join(
        [
            f"{pedido.quantidade}x {pedido.produto.nome} - R$ {pedido.preco_total:.2f}"
            for pedido in pedidos
        ]
    )
    total = sum(pedido.preco_total for pedido in pedidos)

    nome_cliente = request.user.first_name or request.user.username
    data_pedido = now().strftime("%d/%m/%Y %H:%M")

    mensagem = (
        f"*Novo Pedido Realizado!*\n\n"
        f"*Data do Pedido:* {data_pedido}\n"
        f"*Cliente:* {nome_cliente}\n\n"
        f"*Detalhes do Pedido:*\n{detalhes_pedidos}\n\n"
        f"*Total:* R$ {total:.2f}\n\n"
        f"*Ação Necessária:* Por favor, envie:\n"
        f"O endereço completo para entrega.\n"
        f"O método de pagamento escolhido (dinheiro, cartão, etc.).\n\n"
        f"Após enviar essas informações, confirme para que possamos processar o pedido."
    )

    numero_destino = "5518981969555" 

    mensagem_codificada = urlencode({"text": mensagem})

    whatsapp_url = f"https://wa.me/{numero_destino}?{mensagem_codificada}"

    return redirect(whatsapp_url)
