# Generated by Django 3.2.12 on 2023-05-20 10:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Minimum value is 0.'), django.core.validators.MaxValueValidator(100, message='Maximum value is 100.')]),
        ),
    ]
