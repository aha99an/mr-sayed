# Generated by Django 2.2.15 on 2020-10-10 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_merge_20201010_0833'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('date_joined',)},
        ),
    ]