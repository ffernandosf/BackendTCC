from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path("exec_gestao/", views.exec_gestao, name="exec_gestao"),
    path("", RedirectView.as_view(pattern_name="exec_gestao", permanent=False), name="home"),
    path('deletar_aparelho/<int:id>', views.deletar_aparelho, name="deletar_aparelho"),
    path('atualizar_aparelho/<int:id>', views.atualizar_aparelho, name="atualizar_aparelho"),
    path('geolocation/', views.get_cep_from_coords, name='get_cep'),
]