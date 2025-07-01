from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Gestao, Analise
from django.db.models import Sum
from decimal import Decimal
def login_view(request):
    if request.user.is_authenticated:
        return redirect('exec_gestao')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('exec_gestao')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def exec_gestao(request):
    # O bloco POST para criar um novo aparelho continua o mesmo.
    # Ele cria o objeto Gestao, o signal cria a Análise, e depois redireciona.
    if request.method == 'POST':
        aparelho = request.POST.get('aparelho')
        consumo = request.POST.get('consumo')
        tempo = request.POST.get('tempo')
        dias_de_consumo = request.POST.get('dias_de_uso')

        # Usar .create() é uma forma mais curta e limpa
        Gestao.objects.create(
            aparelho=aparelho,
            consumo=consumo,
            tempo=tempo,
            dias_de_uso=dias_de_consumo,
        )
        return redirect('exec_gestao')
    
    # --- LÓGICA CORRIGIDA PARA EXIBIR OS DADOS ---
    # Este bloco agora será executado em qualquer requisição GET
    # (seja no primeiro acesso à página ou após um redirect).

    # Busca todos os aparelhos para a primeira tabela
    aparelhos = Gestao.objects.order_by('id')

    # Busca todas as análises para a segunda tabela
    # .select_related('gestao') otimiza a busca, evitando novas consultas ao banco dentro do loop do template
    analises = Analise.objects.select_related('gestao').all()

    # Calcula os totais de consumo e custo a partir das análises
    totais = analises.aggregate(
        consumo_total=Sum('consumo_mensal_kwh'),
        custo_total=Sum('custo_mensal_reais')
    )

    # Prepara o dicionário de contexto com TODOS os dados que o template precisa
    context = {
        'aparelhos': aparelhos,
        'analises': analises,
        # Se não houver aparelhos, os totais serão 'None'. Usamos 'or' para garantir que seja 0.
        'consumo_total': totais['consumo_total'] or Decimal('0.00'),
        'custo_total': totais['custo_total'] or Decimal('0.00')
    }

    # Renderiza o template com o contexto completo
    return render(request, "iniciar_gestao.html", context)

@login_required
def atualizar_aparelho(request, id):
    # Esta view já estava correta. Ao salvar, o signal recalcula a análise.
    # O redirect para 'exec_gestao' garante que a página seja recarregada com os novos dados.
    aparelho_a_atualizar = get_object_or_404(Gestao, id=id)

    if request.method == "POST":
        aparelho_a_atualizar.aparelho = request.POST.get('aparelho')
        aparelho_a_atualizar.consumo = request.POST.get('consumo')
        aparelho_a_atualizar.tempo = request.POST.get('tempo')
        aparelho_a_atualizar.dias_de_uso = request.POST.get('dias_de_uso')
        
        aparelho_a_atualizar.save() # Dispara o signal que atualiza a análise

    return redirect('exec_gestao')

@login_required
def deletar_aparelho(request, id):
    # Esta view já estava correta.
    # Como o modelo Analise tem 'on_delete=models.CASCADE', a análise associada é deletada automaticamente.
    aparelho = get_object_or_404(Gestao, id=id)
    aparelho.delete()
    return redirect('exec_gestao')