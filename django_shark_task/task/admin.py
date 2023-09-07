from django.contrib import admin

from django_shark_task.task import models
from django_shark_task.utils.admin_utils import CustomChoiceField, get_label, get_linked_value


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "key",
        "name",
        "description",
        "created",
        "updated",
    )


@admin.register(models.TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "description",
        "created",
        "updated",
    )


@admin.register(models.ProjectSchema)
class ProjectSchemaAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "project_info",
        "task_type_info",
        "screen_info",
        "workflow_info",
        "is_active",
        "created",
        "updated",
    )

    def project_info(self, obj):
        project = obj.project
        return get_linked_value(project, get_label(project, [["pk"], ["key"], ["name"]]))

    def task_type_info(self, obj):
        task_type = obj.task_type
        return get_linked_value(task_type, get_label(task_type, [["pk"], ["name"]]))

    def screen_info(self, obj):
        screen = obj.screen
        return get_linked_value(screen, get_label(screen, [["pk"], ["name"]]))

    def workflow_info(self, obj):
        workflow = obj.workflow
        return get_linked_value(workflow, get_label(workflow, [["pk"], ["name"]]))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            return CustomChoiceField(models.Project.objects.all(), [["pk"], ["key"], ["name"]])
        elif db_field.name == "task_type":
            return CustomChoiceField(models.TaskType.objects.all(), [["pk"], ["name"]])
        elif db_field.name == "screen":
            return CustomChoiceField(models.Screen.objects.all(), [["pk"], ["name"]])
        elif db_field.name == "workflow":
            return CustomChoiceField(models.Workflow.objects.all(), [["pk"], ["name"]])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(models.LinkType)
class LinkTypeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "src_name",
        "dest_name",
        "created",
        "updated",
    )
