# Generated by Django 2.2.15 on 2020-09-30 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0007_studentchoiceanswer_is_answered'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentessayanswer',
            name='is_answered',
            field=models.BooleanField(default=False),
        ),
    ]