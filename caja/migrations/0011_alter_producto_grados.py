# Generated by Django 5.0.6 on 2024-06-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0016_periodo'),
        ('caja', '0010_alter_pagoventa_id_comprobante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='grados',
            field=models.ManyToManyField(blank=True, null=True, related_name='productos', to='academico.grado'),
        ),
    ]
