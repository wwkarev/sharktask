import logging

import jsonschema
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from jsonschema.exceptions import ValidationError

from django_shark_task.fields.models import Field, Screen
from django_shark_task.task.const import TASK_EVENT_LISTENERS_JSON_SCHEMA
from django_shark_task.workflow.models import Status, Workflow

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
    event_listeners = models.JSONField(null=True, blank=True)
    groups_with_read_permission = models.ManyToManyField(
        Group, related_name="project_schemas_with_read_permission", blank=True
    )
    groups_with_write_permission = models.ManyToManyField(
        Group, related_name="project_schemas_with_write_permission", blank=True
    )
    groups_with_delete_permission = models.ManyToManyField(
        Group, related_name="project_schemas_with_delete_permission", blank=True
    )
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
        if self.event_listeners:
            try:
                jsonschema.validate(self.event_listeners, TASK_EVENT_LISTENERS_JSON_SCHEMA)
            except ValidationError as e:
                logger = logging.getLogger()
                logger.error(e)
                print(e)
                raise ValueError("Invalid event listener schema")
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


class TaskEventType:
    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    SUMMARY_UPDATED = "SUMMARY_UPDATED"
    STATUS_UPDATED = "STATUS_UPDATED"
    LINK_CREATED = "LINK_CREATED"
    LINK_DELETED = "LINK_DELETED"
    CHOICES = (
        (TASK_CREATED, TASK_CREATED),
        (TASK_UPDATED, TASK_UPDATED),
        (SUMMARY_UPDATED, SUMMARY_UPDATED),
        (STATUS_UPDATED, STATUS_UPDATED),
        (LINK_CREATED, LINK_CREATED),
        (LINK_DELETED, LINK_DELETED),
    )


class TaskEvent(models.Model):
    type = models.CharField(max_length=128, choices=TaskEventType.CHOICES)
    task = models.ForeignKey(Task, related_name="task_events", on_delete=models.PROTECT)
    field = models.JSONField(null=True, blank=True)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
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
