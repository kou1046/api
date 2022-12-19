# Generated by Django 4.1.3 on 2022-12-19 05:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_mousepos_group_mousepos_unique_mouse_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='InferenceModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('label_description', models.CharField(max_length=100)),
                ('model_path', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'inference_model',
            },
        ),
        migrations.AlterField(
            model_name='device',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='api.group'),
        ),
        migrations.CreateModel(
            name='Teacher2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.IntegerField(default=0)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='api.inferencemodel')),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.person')),
            ],
        ),
        migrations.AddField(
            model_name='pteacher',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.inferencemodel'),
        ),
        migrations.AddField(
            model_name='wdteacher',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.inferencemodel'),
        ),
        migrations.AddField(
            model_name='wthteacher',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.inferencemodel'),
        ),
    ]