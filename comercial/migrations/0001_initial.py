# Generated by Django 5.0.6 on 2024-07-12 03:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('caja', '0036_rename_id_ajustedetalle_bajainventario_id_bajainventario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ControlStock',
            fields=[
                ('id_controlStock', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleControl',
            fields=[
                ('id_detalleControl', models.AutoField(primary_key=True, serialize=False)),
                ('stock', models.IntegerField()),
                ('cantidad_contada', models.IntegerField()),
                ('id_controlStock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercial.controlstock')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.producto')),
            ],
        ),
    ]
