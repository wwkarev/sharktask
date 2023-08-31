from django.contrib.auth import get_user_model
from django.db import transaction

from shark_task_core.const import TaskEventName
from shark_task_core.models import Link, TaskEvent

User = get_user_model()


class LinkManager:
    def create(self, link_type_id: int, src_task_id: int, dest_task_id: int, user: User) -> Link:
        with transaction.atomic():
            link = Link.objects.create(link_type_id=link_type_id, src_task_id=src_task_id, dest_task_id=dest_task_id)
            TaskEvent.objects.create(task_id=src_task_id, name=TaskEventName.LINK_CREATED, user=user)
            return link

    def delete(self, link_id: int, user: User) -> None:
        with transaction.atomic():
            link = Link.objects.select_related("src_task").get(pk=link_id)
            task = link.src_task
            link.delete()
            TaskEvent.objects.create(task=task, name=TaskEventName.LINK_DELETED, user=user)
