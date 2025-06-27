
from django.contrib import admin
from django.urls import path, include

# Este é o arquivo de URLs principal do seu projeto.
# A responsabilidade dele é direcionar as requisições para os apps corretos.

urlpatterns = [
    # 1. Rota para a interface de administração do Django.
    # Deve haver apenas uma.
    path("admin/", admin.site.urls),

    # 2. Rota para a API do app de usuários.
    # Todas as URLs definidas em 'usuarios.urls' serão prefixadas com 'api/usuarios/'.
    # Exemplo: http://127.0.0.1:8000/api/usuarios/
    path('api/usuarios/', include('usuarios.urls')),

    # 3. Rota para o app de gestão.
    # Como o caminho é vazio (""), as URLs de 'gestao.urls'
    # serão acessadas a partir da raiz do site.
    # Exemplo: http://127.0.0.1:8000/
    path("", include('gestao.urls')),
]




