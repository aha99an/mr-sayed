# Generated by Django 2.2.15 on 2020-10-10 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choicequestion',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='essayquestion',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='studentchoiceanswer',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='studentessayanswer',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='studentexam',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='studenttruefalseanswer',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='truefalsequestion',
            options={'ordering': ('created_at',)},
        ),
    ]