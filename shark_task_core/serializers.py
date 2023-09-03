from django.contrib.auth import get_user_model
from rest_framework import serializers

from shark_task_core.models import Link, LinkType, TaskEvent
from shark_task_workflow.serializers import StatusSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class ShortTaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    project_id = serializers.IntegerField()
    task_type_id = serializers.IntegerField()
    summary = serializers.CharField()
    creator = UserSerializer()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class FieldInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    value = serializers.DictField(required=False)


class LinkInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    link_type_id = serializers.IntegerField()
    linked_task = ShortTaskSerializer()


class CreateTaskSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    task_type_id = serializers.IntegerField()
    summary = serializers.CharField()
    fields = FieldInfoSerializer(many=True)


class UpdateTaskSerializer(serializers.Serializer):
    summary = serializers.CharField(required=False)
    fields = FieldInfoSerializer(many=True)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    project_id = serializers.IntegerField()
    task_type_id = serializers.IntegerField()
    summary = serializers.CharField()
    status = StatusSerializer()
    key = serializers.CharField()
    task_num = serializers.IntegerField()
    creator = UserSerializer()
    fields = FieldInfoSerializer(many=True)
    inward_links = LinkInfoSerializer(many=True)
    outward_links = LinkInfoSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class RequestTaskListSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()


class TaskEventSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TaskEvent
        fields = (
            "id",
            "type",
            "old_field",
            "old_value",
            "new_field",
            "new_value",
            "user",
            "created",
        )


class LinkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkType
        fields = (
            "id",
            "src_name",
            "dest_name",
            "created",
        )


class CreateLinkSerializer(serializers.Serializer):
    link_type_id = serializers.IntegerField()
    src_task_id = serializers.IntegerField()
    dest_task_id = serializers.IntegerField()


class LinkSerializer(serializers.ModelSerializer):
    link_type = LinkTypeSerializer
    src_task = ShortTaskSerializer
    dest_task = ShortTaskSerializer

    class Meta:
        model = Link
        fields = (
            "id",
            "link_type",
            "src_task",
            "dest_task",
            "created",
        )


class TransitTaskSerializer(serializers.Serializer):
    transition_id = serializers.IntegerField()
