# Generated by Django 4.2.4 on 2023-09-07 03:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Field",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=256, unique=True)),
                ("name", models.CharField(max_length=256)),
                ("config", models.JSONField(blank=True, null=True)),
                ("description", models.CharField(blank=True, max_length=512, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="FieldType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=256, unique=True)),
                ("config_schema", models.JSONField(blank=True, null=True)),
                ("value_schema", models.JSONField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
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
                ("event_listeners", models.JSONField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "groups_with_delete_permission",
                    models.ManyToManyField(
                        blank=True, related_name="project_schemas_with_delete_permission", to="auth.group"
                    ),
                ),
                (
                    "groups_with_read_permission",
                    models.ManyToManyField(
                        blank=True, related_name="project_schemas_with_read_permission", to="auth.group"
                    ),
                ),
                (
                    "groups_with_write_permission",
                    models.ManyToManyField(
                        blank=True, related_name="project_schemas_with_write_permission", to="auth.group"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="project_task_schemas",
                        to="django_shark_task.project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Screen",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("description", models.CharField(blank=True, max_length=512, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="StatusType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
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
                        to="django_shark_task.projectschema",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="tasks", to="django_shark_task.status"
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
            name="Workflow",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Transition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=256)),
                ("is_initial", models.BooleanField()),
                ("conditions", models.JSONField(blank=True, null=True)),
                ("postfunctions", models.JSONField(blank=True, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "dest_status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="dest_transitions",
                        to="django_shark_task.status",
                    ),
                ),
                (
                    "src_status",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="src_transitions",
                        to="django_shark_task.status",
                    ),
                ),
                (
                    "workflow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="transitions",
                        to="django_shark_task.workflow",
                    ),
                ),
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
                        to="django_shark_task.task",
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
            model_name="status",
            name="status_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="statuses", to="django_shark_task.statustype"
            ),
        ),
        migrations.CreateModel(
            name="ScreenField",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("is_required", models.BooleanField()),
                ("priority", models.IntegerField(default=100)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "field",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="screen_field_schemas",
                        to="django_shark_task.field",
                    ),
                ),
                (
                    "screen",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="screen_field_schemas",
                        to="django_shark_task.screen",
                    ),
                ),
            ],
            options={
                "unique_together": {("screen", "field")},
            },
        ),
        migrations.AddField(
            model_name="screen",
            name="fields",
            field=models.ManyToManyField(
                blank=True, through="django_shark_task.ScreenField", to="django_shark_task.field"
            ),
        ),
        migrations.AddField(
            model_name="projectschema",
            name="screen",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="project_task_schemas",
                to="django_shark_task.screen",
            ),
        ),
        migrations.AddField(
            model_name="projectschema",
            name="task_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="project_task_schemas",
                to="django_shark_task.tasktype",
            ),
        ),
        migrations.AddField(
            model_name="projectschema",
            name="workflow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="project_task_schemas",
                to="django_shark_task.workflow",
            ),
        ),
        migrations.AddField(
            model_name="field",
            name="field_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name="fields", to="django_shark_task.fieldtype"
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
                        to="django_shark_task.task",
                    ),
                ),
                (
                    "link_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="links",
                        to="django_shark_task.linktype",
                    ),
                ),
                (
                    "src_task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="src_links",
                        to="django_shark_task.task",
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
                        to="django_shark_task.field",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="field_values",
                        to="django_shark_task.task",
                    ),
                ),
            ],
            options={
                "unique_together": {("task", "field")},
            },
        ),
    ]
