# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myjournal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('flag', models.IntegerField(default=0, db_index=True, choices=[(0, b'OK'), (1, b'Flagged as inappropriate')])),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('hide', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['updated']},
        ),
        migrations.AddField(
            model_name='entry',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='myjournal',
            field=models.ForeignKey(related_name='entries', default=1, to='myjournal.CourseMyJournal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='task',
            field=models.ForeignKey(related_name='entries', to='myjournal.Task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='sequence',
            field=models.IntegerField(verbose_name=b'Where this entry is positioned in MyJournal list of entries for course.'),
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(related_name='comments', to='myjournal.Entry'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
