# Generated by Django 2.2.15 on 2020-09-11 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_auto_20200911_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='class',
            name='week',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='week_class', to='classes.Week'),
        ),
        migrations.AlterField(
            model_name='class',
            name='week_day',
            field=models.CharField(blank=True, choices=[(0, 'السبت'), (1, 'الأحد'), (2, 'الاثنين'), (3, 'الثلاثاء'), (4, 'الاربعاء'), (5, 'الخميس'), (6, 'الجمعة')], max_length=1, null=True),
        ),
    ]
