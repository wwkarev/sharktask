import logging

import jsonschema
from django.contrib.auth import get_user_model
from django.db import models
from jsonschema.exceptions import ValidationError

from shark_task_fields.models import Field, Screen
from shark_task_workflow.models import Status, Workflow

User = get_user_model()


class Project(models.Model):
    key = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class TaskType(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ProjectSchema(models.Model):
    is_active = models.BooleanField()
    project = models.ForeignKey(Project, related_name="project_task_schemas", on_delete=models.PROTECT)
    task_type = models.ForeignKey(TaskType, related_name="project_task_schemas", on_delete=models.PROTECT)
    screen = models.ForeignKey(Screen, related_name="project_task_schemas", on_delete=models.PROTECT)
    workflow = models.ForeignKey(Workflow, related_name="project_task_schemas", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if (
            self.is_active
            and ProjectSchema.objects.filter(project=self.project, task_type=self.task_type, is_active=True)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValueError("Only one active project schema for project and task_type could be exist")
        if not self.is_active and Task.objects.filter(project_schema_id=self.pk).exists():
            raise ValueError("You cannot deactivate project schema with linked tasks")
        return super().save(*args, **kwargs)


class Task(models.Model):
    project_schema = models.ForeignKey(ProjectSchema, related_name="tasks", on_delete=models.PROTECT)
    key = models.CharField(max_length=64, unique=True)
    task_num = models.IntegerField()
    summary = models.CharField(max_length=1024)
    status = models.ForeignKey(Status, related_name="tasks", on_delete=models.PROTECT)
    creator = models.ForeignKey(User, related_name="shark_tasks", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class TaskEvent(models.Model):
    task = models.ForeignKey(Task, related_name="task_events", on_delete=models.PROTECT)
    name = models.CharField(max_length=128)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, related_name="shark_task_events", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)


class LinkType(models.Model):
    src_name = models.CharField(max_length=128)
    dest_name = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Link(models.Model):
    link_type = models.ForeignKey(LinkType, related_name="links", on_delete=models.PROTECT)
    src_task = models.ForeignKey(Task, related_name="src_links", on_delete=models.PROTECT)
    dest_task = models.ForeignKey(Task, related_name="dest_links", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "link_type",
            "src_task",
            "dest_task",
        )


class FieldValue(models.Model):
    task = models.ForeignKey(Task, related_name="field_values", on_delete=models.PROTECT)
    field = models.ForeignKey(Field, related_name="field_values", on_delete=models.PROTECT)
    value = models.JSONField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "task",
            "field",
        )

    def save(self, *args, **kwargs):
        try:
            jsonschema.validate(self.value, self.field.field_type.value_schema)
        except ValidationError as e:
            logger = logging.getLogger()
            logger.error(e)
            print(e)
            raise ValueError("Invalid field value schema")
        return super().save(*args, **kwargs)