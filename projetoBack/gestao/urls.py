# Em gestao/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # A rota "" dentro de /gestao/ agora é a página principal
    path("", views.exec_gestao, name="pagina_gestao"),
    
    path("deletar/<int:aparelho_id>/", views.deletar_aparelho, name="deletar_aparelho"),
    path("atualizar/<int:aparelho_id>/", views.atualizar_aparelho, name="atualizar_aparelho"),
    path("geolocation/", views.get_cep_from_coords, name="geolocation"),
]