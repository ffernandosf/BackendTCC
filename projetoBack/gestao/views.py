from django.shortcuts import render, redirect, get_object_or_404
from .models import Gestao

def exec_gestao(request):
    if request.method == 'GET':
      aparelhos= Gestao.objects.all()
      return render(request, "iniciar_gestao.html", {'aparelhos': aparelhos})
   
    elif request.method == 'POST':
       aparelho =request.POST.get('aparelho')
       consumo = request.POST.get('consumo')
       tempo = request.POST.get('tempo')
       dias_de_consumo = request.POST.get('dias_de_uso')

       gestao = Gestao(
          aparelho=aparelho,
          consumo=consumo,
          tempo=tempo,   
          dias_de_uso=dias_de_consumo,
       )

       gestao.save()

       return redirect('exec_gestao')
    



def deletar_aparelho (request, id):
   aparelho = get_object_or_404(Gestao, id=id)
   aparelho.delete()
   return redirect('exec_gestao')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Gestao

def atualizar_aparelho(request, id):
    aparelho_a_atualizar = get_object_or_404(Gestao, id=id)

    if request.method == "POST":
        nome_do_form = request.POST.get('aparelho')
        consumo_do_form = request.POST.get('consumo')
        tempo_do_form = request.POST.get('tempo')
        dias_do_form = request.POST.get('dias_de_uso')

        aparelho_a_atualizar.aparelho = nome_do_form
        aparelho_a_atualizar.consumo = consumo_do_form
        aparelho_a_atualizar.tempo = tempo_do_form
        aparelho_a_atualizar.dias_de_uso = dias_do_form
        
        aparelho_a_atualizar.save()

        return redirect('exec_gestao')

    return redirect('exec_gestao')


   
 