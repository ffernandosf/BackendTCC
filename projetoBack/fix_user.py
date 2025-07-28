import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Deletar usuário existente se houver
try:
    user = User.objects.get(username='testuser')
    user.delete()
    print("✓ Usuário antigo removido")
except User.DoesNotExist:
    print("⚠ Usuário não existia")

# Criar novo usuário
user = User.objects.create_user(
    username='testuser',
    email='test@test.com',
    password='test123',
    is_active=True
)

# Criar token
Token.objects.get_or_create(user=user)

print("✓ Usuário criado: testuser / test123")
print(f"✓ Usuário ativo: {user.is_active}")
print(f"✓ Token criado: {user.auth_token.key}")