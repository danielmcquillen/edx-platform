# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjournal', '0002_auto_20170103_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='myjournal',
            field=models.ForeignKey(related_name='tasks', to='myjournal.CourseMyJournal'),
        ),
    ]
