import logging

import jsonschema
from django.db import models
from jsonschema.exceptions import ValidationError


class FieldType(models.Model):
    key = models.CharField(max_length=256, unique=True)
    config_schema = models.JSONField(null=True, blank=True)
    value_schema = models.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Field(models.Model):
    key = models.CharField(max_length=256, unique=True)
    name = models.CharField(max_length=256)
    config = models.JSONField(null=True, blank=True)
    field_type = models.ForeignKey(FieldType, related_name="fields", on_delete=models.PROTECT)
    description = models.CharField(max_length=512, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        config_schema = self.field_type.config_schema
        if config_schema:
            try:
                jsonschema.validate(self.config, config_schema)
            except ValidationError as e:
                logger = logging.getLogger()
                logger.error(e)
                print(e)
                raise ValueError("Invalid config schema")
        return super().save(*args, **kwargs)


class Screen(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True, blank=True)
    fields = models.ManyToManyField(Field, through="ScreenField", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ScreenField(models.Model):
    screen = models.ForeignKey(Screen, related_name="screen_field_schemas", on_delete=models.PROTECT)
    field = models.ForeignKey(Field, related_name="screen_field_schemas", on_delete=models.PROTECT)
    is_required = models.BooleanField()
    priority = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "screen",
            "field",
        )

    def save(self, no_priority_update=False, *args, **kwargs):
        if not no_priority_update:
            i = 0
            for screen_field in ScreenField.objects.filter(screen=self.screen, priority__lt=self.priority).exclude(
                pk=self.pk
            ):
                screen_field.priority = i
                screen_field.save(*args, **kwargs, no_priority_update=True)
                i += 1
            self.priority = i
            i += 1
            for screen_field in ScreenField.objects.filter(screen=self.screen, priority__gte=self.priority).exclude(
                pk=self.pk
            ):
                screen_field.priority = i
                screen_field.save(*args, **kwargs, no_priority_update=True)
                i += 1

        return super().save(*args, **kwargs)
