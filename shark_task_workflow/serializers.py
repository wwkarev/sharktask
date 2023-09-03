from rest_framework import serializers

from shark_task_workflow.models import Status, StatusType, Transition


class StatusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusType
        fields = ("id", "name")


class StatusSerializer(serializers.ModelSerializer):
    status_type = StatusTypeSerializer()

    class Meta:
        model = Status
        fields = ("id", "name", "status_type", "created")


class TransitionSerializer(serializers.ModelSerializer):
    src_status = StatusSerializer()
    dest_status = StatusSerializer()

    class Meta:
        model = Transition
        fields = ("id", "name", "src_status", "dest_status", "workflow", "is_initial", "created", "updated")
