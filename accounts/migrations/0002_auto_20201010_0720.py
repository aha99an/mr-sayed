# Generated by Django 2.2.15 on 2020-10-10 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='parentPhoneNumber',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phoneNumber',
            field=models.CharField(default='0', max_length=200),
        ),
    ]
