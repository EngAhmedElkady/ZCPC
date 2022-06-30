# Generated by Django 3.2.12 on 2022-06-15 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0012_alter_levelteamfeedback_team_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levelteamfeedback',
            name='stars',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
    ]