# Generated by Django 2.2.15 on 2020-10-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_studentpayment_last_lecture_attended'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentpayment',
            name='remainder_available_lectures',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
