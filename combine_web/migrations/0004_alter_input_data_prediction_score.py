# Generated by Django 4.2.6 on 2023-10-08 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('combine_web', '0003_alter_input_data_prediction_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_data',
            name='prediction_score',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
        ),
    ]
