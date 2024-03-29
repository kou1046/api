# Generated by Django 4.1.3 on 2022-12-08 16:52

import datetime
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_mousepos_rename_drag_mousedrag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='group',
            field=models.ForeignKey(default=datetime.datetime(2022, 12, 8, 16, 52, 52, 208317, tzinfo=datetime.timezone.utc), on_delete=django.db.models.deletion.CASCADE, to='api.group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mousepos',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
