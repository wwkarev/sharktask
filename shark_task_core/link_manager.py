from django.contrib.auth import get_user_model
from django.db import transaction

from shark_task_core.models import Link, Task, TaskEvent, TaskEventType

User = get_user_model()


class LinkManager:
    def create(self, link_type_id: int, src_task_id: int, dest_task_id: int, user: User) -> Link:
        with transaction.atomic():
            link = Link.objects.create(link_type_id=link_type_id, src_task_id=src_task_id, dest_task_id=dest_task_id)
            TaskEvent.objects.create(
                task_id=src_task_id,
                type=TaskEventType.LINK_CREATED,
                user=user,
                field=self._create_task_info(link.dest_task),
            )
            return link

    def delete(self, link_id: int, user: User) -> None:
        with transaction.atomic():
            link = Link.objects.select_related("src_task").get(pk=link_id)
            link.delete()
            TaskEvent.objects.create(
                task_id=link.src_task_id,
                type=TaskEventType.LINK_DELETED,
                user=user,
                field=self._create_task_info(link.dest_task),
            )

    def _create_task_info(self, task: Task) -> dict:
        return {"id": task.pk, "key": task.key, "summary": task.summary}
