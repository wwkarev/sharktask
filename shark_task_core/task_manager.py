from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from pydantic.main import BaseModel

from shark_task_core.models import (
    FieldValue,
    Link,
    Project,
    ProjectSchema,
    Task,
    TaskEvent,
    TaskEventType,
)
from shark_task_fields.models import Field, Screen
from shark_task_fields.serializers import ShortFieldSerializer
from shark_task_workflow.models import Status, Transition
from shark_task_workflow.serializers import StatusSerializer

User = get_user_model()


class FieldValueInfo(BaseModel):
    id: int
    value: Optional[dict]


class CreateTaskInfo(BaseModel):
    project_id: int
    task_type_id: int
    summary: str
    fields: list[FieldValueInfo]

    class Config:
        arbitrary_types_allowed = True


class UpdateTaskInfo(BaseModel):
    summary: Optional[str]
    fields: list[FieldValueInfo]

    class Config:
        arbitrary_types_allowed = True


class ShortTaskInfo(BaseModel):
    id: int
    project_id: int
    task_type_id: int
    creator: User
    summary: str
    created: datetime
    updated: datetime

    class Config:
        arbitrary_types_allowed = True


class LinkInfo(BaseModel):
    id: int
    link_type_id: int
    linked_task: ShortTaskInfo

    class Config:
        arbitrary_types_allowed = True


class TaskInfo(BaseModel):
    id: int
    project_id: int
    task_type_id: int
    creator: User
    summary: str
    status: Status
    key: str
    task_num: int
    fields: list[FieldValueInfo]
    inward_links: list[LinkInfo]
    outward_links: list[LinkInfo]
    created: datetime
    updated: datetime

    class Config:
        arbitrary_types_allowed = True


class TaskManager:
    def create(self, task_info: CreateTaskInfo, user: User) -> TaskInfo:
        with transaction.atomic():
            project_schema = (
                ProjectSchema.objects.select_related("project", "screen")
                .prefetch_related("screen__fields__screen_field_schemas")
                .get(project_id=task_info.project_id, task_type_id=task_info.task_type_id, is_active=True)
            )
            project = project_schema.project
            self._validate_field_info_list_during_creation(project_schema.screen, task_info.fields)

            initial_status = self._get_initial_status(project_schema)

            task_num = self.get_max_task_num(task_info.project_id) + 1
            task = Task.objects.create(
                project_schema=project_schema,
                key=self.generate_task_key(project, task_num),
                task_num=task_num,
                summary=task_info.summary,
                status=initial_status,
                creator=user,
            )
            TaskEvent.objects.create(task=task, type=TaskEventType.TASK_CREATED, user=user)

            for field_info in task_info.fields:
                field = Field.objects.select_related("field_type").get(pk=field_info.id)
                FieldValue.objects.create(task=task, field=field, value=field_info.value)

            return self._get(task)

    def update(self, task_id: int, task_info: UpdateTaskInfo, user: User):
        with transaction.atomic():
            task = (
                Task.objects.select_related("status")
                .select_related("project_schema__project")
                .prefetch_related("project_schema__screen__fields")
                .get(pk=task_id)
            )
            project_schema = task.project_schema
            self._validate_field_info_list_during_update(project_schema.screen, task_info.fields)

            task_events: list[TaskEvent] = []
            if task_info.summary:
                old_summary = task.summary
                task.summary = task_info.summary
                task_events.append(
                    TaskEvent(
                        task=task,
                        type=TaskEventType.SUMMARY_UPDATED,
                        old_value={"summary", old_summary},
                        new_value={"summary", task_info.summary},
                        user=user,
                    )
                )

            for field_info in task_info.fields:
                field_value, _ = FieldValue.objects.get_or_create(task=task, field_id=field_info.id)
                field = Field.objects.get(pk=field_info.id)
                old_value = field_value.value
                field_value.value = field_info.value
                field_value.save()

                task_events.append(
                    TaskEvent(
                        task=task,
                        type=TaskEventType.TASK_UPDATED,
                        field=ShortFieldSerializer(field).data,
                        old_value=old_value,
                        new_value=field_info.value,
                        user=user,
                    )
                )

            TaskEvent.objects.bulk_create(task_events)

            task.updated = datetime.now()
            task.save()

        return self._get(task)

    def delete(self, task_id: int) -> None:
        with transaction.atomic():
            TaskEvent.objects.filter(task_id=task_id).delete()
            FieldValue.objects.filter(task_id=task_id).delete()
            Task.objects.get(pk=task_id).delete()

    def get(self, task_id: int) -> TaskInfo:
        task = (
            Task.objects.select_related("status")
            .select_related("project_schema__project")
            .prefetch_related("project_schema__screen__fields")
            .get(pk=task_id)
        )
        return self._get(task)

    def filter_task(self, project_id: int) -> list[ShortTaskInfo]:
        tasks = Task.objects.filter(project_schema__project_id=project_id).order_by("-created")
        return [self._get_short(task) for task in tasks]

    def _get(self, task: Task) -> TaskInfo:
        project_schema = task.project_schema

        inward_link_info_list = [
            LinkInfo(id=link.pk, link_type_id=link.link_type_id, linked_task=self._get_short(link.src_task))
            for link in Link.objects.select_related("src_task").filter(dest_task=task)
        ]
        outward_link_info_list = [
            LinkInfo(id=link.pk, link_type_id=link.link_type_id, linked_task=self._get_short(link.dest_task))
            for link in Link.objects.select_related("dest_task").filter(src_task=task)
        ]

        return TaskInfo(
            id=task.pk,
            project_id=project_schema.project_id,
            task_type_id=project_schema.task_type_id,
            creator=task.creator,
            summary=task.summary,
            status=task.status,
            key=task.key,
            task_num=task.task_num,
            fields=self._get_field_info_list(project_schema, task),
            inward_links=inward_link_info_list,
            outward_links=outward_link_info_list,
            created=task.created,
            updated=task.updated,
        )

    def _get_short(self, task: Task) -> ShortTaskInfo:
        return ShortTaskInfo(
            id=task.pk,
            project_id=task.project_schema.project_id,
            task_type_id=task.project_schema.task_type_id,
            creator=task.creator,
            summary=task.summary,
            created=task.created,
            updated=task.updated,
        )

    def get_max_task_num(self, project_id: int) -> int:
        max_task_num = 0
        if task := Task.objects.filter(project_schema__project_id=project_id).order_by("-task_num").first():
            max_task_num = task.task_num
        return max_task_num

    def generate_task_key(self, project: Project, task_num: int) -> str:
        return f"{project.key}-{task_num}"

    def get_transitions(self, task_id: int) -> list[Transition]:
        task = Task.objects.select_related("project_schema").get(pk=task_id)
        return self._get_out_transitions_query_set(task)

    def transit(self, task_id: int, transition_id: int, user: User) -> None:
        with transaction.atomic():
            task = Task.objects.select_related("status", "project_schema").get(pk=task_id)
            transition = self._get_out_transitions_query_set(task).get(pk=transition_id)
            TaskEvent.objects.create(
                task=task,
                type=TaskEventType.STATUS_UPDATED,
                user=user,
                old_value=StatusSerializer(task.status).data,
                new_value=StatusSerializer(transition.dest_status).data,
            )
            task.status = transition.dest_status
            task.save()

    def _get_out_transitions_query_set(self, task: Task) -> list[Transition]:
        return (
            Transition.objects.filter(workflow_id=task.project_schema.workflow_id)
            .filter(Q(src_status_id=task.status_id) | Q(src_status_id__isnull=True))
            .exclude(is_initial=True)
        )

    def _get_field_info_list(self, project_schema: ProjectSchema, task: Task) -> list[FieldValueInfo]:
        field_value_storage: dict[int, dict] = {
            field_value.field.pk: field_value.value
            for field_value in FieldValue.objects.select_related("field").filter(task=task, value__isnull=False)
        }

        field_info_list: list[FieldValueInfo] = []
        for field in project_schema.screen.fields.all():
            field_info_list.append(FieldValueInfo(id=field.pk, value=field_value_storage.get(field.pk)))
        return field_info_list

    def _validate_field_info_list_during_creation(self, screen: Screen, field_info_list: list[FieldValueInfo]) -> None:
        required_field_storage = self._get_required_field_storage(screen)
        filled_field_id_set = {field_info.id for field_info in field_info_list if field_info.value is not None}
        for _, required_field in required_field_storage.items():
            if required_field.pk not in filled_field_id_set:
                raise ValueError(f"Field {required_field.name} is required")

    def _validate_field_info_list_during_update(self, screen: Screen, field_info_list: list[FieldValueInfo]) -> None:
        required_field_storage = self._get_required_field_storage(screen)

        for field_info in field_info_list:
            if field_info.id in required_field_storage and field_info.value is None:
                required_field = required_field_storage[field_info.id]
                raise ValueError(f"Field {required_field.name} is required")

    def _get_required_field_storage(self, screen: Screen) -> dict[int, Field]:
        return {field.pk: field for field in screen.fields.filter(screen_field_schemas__is_required=True)}

    def _get_initial_status(self, project_schema: ProjectSchema) -> Status:
        initial_transition = Transition.objects.select_related("dest_status__status_type").get(
            workflow_id=project_schema.workflow_id, is_initial=True
        )
        return initial_transition.dest_status
