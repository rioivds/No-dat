# Generated by Django 4.2.2 on 2023-07-29 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proa', '0007_alter_alumno_repitio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento'),
        ),
    ]
