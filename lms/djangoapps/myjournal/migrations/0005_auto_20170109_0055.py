# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjournal', '0004_auto_20170109_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='task',
            field=models.OneToOneField(related_name='entry', to='myjournal.Task'),
        ),
    ]
