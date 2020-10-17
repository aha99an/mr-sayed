# Generated by Django 2.2.15 on 2020-10-12 23:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_studentexammakeup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentexammakeup',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='studentexammakeup',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentexammakeup',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]