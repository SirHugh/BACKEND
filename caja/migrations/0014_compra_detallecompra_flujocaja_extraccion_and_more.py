# Generated by Django 5.0.6 on 2024-06-18 05:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caja', '0013_alter_comprobante_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nro_factura', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id_detalleCompra', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalleCompra', to='caja.compra')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalleCompra', to='caja.producto')),
            ],
        ),
        migrations.CreateModel(
            name='FlujoCaja',
            fields=[
                ('id_flujoCaja', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora_apertura', models.TimeField()),
                ('hora_cierre', models.TimeField()),
                ('monto_apertura', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monto_cierre', models.DecimalField(decimal_places=2, max_digits=10)),
                ('es_activo', models.BooleanField()),
                ('id_usuario', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Extraccion',
            fields=[
                ('id_extraccion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('concepto', models.TextField()),
                ('nro_factura', models.IntegerField(blank=True, null=True)),
                ('id_flujoCaja', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extraccion', to='caja.flujocaja')),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='id_flujoCaja',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compra', to='caja.flujocaja'),
        ),
        migrations.AddField(
            model_name='comprobante',
            name='id_flujoCaja',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='caja.flujocaja'),
        ),
    ]
