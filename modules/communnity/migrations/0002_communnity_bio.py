# Generated by Django 3.2.12 on 2022-05-22 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communnity',
            name='bio',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
