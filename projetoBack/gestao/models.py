from django.db import models
from datetime import timedelta
from django.dispatch import receiver
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver

class Gestao (models.Model):
    aparelho = models.CharField(max_length=255, blank=False)
    consumo = models.CharField(max_length=20, blank=False)
    tempo = models.CharField(max_length=100)
    dias_de_uso = models.IntegerField(default=0, null=False, blank=False)
   

    def __str__(self):
        return self.aparelho

class Analise(models.Model):
    # Relacionamento um-para-um com a tabela Gestao
    gestao = models.OneToOneField(Gestao, on_delete=models.CASCADE, primary_key=True)
    
    # Campos calculados para a análise
    consumo_mensal_kwh = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    custo_mensal_reais = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Análise de {self.gestao.aparelho}"

    def calcular_analise(self):
        """
        Calcula o consumo e o custo mensal com base nos dados de Gestao.
        """
        try:
            # Defina o preço do kWh da sua região
            TARIFA_KWH = Decimal("0.92") # Exemplo: R$ 0,92 por kWh

            # Converte os campos de texto para Decimal para o cálculo
            potencia_watts = Decimal(self.gestao.consumo)
            horas_por_dia = Decimal(self.gestao.tempo)
            dias_por_mes = Decimal(self.gestao.dias_de_uso)

            # 1. Converte potência de Watts para kilowatts (kW)
            potencia_kw = potencia_watts / 1000
            
            # 2. Calcula o consumo diário em kWh
            consumo_diario_kwh = potencia_kw * horas_por_dia
            
            # 3. Calcula o consumo mensal em kWh
            self.consumo_mensal_kwh = consumo_diario_kwh * dias_por_mes
            
            # 4. Calcula o custo mensal
            self.custo_mensal_reais = self.consumo_mensal_kwh * TARIFA_KWH
            
            self.save()

        except (ValueError, TypeError):
            # Lida com casos onde 'consumo' ou 'tempo' não são números válidos
            print(f"Não foi possível calcular a análise para {self.gestao.aparelho} devido a dados inválidos.")


# --- Signal para automatizar a análise ---
# Este código será executado sempre que um objeto Gestao for salvo (novo ou atualizado)
@receiver(post_save, sender=Gestao)
def criar_ou_atualizar_analise(sender, instance, created, **kwargs):
    if created:
        # Se um novo Gestao foi criado, cria a análise correspondente
        analise = Analise.objects.create(gestao=instance)
        analise.calcular_analise()
    else:
        # Se um Gestao existente foi atualizado, recalcula a análise
        instance.analise.calcular_analise()