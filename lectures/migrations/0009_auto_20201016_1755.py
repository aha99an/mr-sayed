# Generated by Django 2.2.15 on 2020-10-16 15:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lectures', '0008_remove_lecture_lecture_manual_allow'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StudentSeenLecture',
            new_name='StudentSeenLink',
        ),
        migrations.RenameField(
            model_name='studentlecture',
            old_name='attendance',
            new_name='is_seen',
        ),
        migrations.RemoveField(
            model_name='studentlecture',
            name='special_access',
        ),
    ]
