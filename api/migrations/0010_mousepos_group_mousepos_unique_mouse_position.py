# Generated by Django 4.1.3 on 2022-12-08 17:39

import datetime

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_device_group_alter_mousepos_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mousepos',
            name='group',
            field=models.ForeignKey(default=datetime.datetime(2022, 12, 8, 17, 39, 42, 148914, tzinfo=datetime.timezone.utc), on_delete=django.db.models.deletion.CASCADE, related_query_name='mouse_postions', to='api.group'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='mousepos',
            constraint=models.UniqueConstraint(fields=('group', 'time'), name='unique_mouse_position'),
        ),
    ]
