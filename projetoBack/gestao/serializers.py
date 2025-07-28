from rest_framework import serializers
from .models import Gestao, Analise

class GestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestao
        fields = ['id', 'aparelho', 'consumo', 'tempo', 'dias_de_uso', 'usuario']

class AnaliseSerializer(serializers.ModelSerializer):
    gestao = GestaoSerializer(read_only=True)
    class Meta:
        model = Analise
        fields = ['gestao', 'consumo_mensal_kwh', 'custo_mensal_reais']