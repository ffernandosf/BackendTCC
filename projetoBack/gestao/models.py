from django.db import models
from datetime import timedelta

class Gestao (models.Model):
    aparelho = models.CharField(max_length=255, blank=False)
    consumo = models.CharField(max_length=20, blank=False)
    tempo = models.CharField(max_length=100)
    dias_de_uso = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.aparelho
