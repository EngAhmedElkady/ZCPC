# Generated by Django 3.2.12 on 2022-04-27 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='round',
            old_name='communnity_id',
            new_name='communnity',
        ),
    ]
