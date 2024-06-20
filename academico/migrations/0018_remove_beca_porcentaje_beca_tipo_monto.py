# Generated by Django 5.0.6 on 2024-06-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0017_beca_arancel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beca',
            name='porcentaje',
        ),
        migrations.AddField(
            model_name='beca',
            name='tipo_monto',
            field=models.IntegerField(choices=[(1, 'MONTO'), (2, 'PORCENTAJE')], default=0),
        ),
    ]