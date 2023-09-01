from datetime import datetime
from typing import Optional

from shark_task_fields.serializers import (
    FieldSerializer,
    FieldTypeSerializer,
    ShortFieldTypeSerializer,
    ShotrFieldSerializer,
)

from .models import Field, FieldType


class FieldTypeInfo:
    id: int
    key: str
    config_schema: Optional[dict]
    value_schema: dict
    created: datetime
    updated: datetime


class ShortFieldTypeInfo:
    id: int
    key: str


class FieldInfo:
    id: int
    key: str
    description: Optional[str]
    config: Optional[dict]
    field_type: FieldType
    created: datetime
    updated: datetime


class ShortFieldInfo:
    id: int
    key: str
    field_type: int


class FieldTypesManager:
    def get(self, field_type_id: int) -> FieldTypeInfo:
        field_type = FieldType.objects.get(pk=field_type_id)
        return self._get(field_type)

    def get_list(self) -> list[ShortFieldInfo]:
        field_types = FieldType.objects.all()
        return ShortFieldTypeSerializer(field_types, many=True).data

    def _get(self, field_type: FieldType) -> FieldTypeInfo:
        return FieldTypeSerializer(field_type).data

    def _get_short(self, field_type: Field) -> ShortFieldTypeInfo:
        return ShortFieldTypeSerializer(field_type).data


class FieldsManager:
    def get(self, field_id: int) -> FieldInfo:
        field = Field.objects.get(pk=field_id)
        return self._get(field)

    def get_list(self) -> list[ShortFieldInfo]:
        fields = Field.objects.all()
        return ShotrFieldSerializer(fields, many=True).data

    def _get(self, field: Field) -> FieldInfo:
        return FieldSerializer(field).data

    def _get_short(self, field: Field) -> ShortFieldInfo:
        return ShotrFieldSerializer(field).data
