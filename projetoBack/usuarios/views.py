from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    
    # Define permissões. Para manter como antes (qualquer um pode editar),
    # usamos AllowAny. Em um app real, você usaria IsAdminUser.
    permission_classes = [permissions.AllowAny] 

    def get_serializer_class(self):
        """
        Retorna um serializer diferente para a ação de 'create'.
        Isso garante que a senha seja tratada corretamente (hashed).
        """
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer