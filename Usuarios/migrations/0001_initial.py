
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Carro",
            fields=[
                (
                    "placa",
                    models.CharField(
                        max_length=10, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "nombre_conductor",
                    models.CharField(
                        max_length=150, verbose_name="Nombre del conductor"
                    ),
                ),
                ("Marca", models.CharField(max_length=50)),
                ("color", models.CharField(max_length=20)),
                (
                    "telefono_conductor",
                    models.CharField(
                        max_length=10,
                        unique=True,
                        verbose_name="Teléfono del conductor",
                    ),
                ),
                (
                    "estado",
                    models.BooleanField(default=True, verbose_name="Estado del carro"),
                ),
            ],
            options={"db_table": "carros",},
        ),
        migrations.CreateModel(
            name="Hijo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nombres",
                    models.CharField(max_length=15, verbose_name="Nombre del hijo"),
                ),
                (
                    "apellidos",
                    models.CharField(max_length=25, verbose_name="Apellido del hijo"),
                ),
                ("latitud", models.FloatField(verbose_name="latitud donde vive")),
                ("longitud", models.FloatField(verbose_name="longitud donde vive")),
                ("posicion", models.IntegerField(verbose_name="Posicion del hijo")),
                (
                    "estado",
                    models.BooleanField(default=True, verbose_name="Estado del viaje"),
                ),
                (
                    "placa",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Usuarios.carro",
                    ),
                ),
            ],
            options={"db_table": "hijos",},
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "usuario",
                    models.CharField(
                        max_length=15, unique=True, verbose_name="Usuario"
                    ),
                ),
                (
                    "nombres",
                    models.CharField(max_length=15, verbose_name="Nombre de usuario"),
                ),
                (
                    "apellidos",
                    models.CharField(max_length=25, verbose_name="Apellido de usuario"),
                ),
                (
                    "telefono",
                    models.CharField(
                        max_length=10,
                        validators=[django.core.validators.MinLengthValidator(10)],
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Correo Electrónico"
                    ),
                ),
                (
                    "estado",
                    models.BooleanField(
                        default=True, verbose_name="Estado del usuario"
                    ),
                ),
                ("administrador", models.BooleanField(default=False)),
                ("hijos", models.ManyToManyField(to="Usuarios.hijo")),
            ],
            options={"db_table": "usuarios",},
        ),
    ]
