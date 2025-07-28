from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as authtoken_views
from usuarios.test_login import login_view
from usuarios.simple_login import simple_login
from gestao import views as gestao_views # Importe as views de gestao

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # --- ROTAS DA INTERFACE WEB ---
    path("", gestao_views.login_view, name="login"), 
    path("gestao/", include("gestao.urls")),
    path("usuarios/", include(("usuarios.urls", "usuarios"), namespace="usuarios_web")),
    
    # --- ROTAS DA API ---
    path("api/usuarios/", include("usuarios.urls")),
    path("api/gestao/", include(("gestao.urls", "gestao"), namespace="api_gestao")),
    path("api/login/", login_view),
    path("api/auth/login/", simple_login),
]