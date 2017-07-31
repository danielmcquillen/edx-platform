# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20161117_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=6, null=True, db_index=True, choices=[
                (b'm', b'Male'),
                (b'f', b'Female'),
                (b't', b'Transgender'),
                (b'p', b'Prefer not to say'),
                (b'o', b'I do not identify with any of the listed options.')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='level_of_education',
            field=models.CharField(blank=True, max_length=6, null=True, db_index=True, choices=[
                (b'b', b'Undergraduate'),
                (b'm', b"Master's or professional degree"),
                (b'p', b'Doctorate'), (b'r', b'Postdoctoral researcher'),
                (b'e', b'Early career faculty member (pre-tenure)'),
                (b'n', b'Non-tenure track faculty member'),
                (b't', b'Tenured faculty'),
                (b'r', b'Researcher/staff scientist'),
                (b'a', b'Administrator'),
                (b's', b'Professional development/career development staff'),
                (b'o', b'Other')]),
        ),
    ]
