# Generated by Django 2.2.15 on 2020-09-22 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20200918_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mrquestion',
            name='image_question',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='اسأل بصوره:'),
        ),
        migrations.AlterField(
            model_name='mrquestion',
            name='question',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='السؤال:'),
        ),
    ]
