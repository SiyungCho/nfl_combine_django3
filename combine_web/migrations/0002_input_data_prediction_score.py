# Generated by Django 4.2.6 on 2023-10-08 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('combine_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='input_data',
            name='prediction_score',
            field=models.FloatField(default=0.0),
        ),
    ]