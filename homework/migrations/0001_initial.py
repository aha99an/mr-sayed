# Generated by Django 2.2.15 on 2020-09-26 21:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='اسم الواجب')),
                ('homework_file', models.FileField(blank=True, null=True, upload_to='', verbose_name='ملف الواجب')),
                ('homework_text', models.CharField(blank=True, max_length=200, null=True, verbose_name='الواجب')),
                ('homework_answer_file', models.FileField(blank=True, null=True, upload_to='', verbose_name='ملف حل الواجب')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('week', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='homework', to='classes.Week', verbose_name='الأسبوع')),
            ],
        ),
        migrations.CreateModel(
            name='StudentHomework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True)),
                ('is_checked', models.BooleanField(default=False)),
                ('notes_file', models.FileField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_homework', to='homework.Homework')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentHomeworkFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_homework_file', models.FileField(blank=True, null=True, upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_homework_file', to='homework.StudentHomework')),
            ],
        ),
    ]
