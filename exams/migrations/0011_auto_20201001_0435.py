# Generated by Django 2.2.15 on 2020-10-01 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_studentessayanswer_is_graded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentchoiceanswer',
            name='student_exam',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_choice_answer', to='exams.StudentExam'),
        ),
    ]