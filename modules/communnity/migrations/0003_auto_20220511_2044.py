# Generated by Django 3.2.12 on 2022-05-11 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0002_alter_communnity_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='communnity_id',
            new_name='community',
        ),
        migrations.RenameField(
            model_name='team',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddField(
            model_name='communnity',
            name='slug',
            field=models.SlugField(blank=True, max_length=244, null=True),
        ),
    ]
