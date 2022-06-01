# Generated by Django 3.2.12 on 2022-06-01 13:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('round', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=700, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='round.round')),
            ],
            options={
                'verbose_name': 'level',
                'verbose_name_plural': 'levels',
                'unique_together': {('round', 'name')},
            },
        ),
        migrations.CreateModel(
            name='TeamFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('disc', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamfeedback', to='level.level')),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teamfeedback', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userteamfeedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='level.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='LevelTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('instructor', 'instructor'), ('mentor', 'mentor')], max_length=200)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='level.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'LevelTeam',
                'verbose_name_plural': 'LevelTeams',
            },
        ),
        migrations.CreateModel(
            name='LevelFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('disc', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='level.level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
