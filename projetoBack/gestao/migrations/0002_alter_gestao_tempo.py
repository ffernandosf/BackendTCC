# Generated by Django 4.2.22 on 2025-06-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gestao',
            name='tempo',
            field=models.CharField(max_length=100),
        ),
    ]
