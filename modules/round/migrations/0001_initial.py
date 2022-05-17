# Generated by Django 3.2.12 on 2022-05-16 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communnity', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(max_length=700)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=True)),
                ('communnity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='communnity.communnity')),
            ],
            options={
                'verbose_name': 'Round',
                'verbose_name_plural': 'Rounds',
            },
        ),
    ]
