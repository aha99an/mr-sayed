# Generated by Django 2.2.15 on 2020-09-01 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=300, null=True)),
                ('image_question', models.ImageField(
                    blank=True, null=True, upload_to='')),
                ('grade', models.FloatField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(
                    blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('total_question', models.IntegerField(default=0)),
                ('score', models.DecimalField(
                    decimal_places=2, default=0, max_digits=10)),
                ('time_quiz', models.IntegerField(default=0)),
                ('mandatory', models.BooleanField(default=False)),
                ('max_tries', models.IntegerField(default=1)),
                ('availabe_from', models.DateTimeField(blank=True, null=True)),
                ('availabe_to', models.DateTimeField(blank=True, null=True)),
                ('answer', models.FileField(blank=True, null=True, upload_to='')),
                ('show_answer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, default=0, null=True)),
                ('answered_questions', models.IntegerField(
                    blank=True, default=0, null=True)),
                ('try_number', models.IntegerField(
                    blank=True, default=0, null=True)),
                ('created_at', models.DateTimeField(
                    blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='provider_quiz', to='exams.Exam')),
                ('user', models.ForeignKey(blank=True, null=True,
                                           on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=300, null=True)),
                ('image_question', models.ImageField(
                    blank=True, null=True, upload_to='')),
                ('grade', models.FloatField(max_length=100)),
                ('right_answer', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='StudentTrueFalseAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
                ('grade', models.FloatField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.EssayQuestion')),
                ('student_exam', models.ForeignKey(blank=True, null=True,
                                                   on_delete=django.db.models.deletion.CASCADE, to='exams.StudentExam')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEssayAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('image_answer', models.ImageField(
                    blank=True, null=True, upload_to='')),
                ('grade', models.FloatField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.EssayQuestion')),
                ('student_exam', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.StudentExam')),
            ],
        ),
        migrations.CreateModel(
            name='StudentChoiceAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=100, null=True)),
                ('grade', models.FloatField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.EssayQuestion')),
                ('student_exam', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.StudentExam')),
            ],
        ),
        migrations.AddField(
            model_name='essayquestion',
            name='exam',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='exams.Exam'),
        ),
        migrations.CreateModel(
            name='ChoiceQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=300, null=True)),
                ('image_question', models.ImageField(
                    blank=True, null=True, upload_to='')),
                ('option1', models.CharField(max_length=300)),
                ('option2', models.CharField(max_length=300)),
                ('option3', models.CharField(blank=True, max_length=300, null=True)),
                ('option4', models.CharField(blank=True, max_length=300, null=True)),
                ('right_answer_choice', models.IntegerField(choices=[
                 (0, 'option1'), (1, 'option2'), (2, 'option3'), (3, 'option4')])),
                ('grade', models.FloatField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='exams.Exam')),
            ],
        ),
    ]