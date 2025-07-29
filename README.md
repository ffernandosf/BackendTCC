# 🔋 ECOWATT - Sistema de Gestão de Energia Elétrica

API REST desenvolvida em Django para gerenciamento inteligente de consumo de energia elétrica.

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### 2. Configuração do Ambiente

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd DB2/BackendTCC/projetoBack

# Crie e ative o ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Configuração do Banco de Dados

```bash
# Execute as migrações
python manage.py migrate

# Crie os usuários de teste
python create_user.py

# Crie um superusuário (admin)
python manage.py createsuperuser

# Ou use o script personalizado
python create_custom_user.py
```

### 4. Executar o Servidor

```bash
# Inicie o servidor de desenvolvimento
python manage.py runserver

# O servidor estará disponível em: http://127.0.0.1:8000
```

## 👥 Usuários Criados

### Usuários Comuns
O script `create_user.py` cria automaticamente:
- **testuser** / test123 (usuário padrão)
- **user1** / test123 (para testes de segurança)
- **user2** / test123 (para testes de segurança)

### Superusuário (Admin)
Para criar um administrador:
```bash
python manage.py createsuperuser
```

Ou use o script interativo:
```bash
python create_custom_user.py
```

## 🔧 Funcionalidades

- ✅ Autenticação com tokens JWT
- ✅ CRUD completo de aparelhos elétricos
- ✅ Cálculo automático de consumo (kWh)
- ✅ Cálculo automático de custos (R$)
- ✅ Análises de consumo mensal
- ✅ Segurança entre usuários
- ✅ Permissões granulares

## 📡 Endpoints da API

### Autenticação
- `POST /api/login/` - Login e obtenção de token
- `POST /api/usuarios/logout/` - Logout

### Gestão de Aparelhos
- `GET /api/gestao/aparelhos/` - Listar aparelhos do usuário
- `POST /api/gestao/aparelhos/` - Criar novo aparelho
- `GET /api/gestao/aparelhos/{id}/` - Detalhes do aparelho
- `PUT /api/gestao/aparelhos/{id}/` - Atualizar aparelho
- `DELETE /api/gestao/aparelhos/{id}/` - Deletar aparelho

### Análises
- `GET /api/gestao/analises/` - Análises de consumo do usuário

## 🧪 Testes

### Testes Automatizados
```bash
# Executar todos os testes
python manage.py test

# Executar com visualização
python run_visual_tests.py

# Ou usar o script batch (Windows)
executar_testes.bat
```

### Testes no Postman
1. Importe a coleção: `postman/collection.json`
2. Configure o environment: `postman/environment_local.json`
3. Execute os testes de segurança: `postman/teste_relacionamento.json`

## 🛡️ Segurança

- Autenticação obrigatória para todas as operações
- Usuários só podem ver/editar seus próprios dados
- Tokens seguros para autenticação
- Validação de permissões em todas as operações

## 🏗️ Estrutura do Projeto

```
projetoBack/
├── core/                 # Configurações Django
├── gestao/              # App principal (aparelhos/análises)
├── usuarios/            # App de usuários e autenticação
├── postman/             # Coleções de teste Postman
├── create_user.py       # Script para criar usuários
├── manage.py           # Gerenciador Django
└── requirements.txt    # Dependências
```

## 💡 Como Usar

1. **Faça login** para obter o token
2. **Adicione aparelhos** com consumo, tempo de uso e dias
3. **Visualize análises** automáticas de consumo e custo
4. **Gerencie seus dados** com segurança

## 🔍 Exemplo de Uso

```json
// Login
POST /api/login/
{
  "username": "testuser",
  "password": "test123"
}

// Criar aparelho
POST /api/gestao/aparelhos/
{
  "aparelho": "Geladeira",
  "consumo": "150",
  "tempo": "24",
  "dias_de_uso": 30
}
```

## 🐛 Troubleshooting

- **Erro de migração**: Execute `python manage.py migrate`
- **Usuários não existem**: Execute `python create_user.py`
- **Porta ocupada**: Mude a porta com `python manage.py runserver 8001`
- **Dependências**: Reinstale com `pip install -r requirements.txt`