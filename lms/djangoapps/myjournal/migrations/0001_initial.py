# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import xmodule_django.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseMyJournal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('myjournal_id', models.CharField(unique=True, max_length=255)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('course_id', xmodule_django.models.CourseKeyField(max_length=255, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text=b"Used to build the entry's URL.", max_length=255)),
                ('status', models.IntegerField(default=0, db_index=True, choices=[(0, b'private'), (1, b'public')])),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('text', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence', models.IntegerField(verbose_name=b'Where this entry is positioning in MyJournal list of entries for course.')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title for entry')),
                ('description', models.TextField(verbose_name=b'Instructor description of entry task')),
                ('myjournal', models.ForeignKey(to='myjournal.CourseMyJournal')),
            ],
            options={
                'ordering': ['sequence'],
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='task',
            field=models.ForeignKey(to='myjournal.Task'),
        ),
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
