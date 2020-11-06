# Generated by Django 2.2.15 on 2020-10-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0011_auto_20201017_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='examAnswerFile',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name=' ملف الامتحان في المحاضرة'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='homeworkAnswerFile',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name=' ملف الواجب في المحاضرة'),
        ),
    ]