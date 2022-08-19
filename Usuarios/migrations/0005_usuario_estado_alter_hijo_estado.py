
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Usuarios", "0004_hijo_estado"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="estado",
            field=models.BooleanField(default=True, verbose_name="Estado del usuario"),
        ),
        migrations.AlterField(
            model_name="hijo",
            name="estado",
            field=models.BooleanField(default=True, verbose_name="Estado del viaje"),
        ),
    ]
