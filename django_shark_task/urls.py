from django.urls import path

from django_shark_task.task.views import (
    LinkTypeView,
    LinkView,
    TaskView,
    TransitTaskView,
    filter_tasks,
    get_task_events,
    get_task_fields,
    get_task_workflow,
)

urlpatterns = [
    path("task/", TaskView.as_view(), name="task_views"),
    path("task/<int:task_id>/", TaskView.as_view(), name="task_views"),
    path("filter_tasks/", filter_tasks, name="filter_task_view"),
    path("task_events/<int:task_id>/", get_task_events, name="task_events_view"),
    path("task_fields/<int:task_id>/", get_task_fields, name="task_fields_view"),
    path("task_workflow/<int:task_id>/", get_task_workflow, name="task_workflow_view"),
    path("link_type/", LinkTypeView.as_view(), name="link_type_view"),
    path("link/", LinkView.as_view(), name="link_view"),
    path("link/<int:link_id>/", LinkView.as_view(), name="link_view"),
    path("transit/<int:task_id>/", TransitTaskView.as_view(), name="transit_task_view"),
]
