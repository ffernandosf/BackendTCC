from rest_framework import viewsets, permissions
from .models import Gestao, Analise
from .serializers import GestaoSerializer, AnaliseSerializer

class GestaoViewSet(viewsets.ModelViewSet):
    serializer_class = GestaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        # Para operações de listagem, filtrar por usuário
        if self.action == 'list':
            if self.request.user.is_staff:
                return Gestao.objects.all()
            else:
                return Gestao.objects.filter(usuario=self.request.user)
        
        # Para outras operações (retrieve, update, destroy), retornar todos
        # A verificação de permissão será feita no perform_destroy
        return Gestao.objects.all()

    def perform_create(self, serializer):
        # Admin pode criar para qualquer usuário
        if self.request.user.is_staff:
            # Se não especificar usuário, cria para o admin
            if 'usuario' not in serializer.validated_data:
                serializer.save(usuario=self.request.user)
            else:
                # Admin pode especificar qualquer usuário
                serializer.save()
        else:
            # Usuário comum só pode criar para si mesmo
            serializer.save(usuario=self.request.user)
    
    def perform_destroy(self, instance):
        if instance.usuario != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Você não tem permissão para deletar este aparelho.")
        instance.delete()
        
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.usuario != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Você não tem permissão para atualizar este aparelho.")
        serializer.save()

class AnaliseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnaliseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Analise.objects.select_related('gestao').filter(gestao__usuario=self.request.user)