# Generated by Django 2.2.15 on 2020-09-10 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0001_initial'),
        ('accounts', '0009_auto_20200910_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='student_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='classes.Class'),
        ),
    ]