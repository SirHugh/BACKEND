# Generated by Django 5.0.6 on 2024-08-03 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0039_producto_codigo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flujocaja',
            old_name='monto_cierre',
            new_name='monto_flujoCaja',
        ),
    ]