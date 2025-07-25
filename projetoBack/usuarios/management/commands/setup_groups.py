from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@test.com', 'user123')
        self.stdout.write('Setup concluído!')