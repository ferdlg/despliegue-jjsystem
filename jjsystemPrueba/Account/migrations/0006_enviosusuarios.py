# Generated by Django 5.0 on 2024-04-04 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0005_delete_actividadescronogramatecnicos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnviosUsuarios',
            fields=[
                ('emailCliente', models.EmailField(max_length=120)),
                ('nombreCliente', models.CharField(max_length=50)),
                ('apellidoCliente', models.CharField(max_length=50)),
                ('numeroDocumentoCliente', models.BigIntegerField(primary_key=True, serialize=False)),
                ('idEnvio', models.IntegerField()),
                ('direccionEnvio', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'EnviosUsuarios',
                'managed': False,
            },
        ),
    ]