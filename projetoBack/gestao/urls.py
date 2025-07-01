from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("gestao/", views.exec_gestao, name="exec_gestao"),
    path('deletar_aparelho/<int:id>', views.deletar_aparelho, name="deletar_aparelho"),
    path('atualizar_aparelho/<int:id>', views.atualizar_aparelho, name="atualizar_aparelho"),
    path('logout/', views.logout_view, name="logout"),
]