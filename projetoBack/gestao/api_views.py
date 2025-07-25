from rest_framework import viewsets, permissions
from .models import Gestao, Analise
from .serializers import GestaoSerializer, AnaliseSerializer

class GestaoViewSet(viewsets.ModelViewSet):
    queryset = Gestao.objects.all()
    serializer_class = GestaoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class AnaliseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Analise.objects.select_related('gestao').all()
    serializer_class = AnaliseSerializer
    permission_classes = [permissions.AllowAny]