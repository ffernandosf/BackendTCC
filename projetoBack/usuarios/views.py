from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def gerenciar_usuarios(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        
        return redirect('gerenciar_usuarios')

    usuarios = User.objects.all().order_by('id')
    return render(request, 'usuarios/crud.html', {'usuarios': usuarios})


def atualizar_usuario(request, id):
   
    if request.method == 'POST':
        
        usuario = get_object_or_404(User, id=id)
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        
        password = request.POST.get('password')
        if password:
            usuario.set_password(password)
        
        usuario.save()


    return redirect('gerenciar_usuarios')


def deletar_usuario(request, id):
    # Encontra o usuário para deletar
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    
    # Redireciona de volta para a página de gerenciamento
    return redirect('gerenciar_usuarios')