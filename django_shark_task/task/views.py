from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_shark_task.fields.models import ScreenField
from django_shark_task.fields.serializers import ScreenFieldSerializer
from django_shark_task.task.link_manager import LinkManager
from django_shark_task.task.models import LinkType, Task, TaskEvent
from django_shark_task.task.serializers import (
    CreateLinkSerializer,
    CreateTaskSerializer,
    LinkSerializer,
    LinkTypeSerializer,
    RequestTaskListSerializer,
    ShortTaskSerializer,
    TaskEventSerializer,
    TaskSerializer,
    TransitTaskSerializer,
    UpdateTaskSerializer,
)
from django_shark_task.task.task_manager import CreateTaskInfo, TaskManager, UpdateTaskInfo
from django_shark_task.workflow.models import Transition
from django_shark_task.workflow.serializers import TransitionSerializer


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CreateTaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task_manager = TaskManager()
            create_task_info = CreateTaskInfo(**serializer.data)
            task_info = task_manager.create(create_task_info, request.user)
            return Response(TaskSerializer(task_info.dict()).data)
        except Exception as e:
            print(e)
            raise e

    def put(self, request, task_id: int):
        try:
            serializer = UpdateTaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task_manager = TaskManager()
            update_task_info = UpdateTaskInfo(**serializer.data)
            task_info = task_manager.update(task_id, update_task_info, request.user)
            return Response(TaskSerializer(task_info.dict()).data)
        except Exception as e:
            print(e)
            raise e

    def get(self, request, task_id):
        task_manager = TaskManager()
        task_info = task_manager.get(task_id, request.user)
        return Response(TaskSerializer(task_info.dict()).data)

    def delete(self, request, task_id):
        try:
            task_manager = TaskManager()
            task_manager.delete(task_id, request.user)
            return Response(f"Task with id {task_id} deleted")
        except Exception as e:
            print(e)
            raise e


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def filter_tasks(request):
    serializer = RequestTaskListSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    task_manager = TaskManager()
    task_info_list = task_manager.filter_task(serializer.data["project_id"])
    return Response(ShortTaskSerializer([task_info.dict() for task_info in task_info_list], many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_events(request, task_id: int):
    return Response(TaskEventSerializer(TaskEvent.objects.filter(task_id=task_id).order_by("-created"), many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_fields(request, task_id: int):
    task = Task.objects.select_related("project_schema").get(pk=task_id)
    screen_fields = ScreenField.objects.filter(screen_id=task.project_schema.screen_id).order_by("priority")
    return Response(ScreenFieldSerializer(screen_fields, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_task_workflow(request, task_id: int):
    task = Task.objects.select_related("project_schema").get(pk=task_id)
    transitions = Transition.objects.filter(workflow_id=task.project_schema.workflow_id)
    return Response(TransitionSerializer(transitions, many=True).data)


class LinkTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(LinkTypeSerializer(LinkType.objects.all(), many=True).data)


class LinkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        link_manager = LinkManager()
        link = link_manager.create(data["link_type_id"], data["src_task_id"], data["dest_task_id"], request.user)
        return Response(LinkSerializer(link).data)

    def delete(self, request, link_id):
        link_manager = LinkManager()
        link_manager.delete(link_id, request.user)
        return Response(f"Link with id {link_id} deleted")


class TransitTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        try:
            serializer = TransitTaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task_manager = TaskManager()
            task_manager.transit(task_id, serializer.data["transition_id"], request.user)
            task_info = task_manager.get(task_id)
            return Response(TaskSerializer(task_info.dict()).data)
        except Exception as e:
            print(e)
            raise e

    def get(self, request, task_id):
        task_manager = TaskManager()
        transitions = task_manager.get_transitions(task_id, request.user)
        return Response(TransitionSerializer(transitions, many=True).data)
