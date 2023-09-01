from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Field, FieldType, Screen
from .serializers import (
    FieldSerializer,
    FieldTypeSerializer,
    ScreenSerializer,
    ShortFieldTypeSerializer,
    ShotrFieldSerializer,
    ShotrScreenSerializer,
)


class FieldTypesView(ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer
    list_serializer_class = ShortFieldTypeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)


class FieldsView(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    list_serializer_class = ShotrFieldSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)


class ScreensView(ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer
    list_serializer_class = ShotrScreenSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.serializer_class = self.list_serializer_class
        return super().list(request, *args, **kwargs)
