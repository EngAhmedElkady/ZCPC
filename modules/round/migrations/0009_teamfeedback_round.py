# Generated by Django 3.2.12 on 2022-04-30 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('round', '0008_auto_20220430_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamfeedback',
            name='round',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='round.roundteam'),
            preserve_default=False,
        ),
    ]
