from django.contrib import admin
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget

from django_shark_task.fields import models
from django_shark_task.utils.admin_utils import CustomChoiceField, get_label, get_linked_value


@admin.register(models.FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }

    list_display = (
        "pk",
        "key",
        "config_schema",
        "value_schema",
        "created",
        "updated",
    )


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": JSONEditorWidget},
    }

    list_display = (
        "pk",
        "key",
        "field_type_info",
        "description",
        "config",
        "created",
        "updated",
    )

    def field_type_info(self, obj):
        field_type = obj.field_type
        return get_linked_value(field_type, get_label(field_type, [["pk"], ["key"]]))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "field_type":
            return CustomChoiceField(models.FieldType.objects.all(), [["pk"], ["key"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ScreenFieldInline(admin.TabularInline):
    model = models.ScreenField
    extra = 0
    ordering = ("priority",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "field":
            return CustomChoiceField(models.Field.objects.all(), [["pk"], ["key"], ["name"], ["field_type", "key"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Screen)
class ScreenAdmin(admin.ModelAdmin):
    inlines = (ScreenFieldInline,)
    list_display = (
        "pk",
        "description",
        "name",
        "created",
        "updated",
    )
