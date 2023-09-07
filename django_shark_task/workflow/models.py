import logging

import jsonschema
from django.db import models
from jsonschema.exceptions import ValidationError

from django_shark_task.workflow.const import (
    TRANSITION_CONDITIONS_JSON_SCHEMA,
    TRANSITION_POSTFUNCIONS_JSON_SCHEMA,
)


class StatusType(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Status(models.Model):
    status_type = models.ForeignKey(StatusType, related_name="statuses", on_delete=models.PROTECT)
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Workflow(models.Model):
    name = models.CharField(max_length=256, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Transition(models.Model):
    name = models.CharField(max_length=256)
    src_status = models.ForeignKey(
        Status, related_name="src_transitions", on_delete=models.PROTECT, null=True, blank=True
    )
    dest_status = models.ForeignKey(Status, related_name="dest_transitions", on_delete=models.PROTECT)
    workflow = models.ForeignKey(Workflow, related_name="transitions", on_delete=models.PROTECT)
    is_initial = models.BooleanField()
    conditions = models.JSONField(null=True, blank=True)
    postfunctions = models.JSONField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if (
            self.is_initial
            and Transition.objects.filter(workflow_id=self.workflow.pk, is_initial=True).exclude(pk=self.pk).exists()
        ):
            raise ValueError("Only one transition in one workflow could be initial")
        if self.conditions:
            try:
                jsonschema.validate(self.conditions, TRANSITION_CONDITIONS_JSON_SCHEMA)
            except ValidationError as e:
                logger = logging.getLogger()
                logger.error(e)
                print(e)
                raise ValueError("Invalid condition schema")
        if self.postfunctions:
            try:
                jsonschema.validate(self.postfunctions, TRANSITION_POSTFUNCIONS_JSON_SCHEMA)
            except ValidationError as e:
                logger = logging.getLogger()
                logger.error(e)
                print(e)
                raise ValueError("Invalid postfunction schema")
        return super().save(*args, **kwargs)
