# Generated by Django 2.2.15 on 2020-10-10 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0003_remove_homework_homework_text1'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studenthomework',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='studenthomeworkfile',
            options={'ordering': ('created_at',)},
        ),
    ]
