# Generated by Django 5.0.6 on 2024-06-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academico', '0016_periodo'),
        ('caja', '0013_alter_comprobante_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='beca',
            name='arancel',
            field=models.ManyToManyField(default=0, related_name='beca', to='caja.producto'),
        ),
    ]
