# Generated by Django 4.1.3 on 2022-12-07 09:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_click_release_combinedframe_screenshot_path_drag_and_more'),
    ]

    operations = [
        #migrations.RemoveField(
        #    model_name='drag',
        #    name='frame',
        #),
        migrations.AddField(
            model_name='click',
            name='frame',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.combinedframe'),
        ),
        migrations.AddField(
            model_name='drag',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.person'),
        ),
        migrations.AddField(
            model_name='release',
            name='frame',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.combinedframe'),
        ),
    ]
