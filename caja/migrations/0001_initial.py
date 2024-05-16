# Generated by Django 5.0.3 on 2024-05-12 15:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academico', '0015_rename_alumno_responsable_id_alumno_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=254, null=True)),
                ('tipo', models.CharField(choices=[('PR', 'PRODUCTO'), ('AR', 'ARANCEL'), ('AC', 'ACTIVIDAD')], max_length=2)),
                ('es_activo', models.BooleanField()),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('precio', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timbrado',
            fields=[
                ('id_timbrado', models.AutoField(primary_key=True, serialize=False)),
                ('nro_timbrado', models.IntegerField()),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('es_activo', models.BooleanField()),
                ('numero_inicial', models.IntegerField()),
                ('numero_final', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Arancel',
            fields=[
                ('id_arancel', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_vencimiento', models.DateField()),
                ('nro_cuota', models.IntegerField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('es_activo', models.BooleanField()),
                ('id_matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.matricula')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id_factura', models.AutoField(primary_key=True, serialize=False)),
                ('nro_factura', models.IntegerField()),
                ('fecha', models.DateField()),
                ('tipo_pago', models.CharField(max_length=50)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.cliente')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_timbrado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.timbrado')),
            ],
        ),
    ]