from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views
from usuarios.test_login import login_view
from gestao import views as gestao_views # Importe as views de gestao

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- ROTAS DA API ---
    path("api/usuarios/", include("usuarios.urls")),
    path("api/gestao/", include("gestao.urls")),
    path("api/login/", login_view),

    # --- ROTAS DA INTERFACE WEB ---
    # A rota raiz agora aponta para a view de login
    path("", gestao_views.login_view, name="login"), 
    
    # A rota /gestao/ agora leva para as URLs do app de gestão
    # Acessível apenas após o login, graças ao @login_required na view
    path("gestao/", include("gestao.urls")),
]