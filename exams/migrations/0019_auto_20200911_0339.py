# Generated by Django 2.2.15 on 2020-09-11 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0018_auto_20200911_0331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='time_quiz',
            new_name='time',
        ),
    ]
