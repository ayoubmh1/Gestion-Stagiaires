# Generated by Django 5.0.6 on 2024-09-05 20:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stagiaires', '0002_remove_stagiaire_date_de_creation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('absent', 'Absent'), ('retard', 'Retard'), ('quitter', 'Quitter le stage')], max_length=20)),
                ('stagiaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stagiaires.stagiaire')),
            ],
        ),
    ]
