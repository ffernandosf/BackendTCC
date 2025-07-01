from rest_framework import serializers
from .models import Gestao, Analise

class GestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestao
        fields = ['id', 'aparelho', 'consumo', 'tempo', 'dias_de_uso']

class AnaliseSerializer(serializers.ModelSerializer):
    aparelho = serializers.CharField(source='gestao.aparelho', read_only=True)
    
    class Meta:
        model = Analise
        fields = ['aparelho', 'consumo_mensal_kwh', 'custo_mensal_reais']

class DashboardSerializer(serializers.Serializer):
    aparelhos = GestaoSerializer(many=True)
    analises = AnaliseSerializer(many=True)
    consumo_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    custo_total = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_aparelhos = serializers.IntegerField()