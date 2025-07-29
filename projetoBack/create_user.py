import os
import django

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token

    # Criar usuário comum
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@test.com',
            'is_staff': False,
            'is_active': True
        }
    )

    if created:
        user.set_password('test123')
        user.save()
        Token.objects.get_or_create(user=user)
        print("✓ Usuário criado: testuser / test123")
    else:
        print("⚠ Usuário já existe: testuser / test123")

    # Criar user1 para testes de segurança
    user1, created = User.objects.get_or_create(
        username='user1',
        defaults={
            'email': 'user1@test.com',
            'is_staff': False,
            'is_active': True
        }
    )

    if created:
        user1.set_password('test123')
        user1.save()
        Token.objects.get_or_create(user=user1)
        print("✓ Usuário criado: user1 / test123")
    else:
        print("⚠ Usuário já existe: user1 / test123")

    # Criar user2 para testes de segurança
    user2, created = User.objects.get_or_create(
        username='user2',
        defaults={
            'email': 'user2@test.com',
            'is_staff': False,
            'is_active': True
        }
    )

    if created:
        user2.set_password('test123')
        user2.save()
        Token.objects.get_or_create(user=user2)
        print("✓ Usuário criado: user2 / test123")
    else:
        print("⚠ Usuário já existe: user2 / test123")

except Exception as e:
    print(f"❌ Erro: {e}")
    print("Execute: python manage.py migrate")