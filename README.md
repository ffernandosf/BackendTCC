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