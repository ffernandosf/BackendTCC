from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .auth_views import CustomAuthToken, logout_view, revoke_tokens

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', logout_view, name='api_logout'),
    path('revoke-tokens/', revoke_tokens, name='revoke_tokens'),
]
