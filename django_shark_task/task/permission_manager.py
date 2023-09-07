from django.contrib.auth import get_user_model

from django_shark_task.task.models import ProjectSchema

User = get_user_model()


class PermissionManager:
    def check_read_permissions(self, user: User, project_schema: ProjectSchema) -> None:
        (
            group_ids_with_read_permission,
            group_ids_with_write_permission,
            group_ids_with_delete_permission,
        ) = self._get_group_ids_with_permission(project_schema)

        if group_ids_with_read_permission and not self._is_user_in_groups(
            user, group_ids_with_read_permission + group_ids_with_write_permission + group_ids_with_delete_permission
        ):
            raise PermissionError(f"No read permission {user.username} on project_schema {project_schema.pk}")

    def check_write_permissions(self, user: User, project_schema: ProjectSchema) -> None:
        _, group_ids_with_write_permission, group_ids_with_delete_permission = self._get_group_ids_with_permission(
            project_schema
        )

        if group_ids_with_write_permission and not self._is_user_in_groups(
            user, group_ids_with_write_permission + group_ids_with_delete_permission
        ):
            raise PermissionError(f"No write permission {user.username} on project_schema {project_schema.pk}")

    def check_delete_permissions(self, user: User, project_schema: ProjectSchema) -> None:
        _, _, group_ids_with_delete_permission = self._get_group_ids_with_permission(project_schema)

        if group_ids_with_delete_permission and not self._is_user_in_groups(user, group_ids_with_delete_permission):
            raise PermissionError(f"No delete permission {user.username} on project_schema {project_schema.pk}")

    def _get_group_ids_with_permission(self, project_schema: ProjectSchema) -> tuple[list[int], list[int], list[int]]:
        group_ids_with_read_permission = (
            list(project_schema.groups_with_read_permission.all().values_list("pk", flat=True))
            if project_schema.groups_with_read_permission
            else []
        )
        group_ids_with_write_permission = (
            list(project_schema.groups_with_write_permission.all().values_list("pk", flat=True))
            if project_schema.groups_with_write_permission
            else []
        )
        group_ids_with_delete_permission = (
            list(project_schema.groups_with_delete_permission.all().values_list("pk", flat=True))
            if project_schema.groups_with_delete_permission
            else []
        )
        return group_ids_with_read_permission, group_ids_with_write_permission, group_ids_with_delete_permission

    def _is_user_in_groups(self, user: User, group_ids: list[str]) -> bool:
        return user.groups.filter(pk__in=group_ids).exists()
