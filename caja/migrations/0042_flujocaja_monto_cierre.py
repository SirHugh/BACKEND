# Generated by Django 5.0.6 on 2024-08-03 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0041_alter_flujocaja_monto_flujocaja'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujocaja',
            name='monto_cierre',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]