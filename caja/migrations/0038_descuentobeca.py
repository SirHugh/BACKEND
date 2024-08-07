# Generated by Django 5.0.6 on 2024-07-21 23:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0022_alter_periodo_options'),
        ('caja', '0037_formapago_comprobante_id_formapago'),
    ]

    operations = [
        migrations.CreateModel(
            name='DescuentoBeca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_arancel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caja.arancel')),
                ('id_beca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academico.beca')),
            ],
        ),
    ]
