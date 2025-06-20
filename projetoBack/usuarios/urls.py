from django.urls import path
from . import views

urlpatterns = [
    # URL para listar e criar usuários (a página principal)
    path('gerenciar/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    
    # URL para processar a atualização de um usuário específico
    path('atualizar/<int:id>/', views.atualizar_usuario, name='atualizar_usuario'),
    
    # URL para deletar um usuário específico
    path('deletar/<int:id>/', views.deletar_usuario, name='deletar_usuario'),
]