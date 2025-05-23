
# Projeto Django Simples

Este é um projeto básico utilizando Django. Este README irá guiá-lo sobre como configurar e inicializar o ambiente de desenvolvimento para rodar o projeto.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado em sua máquina:

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)
- Virtualenv (para criar ambientes virtuais)

## Passos para iniciar o projeto

### 1. Clonar o repositório

Primeiro, clone o repositório para o seu computador:

```bash
git clone https://github.com/ffernandosf/BackendTCC.git
cd BackendTCC/projeto
```

### 2. Criar e ativar o ambiente virtual

Crie um ambiente virtual para o projeto:

```bash
python -m venv venv
```

Ative o ambiente virtual:

- **Windows:**

```bash
venv\Scripts\activate
```

- **Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

Com o ambiente virtual ativado, instale as dependências do projeto listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Se você estiver usando PostgreSQL, MySQL ou outro banco de dados, você deve configurar as variáveis de ambiente correspondentes.

Se o banco de dados for SQLite (configuração padrão), não será necessário configurar nada.

### 5. Rodar as migrações

Execute as migrações para configurar o banco de dados:

```bash
python manage.py migrate
```

### 6. Criar um superusuário (opcional)

Se você quiser acessar o painel administrativo do Django, crie um superusuário:

```bash
python manage.py createsuperuser
```

### 7. Rodar o servidor de desenvolvimento

Agora, você pode rodar o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
```

O servidor estará rodando em `http://127.0.0.1:8000/`.

### 8. Acessar o painel administrativo (opcional)

Para acessar o painel administrativo, vá para `http://127.0.0.1:8000/admin/` e faça login com o superusuário que você criou.

## Dependências

- Django>=4.0,<5.0
- djangorestframework>=3.12,<4.0
- psycopg2>=2.9,<3.0 (opcional, se estiver usando PostgreSQL)
- gunicorn>=20.0,<21.0 (opcional, para produção)
- python-dotenv>=0.19,<1.0 (opcional, para variáveis de ambiente)
- django-debug-toolbar>=3.2,<4.0 (opcional, para depuração)
- whitenoise>=5.0,<6.0 (opcional, para arquivos estáticos)



