# Generated by Django 3.0.6 on 2020-05-24 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200523_1216'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feed',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='feed',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='feeditem',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='feeditem',
            name='feed',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Feed',
        ),
        migrations.DeleteModel(
            name='FeedItem',
        ),
    ]