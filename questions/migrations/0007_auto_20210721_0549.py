# Generated by Django 2.2.15 on 2021-07-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_mrquestionfile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mrquestion',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterModelOptions(
            name='mrquestionfile',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AddField(
            model_name='mrquestion',
            name='display_to_all',
            field=models.BooleanField(default=False),
        ),
    ]
