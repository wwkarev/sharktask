from rest_framework import serializers

from django_shark_task.fields.models import Field, FieldType, ScreenField


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ["id", "key", "config_schema", "value_schema", "created", "updated"]


class ShortFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ["id", "key", "name"]


class FieldSerializer(serializers.ModelSerializer):
    field_type = FieldTypeSerializer()

    class Meta:
        model = Field
        fields = ["id", "key", "name", "config", "field_type", "description", "created", "updated"]


class ScreenFieldSerializer(serializers.ModelSerializer):
    field = FieldSerializer()

    class Meta:
        model = ScreenField
        fields = ["id", "screen", "field", "is_required", "priority", "created", "updated"]
