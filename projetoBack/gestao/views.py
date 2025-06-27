import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Gestao, Analise  
from django.db.models import Sum     
from decimal import Decimal  
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# ... (mantenha suas outras views: exec_gestao, deletar_aparelho, etc.)

def login_view(request):
    if request.method == 'POST':
        usuario_form = request.POST.get('username')
        senha_form = request.POST.get('password')
        
        user = authenticate(request, username=usuario_form, password=senha_form)
        
        if user is not None:
            login(request, user)
            # Altere o redirecionamento para a URL da página de gestão
            return redirect('/gestao/') 
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
            
    return render(request, 'login.html')


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


def get_cep_from_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'erro': 'Latitude e Longitude são obrigatórias'}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return JsonResponse({'erro': 'Latitude e Longitude devem ser números válidos'}, status=400)

    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    headers = {
        'User-Agent': 'GerenciadorGastosEletricos/1.0 (contato@seudominio.com)'  # personalize com seu e-mail
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        address = data.get('address', {})

        # A cidade pode estar em diferentes campos
        cidade = address.get('city') or address.get('town') or address.get('village')

        if cidade:
            return JsonResponse({'cidade': cidade})
        else:
            return JsonResponse({'erro': 'Cidade não encontrada'}, status=404)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'erro': f'Falha na API externa: {e}'}, status=502)



