from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import GestaoViewSet, AnaliseViewSet

router = DefaultRouter()
router.register(r'aparelhos', GestaoViewSet, basename='gestao')
router.register(r'analises', AnaliseViewSet, basename='analise')

urlpatterns = [
    # --- ROTAS DA INTERFACE WEB ---
    path("", views.exec_gestao, name="pagina_gestao"),
    path("deletar/<int:id>/", views.deletar_aparelho, name="deletar_aparelho"),
    path("atualizar/<int:id>/", views.atualizar_aparelho, name="atualizar_aparelho"),
    path("geolocation/", views.get_cep_from_coords, name="geolocation"),
    
    # --- ROTAS DA API ---
    path('api/', include(router.urls)),
]