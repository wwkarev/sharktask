from rest_framework import serializers


class FieldTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()
    config_schema = serializers.DictField(required=False)
    value_schema = serializers.DictField(required=False)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ShortFieldTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()


class FieldSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()
    config = serializers.DictField(required=False)
    field_type = FieldTypeSerializer()
    description = serializers.CharField()
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ShotrFieldSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    key = serializers.CharField()
    field_type = ShortFieldTypeSerializer()


class ScreenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    fields = FieldSerializer(many=True)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()


class ShotrScreenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    fields = ShotrFieldSerializer(many=True)
