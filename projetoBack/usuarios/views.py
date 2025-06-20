from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

def gerenciar_usuarios(request):
    # Se o método for POST, significa que um novo usuário está sendo criado
    if request.method == 'POST':
        # Pega os dados do formulário de criação
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Cria o novo usuário
        # O set_password é importante para criptografar a senha
        if username and email and password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        
        # Redireciona para a mesma página para limpar o formulário e mostrar a lista atualizada
        return redirect('gerenciar_usuarios')

    # Se o método for GET, apenas busca todos os usuários e exibe a página
    usuarios = User.objects.all().order_by('id')
    return render(request, 'usuarios/crud.html', {'usuarios': usuarios})


def atualizar_usuario(request, id):
    # Esta view só deve aceitar POST
    if request.method == 'POST':
        # Encontra o usuário pelo ID ou retorna um erro 404 se não existir
        usuario = get_object_or_404(User, id=id)
        
        # Pega os dados do formulário de atualização da tabela
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        
        # Atualiza a senha apenas se uma nova for digitada
        password = request.POST.get('password')
        if password:
            usuario.set_password(password)
        
        usuario.save()

    # Redireciona de volta para a página de gerenciamento
    return redirect('gerenciar_usuarios')


def deletar_usuario(request, id):
    # Encontra o usuário para deletar
    usuario = get_object_or_404(User, id=id)
    usuario.delete()
    
    # Redireciona de volta para a página de gerenciamento
    return redirect('gerenciar_usuarios')