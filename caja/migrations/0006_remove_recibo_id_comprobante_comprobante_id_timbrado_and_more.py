# Generated by Django 5.0.6 on 2024-05-30 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0005_alter_producto_es_mensual'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recibo',
            name='id_comprobante',
        ),
        migrations.AddField(
            model_name='comprobante',
            name='id_timbrado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='caja.timbrado'),
        ),
        migrations.AddField(
            model_name='comprobante',
            name='nro_factura',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Factura',
        ),
        migrations.DeleteModel(
            name='Recibo',
        ),
    ]