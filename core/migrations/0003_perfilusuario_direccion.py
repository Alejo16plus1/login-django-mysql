# Generated by Django 5.1.3 on 2024-12-02 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_perfilusuario_nacionalidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='direccion',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
