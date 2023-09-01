from datetime import datetime

from shark_task_fields.serializers import ScreenSerializer, ShotrScreenSerializer

from .models import Screen
from .task_fields_manager import FieldInfo, ShortFieldInfo


class ScreenInfo:
    id: int
    name: str
    description: str
    fields: list[FieldInfo]
    value_schema: dict
    created: datetime
    updated: datetime


class ShortScreenInfo:
    id: int
    name: str
    description: str
    fields: list[ShortFieldInfo]


class ScreenManager:
    def get(self, screen_id: int) -> ScreenInfo:
        screen = Screen.objects.get(pk=screen_id)
        return self._get(screen)

    def get_list(self) -> list[ShortScreenInfo]:
        screens = Screen.objects.all()
        return ShotrScreenSerializer(screens, many=True).data

    def _get(self, screen: Screen) -> ScreenInfo:
        return ScreenSerializer(screen).data

    def _get_short(self, screen: Screen) -> ShortScreenInfo:
        return ShotrScreenSerializer(screen).data
