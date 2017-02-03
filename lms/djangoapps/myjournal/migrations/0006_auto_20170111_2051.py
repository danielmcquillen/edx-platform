# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjournal', '0005_auto_20170109_0055'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['updated']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='user',
            new_name='owner',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='status',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='title',
        ),
        migrations.AddField(
            model_name='entry',
            name='excerpt',
            field=models.TextField(editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=5000, blank=True),
        ),
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=models.TextField(max_length=20000, blank=True),
        ),
    ]
