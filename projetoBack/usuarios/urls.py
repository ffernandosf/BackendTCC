from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Cria um router e registra nossa viewset com ele.
router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

# As URLs da API são determinadas automaticamente pelo router.
urlpatterns = [
    path('', include(router.urls)),
]
