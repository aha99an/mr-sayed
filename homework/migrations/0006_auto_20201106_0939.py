# Generated by Django 2.2.15 on 2020-11-06 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0005_studenthomeworkmakeup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studenthomeworkmakeup',
            old_name='exam',
            new_name='homework',
        ),
    ]
