# Generated by Django 2.2.15 on 2020-09-03 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_auto_20200903_0144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentexam',
            name='exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_exam', to='exams.Exam'),
        ),
    ]