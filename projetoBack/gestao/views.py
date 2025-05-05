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


def atualizar_aluno(request, id):
   aparelho = get_object_or_404(Gestao, id=id)

   aparelho =request.POST.get('aparelho')
   consumo = request.POST.get('consumo')
   tempo = request.POST.get('tempo')
   dias_de_consumo = request.POST.get('dias_de_uso')

   aparelho.aparelho = aparelho
   aparelho.consumo = consumo
   aparelho.tempo = tempo
   aparelho.dias_de_consumo = dias_de_consumo

   aparelho.sabe()
   return redirect('exec_gestao')


   
 