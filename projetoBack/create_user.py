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

except Exception as e:
    print(f"❌ Erro: {e}")
    print("Execute: python manage.py migrate")