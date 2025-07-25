from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .auth_views import logout_view, revoke_tokens
from .simple_login import simple_login
from .test_login import login_view

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', simple_login, name='api_login'),
    path('test-login/', login_view, name='test_login'),
    path('logout/', logout_view, name='api_logout'),
    path('revoke-tokens/', revoke_tokens, name='revoke_tokens'),
]
