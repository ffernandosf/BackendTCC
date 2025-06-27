# Em gestao/admin.py

from django.contrib import admin
from .models import Gestao, Analise

# Registra os modelos para que apareçam no painel de admin
admin.site.register(Gestao)
admin.site.register(Analise)