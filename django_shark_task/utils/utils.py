import importlib

from django.contrib.auth import get_user_model

from django_shark_task.task.models import Task, TaskEvent

User = get_user_model()


class Condition:
    def is_active(self, task: Task, user: User) -> bool:
        ...


class Postfunction:
    def execute(self, task: Task, user: User) -> None:
        ...
        ...


class EventListener:
    def notify(self, task: Task, task_events: list[TaskEvent], user: User) -> None:
        ...


def create_instance(class_name: str, args: list, kwargs: dict):
    module_name, class_name = class_name.rsplit(".", 1)
    cls = getattr(importlib.import_module(module_name), class_name)
    return cls(*args, **kwargs)
