
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gestao, Analise  
from django.db.models import Sum     
from decimal import Decimal         


def exec_gestao(request):
   
    if request.method == 'POST':
        aparelho = request.POST.get('aparelho')
        consumo = request.POST.get('consumo')
        tempo = request.POST.get('tempo')
        dias_de_consumo = request.POST.get('dias_de_uso')

      
        Gestao.objects.create(
            aparelho=aparelho,
            consumo=consumo,
            tempo=tempo,
            dias_de_uso=dias_de_consumo,
        )
        return redirect('exec_gestao')
    
   

    # Busca todos os aparelhos para a primeira tabela
    aparelhos = Gestao.objects.order_by('id')

    analises = Analise.objects.select_related('gestao').all()

    # Calcula os totais de consumo e custo a partir das análises
    totais = analises.aggregate(
        consumo_total=Sum('consumo_mensal_kwh'),
        custo_total=Sum('custo_mensal_reais')
    )

   
    context = {
        'aparelhos': aparelhos,
        'analises': analises,
      
        'consumo_total': totais['consumo_total'] or Decimal('0.00'),
        'custo_total': totais['custo_total'] or Decimal('0.00')
    }

    # Renderiza o template com o contexto completo
    return render(request, "iniciar_gestao.html", context)


def atualizar_aparelho(request, id):
   
    aparelho_a_atualizar = get_object_or_404(Gestao, id=id)

    if request.method == "POST":
        aparelho_a_atualizar.aparelho = request.POST.get('aparelho')
        aparelho_a_atualizar.consumo = request.POST.get('consumo')
        aparelho_a_atualizar.tempo = request.POST.get('tempo')
        aparelho_a_atualizar.dias_de_uso = request.POST.get('dias_de_uso')
        
        aparelho_a_atualizar.save() 

    return redirect('exec_gestao')


def deletar_aparelho(request, id):

    aparelho = get_object_or_404(Gestao, id=id)
    aparelho.delete()
    return redirect('exec_gestao')