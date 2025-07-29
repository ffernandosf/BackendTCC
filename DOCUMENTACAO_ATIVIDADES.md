# DOCUMENTAÇÃO DAS ATIVIDADES - PROJETO ECOWATT

## ATIVIDADE 3 - CRUD WEB

### Onde está localizado:
- **Templates**: `gestao/templates/iniciar_gestao.html` e `usuarios/templates/usuarios/crud.html`
- **Views Web**: `gestao/views.py` e `usuarios/views.py`
- **URLs**: Configuradas em `core/urls.py`, `gestao/urls.py` e `usuarios/urls.py`

### Como funciona:

#### Interface de Gestão de Aparelhos (`/gestao/`):
- **CREATE**: Formulário para cadastrar novos aparelhos com campos:
  - Aparelho (nome)
  - Consumo (em Watts)
  - Tempo de uso (horas por dia)
  - Dias de uso (no mês)
- **READ**: Tabela listando todos os aparelhos do usuário logado
- **UPDATE**: Campos editáveis diretamente na tabela com botão "Atualizar"
- **DELETE**: Botão "Deletar" para cada aparelho

#### Interface de Usuários (`/usuarios/meus-dados/`):
- **READ/UPDATE**: Formulário para editar dados pessoais (nome, email, senha)
- Apenas usuários autenticados podem acessar seus próprios dados

#### Funcionalidades Extras:
- **Geolocalização**: Detecta automaticamente a cidade do usuário
- **Análise de Consumo**: Calcula automaticamente consumo mensal em kWh e custo em R$
- **Segurança**: Cada usuário só vê seus próprios dados

---

## ATIVIDADE 4 - CRUD API

### Onde está localizado:
- **API Views**: `gestao/api_views.py` e `usuarios/views.py` (UserViewSet)
- **Serializers**: `gestao/serializers.py` e `usuarios/serializers.py`
- **URLs da API**: Rotas com prefixo `/api/`

### Como funciona:

#### API de Gestão (`/api/gestao/aparelhos/`):
- **GET** `/api/gestao/aparelhos/` - Lista aparelhos do usuário
- **POST** `/api/gestao/aparelhos/` - Cria novo aparelho
- **PUT** `/api/gestao/aparelhos/{id}/` - Atualiza aparelho específico
- **DELETE** `/api/gestao/aparelhos/{id}/` - Remove aparelho

#### API de Análises (`/api/gestao/analises/`):
- **GET** `/api/gestao/analises/` - Lista análises de consumo (somente leitura)

#### API de Usuários (`/api/usuarios/users/`):
- **GET** `/api/usuarios/users/` - Lista usuários (admin vê todos, usuário comum só a si mesmo)
- **POST** `/api/usuarios/users/` - Cria novo usuário
- **PUT** `/api/usuarios/users/{id}/` - Atualiza usuário
- **DELETE** `/api/usuarios/users/{id}/` - Remove usuário

#### Segurança da API:
- Usuários só podem manipular seus próprios dados
- Admins têm acesso completo
- Validação de permissões em todas as operações

---

## ATIVIDADE 5 - AUTH API

### Onde está localizado:
- **Autenticação**: `usuarios/auth_views.py` e `usuarios/simple_login.py`
- **Permissões**: `usuarios/permissions.py`
- **URLs**: `/api/login/`, `/api/usuarios/logout/`, `/api/usuarios/revoke-tokens/`

### Como funciona para autenticar e diferenciar admin de usuário:

#### Sistema de Login:
```python
# Endpoint: POST /api/login/
{
    "username": "usuario",
    "password": "senha"
}

# Resposta:
{
    "token": "abc123...",
    "user_id": 1,
    "username": "usuario",
    "is_staff": false  # true para admin
}
```

#### Diferenciação Admin vs Usuário:

**Usuário Comum (`is_staff: false`)**:
- Só pode ver/editar seus próprios aparelhos
- Não pode acessar dados de outros usuários
- Acesso limitado às próprias análises

**Administrador (`is_staff: true`)**:
- Pode ver todos os aparelhos de todos os usuários
- Pode criar aparelhos para qualquer usuário
- Acesso completo ao sistema via `/admin/`
- Pode gerenciar todos os usuários

#### Autenticação por Token:
- Cada usuário recebe um token único após login
- Token deve ser enviado no header: `Authorization: Token abc123...`
- Tokens podem ser revogados via `/api/usuarios/logout/`

#### Middleware de Segurança:
- Todas as rotas da API exigem autenticação
- Verificação automática de permissões em cada operação
- Proteção contra acesso cruzado entre usuários

---

## ATIVIDADE 6 - ORM

### Como está funcionando o ORM do projeto:

#### Modelos Principais:

**Modelo Gestao** (`gestao/models.py`):
```python
class Gestao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aparelho = models.CharField(max_length=255)
    consumo = models.CharField(max_length=20)  # Watts
    tempo = models.CharField(max_length=100)   # Horas/dia
    dias_de_uso = models.IntegerField()        # Dias/mês
```

**Modelo Analise** (`gestao/models.py`):
```python
class Analise(models.Model):
    gestao = models.OneToOneField(Gestao, on_delete=models.CASCADE, primary_key=True)
    consumo_mensal_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    custo_mensal_reais = models.DecimalField(max_digits=10, decimal_places=2)
```

#### Relacionamentos:
- **User ↔ Gestao**: Um usuário pode ter vários aparelhos (ForeignKey)
- **Gestao ↔ Analise**: Cada aparelho tem uma análise (OneToOneField)

#### Signals Automáticos:
```python
@receiver(post_save, sender=Gestao)
def criar_ou_atualizar_analise(sender, instance, created, **kwargs):
    if created:
        analise = Analise.objects.create(gestao=instance)
        analise.calcular_analise()
    else:
        instance.analise.calcular_analise()
```

#### Funcionalidades do ORM:
- **Cálculo Automático**: Quando um aparelho é criado/atualizado, a análise é recalculada automaticamente
- **Queries Otimizadas**: Uso de `select_related()` para evitar N+1 queries
- **Agregações**: Cálculo de totais usando `Sum()` e `aggregate()`
- **Filtros por Usuário**: Todas as queries filtram por usuário logado

#### Migrations:
- `0001_initial.py` - Criação inicial das tabelas
- `0002_alter_gestao_tempo.py` - Alteração no campo tempo
- `0003_analise.py` - Adição da tabela de análises
- `0004_gestao_usuario.py` - Adição do relacionamento com usuário

---

## ATIVIDADE 7 - TESTES API

### Testes do Postman:

#### Localização: `postman/collection.json`

**Estrutura da Coleção**:

1. **Auth** - Testes de Autenticação:
   - Login com credenciais válidas
   - Logout com token
   - Salvamento automático de tokens

2. **Gestão** - CRUD de Aparelhos:
   - Listar aparelhos do usuário
   - Criar novo aparelho
   - Atualizar aparelho existente
   - Deletar aparelho

3. **Testes de Segurança** - Validação de Permissões:
   - Setup com 2 usuários diferentes
   - Teste de exclusão cruzada (deve falhar)
   - Validação de que usuários só acessam próprios dados

**Scripts de Teste Automático**:
```javascript
// Exemplo de script que salva token automaticamente
if (pm.response.code === 200) {
    const response = pm.response.json();
    pm.environment.set('token', response.token);
    pm.test('Token saved', function () {
        pm.expect(response.token).to.not.be.undefined;
    });
}
```

**Variáveis de Ambiente**:
- `base_url`: http://127.0.0.1:8000
- `token`: Token de autenticação atual
- `aparelho_id`: ID do aparelho para testes

### Testes do PyCharm (Django Tests):

#### Localização: `usuarios/tests.py`

**Classes de Teste**:

1. **CustomAuthTokenTest** - Testes de Login:
   - Login com usuário comum
   - Login com admin
   - Credenciais inválidas
   - Campos obrigatórios
   - Reutilização de tokens

2. **LogoutTest** - Testes de Logout:
   - Logout com sucesso
   - Logout sem autenticação
   - Token inválido

3. **RevokeTokensTest** - Revogação de Tokens:
   - Revogar token atual
   - Revogar todos os tokens
   - Sem autenticação

4. **UserModelTest** - Modelo de Usuário:
   - Criação de usuário comum
   - Criação de superusuário
   - Validação de senhas

5. **TokenModelTest** - Modelo de Token:
   - Criação de token
   - Unicidade de tokens
   - Get or create pattern

**Execução dos Testes**:
```bash
# Executar todos os testes
python manage.py test

# Executar testes específicos
python manage.py test usuarios.tests.CustomAuthTokenTest

# Com coverage
python -m pytest --cov=usuarios
```

**Configuração de Teste** (`pytest.ini`):
```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = core.settings
python_files = tests.py test_*.py *_tests.py
```

### Diferenças entre os Testes:

**Postman**:
- Testa a API como um cliente externo
- Valida respostas HTTP reais
- Testa fluxos completos de usuário
- Ideal para testes de integração

**PyCharm/Django Tests**:
- Testa unidades de código isoladamente
- Usa banco de dados de teste
- Mais rápido para desenvolvimento
- Ideal para testes unitários e de modelo