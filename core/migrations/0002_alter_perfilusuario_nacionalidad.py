# Generated by Django 5.1.3 on 2024-12-02 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfilusuario',
            name='nacionalidad',
            field=models.CharField(choices=[('VE', 'Venezuela'), ('CO', 'Colombia'), ('AR', 'Argentina'), ('BR', 'Brasil'), ('CL', 'Chile')], max_length=50),
        ),
    ]
