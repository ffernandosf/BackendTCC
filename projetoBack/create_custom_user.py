import os
import django
import getpass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def create_custom_user():
    """Cria usuário personalizado via input"""
    print("=== Criação de Usuário Personalizado ===")
    
    username = input("Username: ")
    email = input("Email: ")
    first_name = input("Nome: ")
    last_name = input("Sobrenome: ")
    
    # Verificar se é admin
    is_admin = input("É administrador? (s/n): ").lower() == 's'
    
    # Senha
    password = getpass.getpass("Senha: ")
    confirm_password = getpass.getpass("Confirmar senha: ")
    
    if password != confirm_password:
        print("❌ Senhas não coincidem!")
        return
    
    # Criar usuário
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_admin,
            is_superuser=is_admin
        )
        
        # Criar token
        Token.objects.get_or_create(user=user)
        
        user_type = "Admin" if is_admin else "Usuário"
        print(f"✓ {user_type} criado: {username}")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário: {e}")

if __name__ == '__main__':
    create_custom_user()