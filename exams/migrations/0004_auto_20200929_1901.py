# Generated by Django 2.2.15 on 2020-09-29 17:01

import collections
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_studentexam_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentexam',
            name='questions',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=collections.OrderedDict, null=True),
        ),
    ]