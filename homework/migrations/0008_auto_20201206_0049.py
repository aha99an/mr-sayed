# Generated by Django 2.2.15 on 2020-12-05 22:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0007_auto_20201205_2336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studenthomeworkmakeup',
            options={'ordering': ('created_at',)},
        ),
    ]
