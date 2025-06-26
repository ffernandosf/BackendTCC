from django.urls import path
from . import views

urlpatterns = [
    
    path('gerenciar/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    
    path('atualizar/<int:id>/', views.atualizar_usuario, name='atualizar_usuario'),
    
    
    path('deletar/<int:id>/', views.deletar_usuario, name='deletar_usuario'),
]