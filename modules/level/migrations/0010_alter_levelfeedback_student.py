# Generated by Django 3.2.12 on 2022-06-12 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('level', '0009_rename_user_levelfeedback_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='levelfeedback',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='level.student'),
        ),
    ]