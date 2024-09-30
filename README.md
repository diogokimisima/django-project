# Sistema de Gerenciamento de Restaurante

Este projeto foi desenvolvido como parte de uma entrega acadêmica e consiste em uma aplicação web para a gestão de um restaurante. O sistema foi implementado utilizando Django como framework back-end, com banco de dados MySQL, e Tailwind CSS para estilização da interface.

## Objetivo do Sistema

O sistema tem como objetivo gerenciar os pedidos e produtos de um restaurante, oferecendo diferentes permissões para administradores e clientes:

- **Administradores**: Podem gerenciar (adicionar, editar, excluir) produtos.
- **Clientes**: Podem visualizar produtos e fazer pedidos, sem acesso a funcionalidades administrativas.

## Tecnologias Utilizadas

### Backend
- **Django**: Framework web de alto nível para o desenvolvimento rápido de aplicações seguras e escaláveis.
- **MySQL**: Sistema de gerenciamento de banco de dados relacional para armazenar informações de usuários, produtos e pedidos.

### Frontend
- **HTML5/CSS3**: Linguagens base para estrutura e estilo da aplicação.
- **Tailwind CSS**: Framework CSS utilizado para criar interfaces modernas e responsivas.

### Outros
- **Django ORM**: Interface de consulta de banco de dados do Django.
- **Django Authentication**: Sistema de autenticação do Django para controle de acessos.
- **MySQL Workbench**: Ferramenta para gerenciamento visual do banco de dados MySQL.

## Funcionalidades

### Cadastro e Login
- **Cadastro de Usuário**: Permite que usuários se registrem como clientes.
- **Autenticação**: Diferencia usuários comuns de administradores e, com base nisso, exibe as telas apropriadas.

### Controle de Acesso
- **Administrador**: Visualiza o cardápio e pode gerenciar os produtos (adicionar, editar e excluir).
- **Cliente**: Visualiza o cardápio de produtos e pode realizar pedidos.

### Gerenciamento de Produtos (Admin)
- **Adicionar Produtos**: O administrador pode cadastrar novos produtos, inserindo nome, descrição, preço e imagem.

## Estrutura do Projeto

### Páginas do Sistema
O sistema possui cinco páginas principais:
1. **Login**: Página onde o usuário insere suas credenciais.
2. **Register**: Página de cadastro de novos usuários.
3. **Home**: Exibe os produtos disponíveis.
4. **Adicionar Produto**: Página para cadastrar novos produtos (somente admin).
5. **Editar Produto**: Página para edição de produtos (somente admin).

### Diretórios e Arquivos Principais
- **restaurant/**: Diretório principal do projeto Django.
  - `settings.py`: Configurações do Django, incluindo o banco de dados MySQL.
  - `urls.py`: Definição das URLs do sistema.
  - `wsgi.py`: Interface de gateway entre Django e o servidor web.
- **accounts/**: Aplicação principal que gerencia as funcionalidades do restaurante.
  - `models.py`: Define os modelos para o banco de dados, como Usuários e Produtos.
  - `views.py`: Processa as requisições e renderiza os templates.
  - `forms.py`: Define os formulários da aplicação.
  - **templates/**: Diretório contendo os templates HTML.
  - **static/**: Diretório contendo arquivos estáticos (CSS, JS, imagens).

### Modelos

- **Usuário (User)**
  - Campos: `username`, `email`, `password`
- **Produto (Product)**
  - Campos: `nome`, `descricao`, `preco`, `imagem`

### URLs (Páginas)
- `/accounts/login/`: Página de login.
- `/accounts/register/`: Página de cadastro.
- `/accounts/home/`: Exibe os produtos (acesso para admin e cliente).
- `/accounts/add_produto/`: Adicionar novo produto (somente admin).
- `/accounts/update_produtos/<int:id>/`: Editar produto (somente admin).

### Views
- **LoginView**: Autenticação e redirecionamento do usuário baseado no tipo (admin ou cliente).
- **ProductListView**: Lista de produtos, com botões de gerenciamento para administradores.
- **AddProductView**: Adição de novos produtos ao banco de dados (admin).
- **EditProductView**: Edição de produtos existentes (admin).
- **OrderView**: Exibição dos produtos para clientes fazerem pedidos.
- **OrderHistoryView**: Histórico de pedidos do cliente.

## Banco de Dados

### Configuração
O banco de dados MySQL foi configurado no arquivo `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'restaurant',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
``` 

### Migrações
Para criar as tabelas, execute as migrações:

```cmd
python manage.py migrate
Tabelas criadas:
```

- **auth_user:** Tabela padrão do Django para usuários.
- **restaurant_produto**: Tabela que armazena os produtos.

### Estilização
O sistema foi estilizado utilizando Tailwind CSS. Abaixo estão os padrões de cores e fontes definidos:

**Padrões de Cores Utilizados**
- Tomate (Tomato): #750310, #92000E, #AB222E, #AB4D55
- Menta (Mint): #04D361
- Bolo (Cake): #065E7C, #82F3FF
- Escuro (Dark): #000405, #00111A, #0D1D25
- Gradiente: #091E26 a #00131C (Fundo do banner)
- Fontes Utilizadas
- Poppins: Usada para títulos.
- Roboto: Usada para textos de leitura geral.

**Responsividade**
O sistema foi configurado para ser responsivo, adaptando-se a diferentes tamanhos de tela (dispositivos móveis, tablets e desktops).

### Validação de Regras de Negócio
Verificação de Permissões: Decoradores @login_required e @user_passes_test garantem que apenas administradores acessem funções de gerenciamento.
Exibição Dinâmica de Elementos: Itens de gerenciamento de produtos são exibidos apenas para administradores. Elementos de pedidos são exibidos apenas para clientes.

### Conclusão
Este sistema de gerenciamento de restaurante foi desenvolvido com Django, MySQL e Tailwind CSS, garantindo uma interface moderna e funcional. O projeto foca na separação clara de permissões e uma experiência de usuário otimizada.
