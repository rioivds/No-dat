# Generated by Django 4.2.3 on 2023-08-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proa', '0011_alumno_usuario_profesor_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumno',
            name='inasistencias',
            field=models.FloatField(null=True, verbose_name='Inasistencias'),
        ),
    ]