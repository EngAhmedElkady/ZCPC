<<<<<<< HEAD
# Generated by Django 3.2.12 on 2022-05-07 13:58
=======
# Generated by Django 3.2.12 on 2022-05-09 19:08
>>>>>>> 103fa7cffc6de0255bbd86814a7405470d4aa4b3

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communnity', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communnity',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
