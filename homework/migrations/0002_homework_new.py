# Generated by Django 2.2.15 on 2020-09-26 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='new',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]