# Generated by Django 5.0.3 on 2024-04-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0005_alter_alumno_curso_jardin_alter_alumno_fotocarnet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='curso_jardin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
