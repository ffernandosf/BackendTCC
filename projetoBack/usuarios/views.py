from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
        
    def get_queryset(self):
        # Usuários podem ver apenas seus próprios dados, admins veem todos
        if self.request.user.is_staff:
            return User.objects.all().order_by('-date_joined')
        else:
            return User.objects.filter(id=self.request.user.id)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def meus_dados(request):
    """View para exibir e editar dados do usuário logado"""
    if request.method == 'POST':
        # Atualizar dados do usuário
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Atualizar senha se fornecida
        new_password = request.POST.get('password')
        if new_password:
            user.set_password(new_password)
        
        user.save()
        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('/gestao/')
    
    return render(request, 'usuarios/meus_dados.html', {'user': request.user})