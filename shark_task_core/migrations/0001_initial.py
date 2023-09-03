# Generated by Django 4.2.4 on 2023-09-03 04:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shark_task_fields", "0001_initial"),
        ("shark_task_workflow", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="LinkType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("src_name", models.CharField(max_length=128)),
                ("dest_name", models.CharField(max_length=128)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=256, unique=True)),
                ("name", models.CharField(max_length=256, unique=True)),
                ("description", models.CharField(blank=True, max_length=512, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProjectSchema",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_active", models.BooleanField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="project_task_schemas",
                        to="shark_task_core.project",
                    ),
                ),
                (
                    "screen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="project_task_schemas",
                        to="shark_task_fields.screen",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=64, unique=True)),
                ("task_num", models.IntegerField()),
                ("summary", models.CharField(max_length=1024)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="shark_tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project_schema",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tasks",
                        to="shark_task_core.projectschema",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="tasks",
                        to="shark_task_workflow.status",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, unique=True)),
                ("description", models.CharField(blank=True, max_length=512, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TaskEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("TASK_CREATED", "TASK_CREATED"),
                            ("TASK_UPDATED", "TASK_UPDATED"),
                            ("SUMMARY_UPDATED", "SUMMARY_UPDATED"),
                            ("STATUS_UPDATED", "STATUS_UPDATED"),
                            ("LINK_CREATED", "LINK_CREATED"),
                            ("LINK_DELETED", "LINK_DELETED"),
                        ],
                        max_length=128,
                    ),
                ),
                ("field", models.JSONField(blank=True, null=True)),
                ("old_value", models.JSONField(blank=True, null=True)),
                ("new_value", models.JSONField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="task_events",
                        to="shark_task_core.task",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="shark_task_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="projectschema",
            name="task_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="project_task_schemas",
                to="shark_task_core.tasktype",
            ),
        ),
        migrations.AddField(
            model_name="projectschema",
            name="workflow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="project_task_schemas",
                to="shark_task_workflow.workflow",
            ),
        ),
        migrations.CreateModel(
            name="Link",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "dest_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dest_links",
                        to="shark_task_core.task",
                    ),
                ),
                (
                    "link_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="links", to="shark_task_core.linktype"
                    ),
                ),
                (
                    "src_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="src_links", to="shark_task_core.task"
                    ),
                ),
            ],
            options={
                "unique_together": {("link_type", "src_task", "dest_task")},
            },
        ),
        migrations.CreateModel(
            name="FieldValue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.JSONField()),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="field_values",
                        to="shark_task_fields.field",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="field_values",
                        to="shark_task_core.task",
                    ),
                ),
            ],
            options={
                "unique_together": {("task", "field")},
            },
        ),
    ]
