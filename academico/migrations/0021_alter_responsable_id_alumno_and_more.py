# Generated by Django 5.0.6 on 2024-06-16 03:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0020_alter_responsable_id_alumno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsable',
            name='id_alumno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.alumno'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='id_cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cliente'),
        ),
    ]