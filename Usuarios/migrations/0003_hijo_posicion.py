# Generated by Django 4.1 on 2022-08-09 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Usuarios", "0002_rename_apellido_usuario_apellidos"),
    ]

    operations = [
        migrations.AddField(
            model_name="hijo",
            name="posicion",
            field=models.IntegerField(default=2, verbose_name="Posicion del hijo"),
            preserve_default=False,
        ),
    ]
