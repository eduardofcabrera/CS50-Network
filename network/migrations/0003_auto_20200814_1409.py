# Generated by Django 3.0.8 on 2020-08-14 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20200813_2013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_comments',
        ),
        migrations.RemoveField(
            model_name='user',
            name='comments_owner',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
