from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, meus_dados
from .auth_views import logout_view, revoke_tokens
from .simple_login import simple_login
from .test_login import login_view

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # --- ROTAS WEB ---
    path('meus-dados/', meus_dados, name='meus_dados'),
    
    # --- ROTAS API ---
    path('login/', simple_login, name='api_login'),
    path('test-login/', login_view, name='test_login'),
    path('logout/', logout_view, name='api_logout'),
    path('revoke-tokens/', revoke_tokens, name='revoke_tokens'),
    path('api/', include(router.urls)),
]
