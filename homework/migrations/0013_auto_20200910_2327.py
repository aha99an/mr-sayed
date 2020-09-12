# Generated by Django 2.2.15 on 2020-09-10 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homework', '0012_auto_20200910_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworkanswerfile',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_answer_file', to='homework.Homework'),
        ),
        migrations.AlterField(
            model_name='homeworkfile',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_file', to='homework.Homework'),
        ),
        migrations.AlterField(
            model_name='homeworknotebook',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homework_notebook', to='homework.Homework'),
        ),
        migrations.AlterField(
            model_name='studenthomework',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_homework', to='homework.Homework'),
        ),
        migrations.AlterField(
            model_name='studenthomeworkfile',
            name='student_homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_homework_file', to='homework.StudentHomework'),
        ),
    ]
