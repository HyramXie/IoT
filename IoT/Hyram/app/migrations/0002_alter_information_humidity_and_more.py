# Generated by Django 5.0.6 on 2024-06-28 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='humidity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='information',
            name='moisture',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='information',
            name='temperature',
            field=models.FloatField(),
        ),
    ]
