from rest_framework import serializers

from shark_task_workflow.models import Status, StatusType


class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = ("id", "name")


class StatusSerializer(serializers.ModelSerializer):
    status_type = StatusTypeSerializer()

    class Meta:
        model = Status
        fields = ("id", "name", "status_type", "created")
