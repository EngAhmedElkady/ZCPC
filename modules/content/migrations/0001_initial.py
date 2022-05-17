# Generated by Django 3.2.12 on 2022-05-16 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('level', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contents', to='level.level')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='content.content')),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField()),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to='content.content')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('file', models.FileField(upload_to='files')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='content.content')),
            ],
        ),
    ]
