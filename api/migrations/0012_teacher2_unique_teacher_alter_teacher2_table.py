# Generated by Django 4.1.3 on 2022-12-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_inferencemodel_alter_device_group_teacher2_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='teacher2',
            constraint=models.UniqueConstraint(fields=('person', 'model'), name='unique_teacher'),
        ),
        migrations.AlterModelTable(
            name='teacher2',
            table='teacher',
        ),
    ]
