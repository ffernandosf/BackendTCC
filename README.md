# Sistema de Gestão de Energia Elétrica

## Como Executar o Projeto

### 1. Configuração Inicial

```bash
# Clone o repositório (se necessário)
cd BackendTCC/projetoBack

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração do Banco de Dados

```bash
# Execute as migrações
python manage.py makemigrations
python manage.py migrate
```

### 3. Criar Usuários

#### Superusuário (Admin)
```bash
python manage.py createsuperuser
```
- Username: `admin`
- Email: `admin@admin.com`
- Password: `admin123`

#### Usuário de Teste
```bash
python create_user.py
```
Cria automaticamente:
- Username: `testuser`
- Password: `test123`

### 4. Executar o Servidor

```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## Testando as APIs no Postman

### Login (Rota Pública)
**POST** `http://localhost:8000/api/login/`

**Body (JSON):**
```json
{
    "username": "testuser",
    "password": "test123"
}
```

**Resposta:**
```json
{
    "token": "abc123...",
    "user_id": 1,
    "username": "testuser",
    "is_staff": false
}
```

### Rotas Protegidas
Use o token retornado no header:

**Header:**
```
Authorization: Token abc123...
```

**Exemplos:**
- **GET** `/api/gestao/aparelhos/` - Listar aparelhos
- **POST** `/api/gestao/aparelhos/` - Criar aparelho
- **PUT** `/api/gestao/aparelhos/1/` - Atualizar aparelho
- **DELETE** `/api/gestao/aparelhos/1/` - Deletar aparelho

## Usuários Disponíveis

| Username | Password | Tipo |
|----------|----------|------|
| `admin` | `admin123` | Superusuário |
| `testuser` | `test123` | Usuário comum |

## URLs Principais

- **Admin**: `http://localhost:8000/admin/`
- **Web Interface**: `http://localhost:8000/gestao/`
- **API Base**: `http://localhost:8000/api/`



## Atividade 3 - CRUD WEB

O CRUD WEB de usuários está localizado no template [usuarios/templates/usuarios/crud.html](projetoBack/usuarios/templates/usuarios/crud.html). Ele permite que administradores criem, atualizem e deletem usuários diretamente pela interface web. O funcionamento se dá por meio de formulários HTML que enviam requisições POST para as views responsáveis pelo gerenciamento dos usuários. Os dados são exibidos em uma tabela, permitindo edição inline e exclusão com confirmação.

---

## Atividade 4 - CRUD API

O CRUD da API está implementado no [UserViewSet](projetoBack/usuarios/views.py) e registrado nas rotas do arquivo [usuarios/urls.py](projetoBack/usuarios/urls.py) sob o endpoint `/api/users/`. Ele utiliza o Django REST Framework para expor endpoints RESTful para criação, leitura, atualização e exclusão de usuários. O acesso é protegido por autenticação, e usuários comuns só podem acessar seus próprios dados, enquanto administradores têm acesso a todos.

---

## Atividade 5 - AUTH API

A autenticação da API está implementada em [usuarios/simple_login.py](projetoBack/usuarios/simple_login.py) e [usuarios/auth_views.py](projetoBack/usuarios/auth_views.py). Os endpoints principais são `/api/login/` e `/api/usuarios/logout/`. O login retorna um token de autenticação, que deve ser usado no header `Authorization` das requisições subsequentes. O logout e a revogação de tokens também são suportados, garantindo segurança nas sessões.

---

## Atividade 6 - ORM

O uso do ORM (Object-Relational Mapping) do Django está presente nos arquivos de modelos, especialmente em [gestao/models.py](projetoBack/gestao/models.py) e [usuarios/models.py](projetoBack/usuarios/models.py). O ORM permite manipular dados do banco de dados usando classes Python, facilitando operações como criação, consulta, atualização e exclusão de registros sem a necessidade de escrever SQL manualmente. Os modelos `Gestao`, `Analise` e o modelo padrão de `User` são exemplos de uso do ORM neste projeto.