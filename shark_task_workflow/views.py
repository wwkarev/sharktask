from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Status, Transition, Workflow
from .serializers import StatusSerializer, TransitionSerializer, WorkflowSerializer


class StatusesViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"])
    def transitions(self, request, pk, *args, **kwargs):
        transitions = Transition.objects.filter(src_status__pk=pk)

        return Response(TransitionSerializer(transitions, many=True).data)


class WorkflowsViewSet(ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [IsAuthenticated]


class TransitionsViewSet(ModelViewSet):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    permission_classes = [IsAuthenticated]
