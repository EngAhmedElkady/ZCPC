# Generated by Django 3.2.12 on 2022-04-24 11:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('round', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoundTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('instructor', 'instructor'), ('mentor', 'mentor')], max_length=200)),
                ('round_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='round.round')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'RoundTeam',
                'verbose_name_plural': 'RoundTeams',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('round_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='round.round')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
    ]