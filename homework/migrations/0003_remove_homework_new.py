# Generated by Django 2.2.15 on 2020-09-27 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0002_homework_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homework',
            name='new',
        ),
    ]
