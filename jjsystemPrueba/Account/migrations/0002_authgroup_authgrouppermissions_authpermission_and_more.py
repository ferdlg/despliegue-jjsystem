# Generated by Django 5.0.1 on 2024-03-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CotizacionesProductos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cotizaciones_productos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CotizacionesServicios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'cotizaciones_servicios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DetalleEnviosVentas',
            fields=[
                ('idenvio', models.IntegerField(primary_key=True, serialize=False)),
                ('direccionenvio', models.CharField(blank=True, max_length=255, null=True)),
                ('detallesventa', models.CharField(blank=True, max_length=255, null=True)),
                ('tecnicoasignado', models.IntegerField(blank=True, null=True)),
                ('numerodocumento', models.CharField(blank=True, max_length=255, null=True)),
                ('fechaventa', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'detalle_envios_ventas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Historialcotizaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechacreada', models.DateTimeField(blank=True, db_column='fechaCreada', null=True)),
                ('fechaactualizacion', models.DateTimeField(blank=True, db_column='fechaActualizacion', null=True)),
            ],
            options={
                'db_table': 'historialcotizaciones',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Historialpqrsfportipoestado',
            fields=[
                ('idregistro', models.AutoField(db_column='idregistro', primary_key=True, serialize=False)),
                ('idtipopqrsf', models.IntegerField(blank=True, db_column='idtipopqrsf', null=True)),
                ('idestadopqrsf', models.IntegerField(blank=True, db_column='idestadopqrsf', null=True)),
                ('fecharegistro', models.DateTimeField(blank=True, db_column='fechaRegistro', null=True)),
            ],
            options={
                'db_table': 'historialpqrsfportipoestado',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='DetallesEnviosVentas',
        ),
    ]
