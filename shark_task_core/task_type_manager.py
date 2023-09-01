from datetime import datetime
from typing import Optional

from shark_task_core.models import TaskType
from shark_task_core.serializers import ShortTaskTypeSerializer, TaskTypeSerializer


class TaskTypeInfo:
    id: int
    name: str
    description: Optional[str]
    created: datetime
    updated: datetime


class ShortTaskTypeInfo:
    id: int
    name: str


class TaskTypeManager:
    def get(self, task_type_id: int) -> TaskTypeInfo:
        task_type = TaskType.objects.get(pk=task_type_id)
        return self._get(task_type)

    def get_list(self) -> list[ShortTaskTypeInfo]:
        task_types = TaskType.objects.all().order_by("-name")
        return ShortTaskTypeSerializer(task_types, many=True).data

    def _get(self, task_type: TaskType) -> TaskTypeInfo:

        return TaskTypeSerializer(task_type).data

    def _get_short(self, task_type: TaskType) -> ShortTaskTypeInfo:
        return ShortTaskTypeSerializer(task_type).data
