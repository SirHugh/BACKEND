# Generated by Django 5.0.3 on 2024-04-01 19:50

import academico.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0004_alter_alumno_curso_jardin_alter_alumno_fotocarnet_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='curso_jardin',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='fotocarnet',
            field=models.ImageField(blank=True, null=True, upload_to=academico.models.upload_to),
        ),
    ]
