from django.contrib import admin

from shark_task_utils.admin_utils import CustomChoiceField, get_label, get_linked_value
from shark_task_workflow import models


@admin.register(models.StatusType)
class StatusTypeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "status_type_info",
        "name",
        "created",
        "updated",
    )

    def status_type_info(self, obj):
        status_type = obj.status_type
        return get_linked_value(status_type, get_label(status_type, [["pk"], ["name"]]))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "status_type":
            return CustomChoiceField(models.StatusType.objects.all(), [["pk"], ["name"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TransitionInline(admin.TabularInline):
    model = models.Transition
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "src_status":
            return CustomChoiceField(models.Status.objects.all(), [["pk"], ["name"]], required=False)
        elif db_field.name == "dest_status":
            return CustomChoiceField(models.Status.objects.all(), [["pk"], ["name"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    inlines = (TransitionInline,)
    list_display = (
        "pk",
        "name",
        "created",
        "updated",
    )


@admin.register(models.Transition)
class TransitionAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "src_status_info",
        "dest_status_info",
        "workflow_info",
        "is_initial",
        "created",
        "updated",
    )

    def src_status_info(self, obj):
        status = obj.src_status
        return get_linked_value(status, get_label(status, [["pk"], ["name"]]))

    def dest_status_info(self, obj):
        status = obj.dest_status
        return get_linked_value(status, get_label(status, [["pk"], ["name"]]))

    def workflow_info(self, obj):
        workflow = obj.workflow
        return get_linked_value(workflow, get_label(workflow, [["pk"], ["name"]]))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "src_status":
            return CustomChoiceField(models.Status.objects.all(), [["pk"], ["name"]], required=False)
        elif db_field.name == "dest_status":
            return CustomChoiceField(models.Status.objects.all(), [["pk"], ["name"]])
        elif db_field.name == "workflow":
            return CustomChoiceField(models.Workflow.objects.all(), [["pk"], ["name"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
