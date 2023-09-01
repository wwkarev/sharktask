from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from shark_task_core.link_manager import LinkManager
from shark_task_core.models import LinkType, TaskEvent
from shark_task_core.serializers import (
    CreateLinkSerializer,
    CreateTaskSerializer,
    LinkSerializer,
    LinkTypeSerializer,
    RequestTaskListSerializer,
    ShortTaskSerializer,
    TaskEventSerializer,
    TaskSerializer,
    UpdateTaskSerializer,
)
from shark_task_core.task_manager import CreateTaskInfo, TaskManager, UpdateTaskInfo
from shark_task_core.task_type_manager import TaskTypeManager


class TaskTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_type_id=None):
        if not task_type_id:
            return self.list(request)

        task_type_manager = TaskTypeManager()
        task_type_info = task_type_manager.get(task_type_id)
        return Response(task_type_info)

    def list(self, request):
        task_type_manager = TaskTypeManager()
        task_types = task_type_manager.get_list()
        return Response(task_types)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = CreateTaskSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task_manager = TaskManager()
            create_task_info = CreateTaskInfo(**serializer.data)
            print(create_task_info)
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
            print(update_task_info)
            task_info = task_manager.update(task_id, update_task_info, request.user)
            return Response(TaskSerializer(task_info.dict()).data)
        except Exception as e:
            print(e)
            raise e

    def get(self, request, task_id=None):
        if not task_id:
            return self.list(request)

        task_manager = TaskManager()
        task_info = task_manager.get(task_id)
        return Response(TaskSerializer(task_info.dict()).data)

    def list(self, request):
        task_manager = TaskManager()
        tasks = task_manager.get_list()
        return Response(ShortTaskSerializer([task_info.dict() for task_info in tasks], many=True).data)

    def delete(self, request, task_id):
        try:
            task_manager = TaskManager()
            task_manager.delete(task_id)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transit_task(request, task_id: int, transition_id: int):
    return Response(TaskEventSerializer(TaskEvent.objects.filter(task_id=task_id).order_by("-created"), many=True).data)
