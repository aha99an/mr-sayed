# Generated by Django 2.2.15 on 2020-11-06 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0014_auto_20201024_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentlecture',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]