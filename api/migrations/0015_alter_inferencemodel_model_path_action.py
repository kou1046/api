# Generated by Django 4.1.5 on 2023-01-19 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_rename_teacher2_teacher_remove_wdteacher_model_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="inferencemodel",
            name="model_path",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.CreateModel(
            name="Action",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_programming", models.BooleanField()),
                ("is_having_pen", models.BooleanField()),
                ("is_watching_display", models.BooleanField()),
                (
                    "person",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="action",
                        to="api.person",
                    ),
                ),
            ],
            options={
                "db_table": "action",
            },
        ),
    ]