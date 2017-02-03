# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myjournal', '0003_auto_20170103_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='task',
            field=models.OneToOneField(to='myjournal.Task'),
        ),
    ]
